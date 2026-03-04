#!/usr/bin/env python3
"""
prepare_samples.py — Prepare audio samples for voice model training.

Workflow:
  1. Scan input directory for audio files (wav, mp3, m4a, flac)
  2. Transcribe each file with Whisper (for alignment + QC)
  3. Split into segments of target_duration with silence-based splitting
  4. Apply noise reduction (optional, via DeepFilterNet)
  5. Normalize loudness (EBU R128)
  6. Output: clean .wav segments + transcript JSON

Usage:
  python scripts/prepare_samples.py \
    --input /path/to/recordings/ \
    --output data/voice_samples/ \
    --min_duration 5 \
    --max_duration 30 \
    --denoise
"""

import argparse
import json
import os
import subprocess
from pathlib import Path


def find_audio_files(input_dir: str) -> list[Path]:
    """Find all audio files in directory, recursively."""
    extensions = {".wav", ".mp3", ".m4a", ".flac", ".ogg", ".aac"}
    input_path = Path(input_dir)
    files = []
    for ext in extensions:
        files.extend(input_path.rglob(f"*{ext}"))
    return sorted(files)


def convert_to_wav(input_file: Path, output_file: Path) -> None:
    """Convert any audio format to 16kHz mono WAV (Whisper/RVC standard)."""
    cmd = [
        "ffmpeg", "-i", str(input_file),
        "-ar", "16000",  # 16kHz sample rate
        "-ac", "1",       # mono
        "-acodec", "pcm_s16le",
        str(output_file),
        "-y", "-loglevel", "error"
    ]
    subprocess.run(cmd, check=True)


def transcribe(wav_file: Path, model: str = "large-v3") -> dict:
    """Transcribe audio with Whisper. Returns segments with timestamps."""
    try:
        import whisper
        model_instance = whisper.load_model(model)
        result = model_instance.transcribe(str(wav_file), word_timestamps=True)
        return result
    except ImportError:
        print("  [!] whisper not installed. Run: pip install openai-whisper")
        return {"segments": []}


def split_on_silence(wav_file: Path, output_dir: Path, min_dur: float, max_dur: float) -> list[Path]:
    """Split audio on silence using ffmpeg silencedetect."""
    # Detect silence
    cmd = [
        "ffmpeg", "-i", str(wav_file),
        "-af", "silencedetect=noise=-40dB:d=0.5",
        "-f", "null", "-"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Parse silence timestamps from stderr
    silence_ends = []
    for line in result.stderr.split("\n"):
        if "silence_end" in line:
            parts = line.split("|")
            end_time = float(parts[0].split("silence_end: ")[1].strip())
            silence_ends.append(end_time)

    if not silence_ends:
        # No silence detected — output entire file as one segment
        out = output_dir / f"{wav_file.stem}_000.wav"
        import shutil
        shutil.copy(wav_file, out)
        return [out]

    # Build segments respecting min/max duration
    segments = []
    prev = 0.0
    for end in silence_ends + [float("inf")]:
        duration = end - prev
        if min_dur <= duration <= max_dur:
            segments.append((prev, end))
            prev = end
        elif duration > max_dur:
            # Force-split long segment
            cursor = prev
            while cursor + max_dur < end:
                segments.append((cursor, cursor + max_dur))
                cursor += max_dur
            if end - cursor >= min_dur:
                segments.append((cursor, end))
            prev = end

    # Extract segments
    output_files = []
    for i, (start, end) in enumerate(segments):
        out = output_dir / f"{wav_file.stem}_{i:04d}.wav"
        duration = min(end - start, max_dur)
        cmd = [
            "ffmpeg", "-i", str(wav_file),
            "-ss", str(start), "-t", str(duration),
            "-ar", "16000", "-ac", "1",
            str(out), "-y", "-loglevel", "error"
        ]
        subprocess.run(cmd, check=True)
        output_files.append(out)

    return output_files


def normalize_loudness(wav_file: Path) -> None:
    """Normalize to -23 LUFS (EBU R128) in-place."""
    tmp = wav_file.with_suffix(".tmp.wav")
    cmd = [
        "ffmpeg", "-i", str(wav_file),
        "-af", "loudnorm=I=-23:TP=-1.5:LRA=11",
        str(tmp), "-y", "-loglevel", "error"
    ]
    subprocess.run(cmd, check=True)
    os.replace(tmp, wav_file)


def apply_denoise(wav_file: Path) -> None:
    """Apply DeepFilterNet noise reduction if available."""
    try:
        import df
        # DeepFilterNet CLI: dfnet --input file --output file
        tmp = wav_file.with_suffix(".denoised.wav")
        cmd = ["dfnet", str(wav_file), "-o", str(tmp)]
        subprocess.run(cmd, check=True)
        os.replace(tmp, wav_file)
    except (ImportError, FileNotFoundError):
        # Fallback: ffmpeg highpass filter (basic)
        tmp = wav_file.with_suffix(".tmp.wav")
        cmd = [
            "ffmpeg", "-i", str(wav_file),
            "-af", "highpass=f=100,lowpass=f=8000",
            str(tmp), "-y", "-loglevel", "error"
        ]
        subprocess.run(cmd, check=True)
        os.replace(tmp, wav_file)


def main():
    parser = argparse.ArgumentParser(description="Prepare voice samples for training")
    parser.add_argument("--input", required=True, help="Input directory with recordings")
    parser.add_argument("--output", required=True, help="Output directory for clean samples")
    parser.add_argument("--min_duration", type=float, default=5.0, help="Min segment duration (sec)")
    parser.add_argument("--max_duration", type=float, default=30.0, help="Max segment duration (sec)")
    parser.add_argument("--denoise", action="store_true", help="Apply noise reduction")
    parser.add_argument("--transcribe", action="store_true", help="Transcribe segments with Whisper")
    parser.add_argument("--whisper_model", default="large-v3", help="Whisper model size")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir = output_dir / "_tmp"
    tmp_dir.mkdir(exist_ok=True)

    audio_files = find_audio_files(args.input)
    print(f"Found {len(audio_files)} audio files")

    all_segments = []
    for i, audio_file in enumerate(audio_files):
        print(f"\n[{i+1}/{len(audio_files)}] {audio_file.name}")

        # Convert to standard WAV
        tmp_wav = tmp_dir / f"{audio_file.stem}.wav"
        print("  → Converting to 16kHz mono WAV...")
        convert_to_wav(audio_file, tmp_wav)

        # Split on silence
        print(f"  → Splitting (min={args.min_duration}s, max={args.max_duration}s)...")
        segments = split_on_silence(tmp_wav, output_dir, args.min_duration, args.max_duration)
        print(f"  → {len(segments)} segments")

        # Post-process each segment
        for seg in segments:
            if args.denoise:
                apply_denoise(seg)
            normalize_loudness(seg)
            all_segments.append(seg)

    # Transcribe if requested
    if args.transcribe:
        print(f"\nTranscribing {len(all_segments)} segments...")
        transcripts = {}
        for seg in all_segments:
            print(f"  → {seg.name}")
            result = transcribe(seg, args.whisper_model)
            transcripts[seg.name] = result.get("text", "")

        transcript_file = output_dir / "transcripts.json"
        with open(transcript_file, "w") as f:
            json.dump(transcripts, f, ensure_ascii=False, indent=2)
        print(f"\nTranscripts saved to {transcript_file}")

    # Summary
    total_duration = 0
    for seg in all_segments:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(seg)],
            capture_output=True, text=True
        )
        try:
            total_duration += float(result.stdout.strip())
        except ValueError:
            pass

    print(f"\n{'='*50}")
    print(f"Output: {len(all_segments)} segments in {output_dir}")
    print(f"Total duration: {total_duration/60:.1f} minutes")
    print(f"\nFor ElevenLabs: upload all .wav files from {output_dir}")
    print(f"For RVC: run scripts/train_rvc.py --samples {output_dir}")
    print(f"For F5-TTS: no training needed — use segments as voice reference directly")

    # Cleanup tmp
    import shutil
    shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    main()
