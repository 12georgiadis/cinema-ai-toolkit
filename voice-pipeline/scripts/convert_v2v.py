#!/usr/bin/env python3
"""
convert_v2v.py — Voice-to-Voice conversion.

Takes a "style reference" audio (the flow/cadence/prosody you want)
and converts it to sound like the target voice model (timbre).

Result: style source's rhythm and pacing, target's vocal identity.

Backends:
  - rvc    : RVC v2 (local, GPU recommended but CPU works)
  - openvoice : OpenVoice v2 (local, CPU-friendly)
  - elevenlabs : ElevenLabs API (cloud, no GPU, highest quality)

Usage:
  # RVC backend
  python scripts/convert_v2v.py \
    --input style_reference.wav \
    --model models/voice_model.pth \
    --backend rvc \
    --output output/result.wav

  # OpenVoice backend
  python scripts/convert_v2v.py \
    --input style_reference.wav \
    --voice_reference subject_sample.wav \
    --backend openvoice \
    --output output/result.wav

  # ElevenLabs backend
  python scripts/convert_v2v.py \
    --input style_reference.wav \
    --voice_id "elevenlabs_voice_id" \
    --backend elevenlabs \
    --output output/result.wav
"""

import argparse
import os
import tempfile
from pathlib import Path


# ─── Backend: RVC ─────────────────────────────────────────────────────────────

def convert_rvc(
    input_audio: Path,
    model_path: Path,
    output_audio: Path,
    pitch_shift: int = 0,
    f0_method: str = "rmvpe",
) -> None:
    """
    Convert audio using RVC (Retrieval-based Voice Conversion).

    RVC preserves the source prosody (rhythm, pacing, pitch contour shape)
    and transfers the timbre/identity of the trained voice model.

    f0_method options: rmvpe (best quality), crepe, harvest, pm
    pitch_shift: semitones, adjust if subject and reference have different registers
    """
    try:
        # Try rvc-python package first (pip install rvc-python)
        from rvc_python.infer import RVCInference
        rvc = RVCInference()
        rvc.load_model(str(model_path))
        rvc.infer_file(
            input_path=str(input_audio),
            output_path=str(output_audio),
            f0_up_key=pitch_shift,
            f0_method=f0_method,
        )
    except ImportError:
        # Fallback: call RVC CLI if installed
        import subprocess
        cmd = [
            "python", "-m", "rvc",
            "--input", str(input_audio),
            "--model", str(model_path),
            "--output", str(output_audio),
            "--f0_up_key", str(pitch_shift),
            "--f0_method", f0_method,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(
                f"RVC failed. Install with: pip install rvc-python\n"
                f"Or see: https://github.com/RVC-Boss/RVC\n"
                f"Error: {result.stderr}"
            )


# ─── Backend: OpenVoice ───────────────────────────────────────────────────────

def convert_openvoice(
    input_audio: Path,
    voice_reference: Path,
    output_audio: Path,
) -> None:
    """
    Convert using OpenVoice v2.

    OpenVoice separates "tone color" from style — it extracts the tone color
    (timbre identity) from voice_reference and applies it to input_audio's
    rhythm, pacing, and content.

    Install: pip install openvoice
    Model weights: https://huggingface.co/myshell-ai/OpenVoiceV2
    """
    try:
        from openvoice import se_extractor
        from openvoice.api import ToneColorConverter

        model_dir = Path("models/openvoice_v2")
        if not model_dir.exists():
            raise FileNotFoundError(
                f"OpenVoice model not found at {model_dir}. "
                "Download from: https://huggingface.co/myshell-ai/OpenVoiceV2"
            )

        converter = ToneColorConverter(str(model_dir / "converter/config.json"))
        converter.load_ckpt(str(model_dir / "converter/checkpoint.pth"))

        # Extract tone color from reference
        target_se, _ = se_extractor.get_se(
            str(voice_reference),
            converter,
            target_dir="temp_se",
            vad=True,
        )

        # Extract tone color from input (source)
        source_se, _ = se_extractor.get_se(
            str(input_audio),
            converter,
            target_dir="temp_se",
            vad=True,
        )

        # Convert: keep input's prosody, apply reference's timbre
        converter.convert(
            audio_src_path=str(input_audio),
            src_se=source_se,
            tgt_se=target_se,
            output_path=str(output_audio),
        )

    except ImportError:
        raise ImportError(
            "OpenVoice not installed. Run: pip install openvoice\n"
            "Or see: https://github.com/myshell-ai/OpenVoice"
        )


# ─── Backend: ElevenLabs ─────────────────────────────────────────────────────

def convert_elevenlabs(
    input_audio: Path,
    voice_id: str,
    output_audio: Path,
    style_exaggeration: float = 0.5,
) -> None:
    """
    Convert using ElevenLabs Voice Changer (Speech-to-Speech).

    ElevenLabs STS preserves the source speech's pacing and emotional content
    while converting to the target voice. style_exaggeration (0-1) controls
    how strongly the reference voice's speaking style is imposed.

    Requires: pip install elevenlabs
    Requires: ELEVENLABS_API_KEY environment variable
    """
    try:
        from elevenlabs.client import ElevenLabs

        api_key = os.environ.get("ELEVENLABS_API_KEY")
        if not api_key:
            raise ValueError(
                "Set ELEVENLABS_API_KEY environment variable. "
                "Get your key at: https://elevenlabs.io"
            )

        client = ElevenLabs(api_key=api_key)

        with open(input_audio, "rb") as f:
            audio_data = f.read()

        # Speech-to-Speech conversion
        audio_stream = client.speech_to_speech.convert(
            voice_id=voice_id,
            audio=audio_data,
            model_id="eleven_english_sts_v2",
            voice_settings={
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": style_exaggeration,
                "use_speaker_boost": True,
            },
        )

        with open(output_audio, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)

    except ImportError:
        raise ImportError("Run: pip install elevenlabs")


# ─── Backend: F5-TTS (Zero-shot) ─────────────────────────────────────────────

def convert_f5tts(
    input_audio: Path,
    voice_reference: Path,
    output_audio: Path,
    transcription: str = "",
) -> None:
    """
    Zero-shot voice conversion via F5-TTS.

    F5-TTS doesn't require a trained model — it clones from a reference
    clip directly. Less prosody preservation than RVC, but zero setup.

    If transcription is empty, Whisper is used to transcribe the input.

    Install: pip install f5-tts
    """
    try:
        import subprocess

        # If no transcription provided, use whisper
        if not transcription:
            try:
                import whisper
                model = whisper.load_model("base")
                result = model.transcribe(str(input_audio))
                transcription = result["text"].strip()
                print(f"  Transcribed: {transcription[:80]}...")
            except ImportError:
                raise ValueError(
                    "Provide --transcription text or install openai-whisper: "
                    "pip install openai-whisper"
                )

        cmd = [
            "f5-tts_infer-cli",
            "--model", "F5TTS_v1_Base",
            "--ref_audio", str(voice_reference),
            "--ref_text", transcription,
            "--gen_text", transcription,
            "--output_dir", str(output_audio.parent),
            "--output_file", output_audio.name,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"F5-TTS failed: {result.stderr}")

    except FileNotFoundError:
        raise FileNotFoundError(
            "F5-TTS CLI not found. Install: pip install f5-tts"
        )


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Voice-to-Voice conversion: transfer prosody from source to target voice"
    )
    parser.add_argument("--input", required=True, help="Source audio (style/cadence reference)")
    parser.add_argument("--output", required=True, help="Output audio file")
    parser.add_argument(
        "--backend", choices=["rvc", "openvoice", "elevenlabs", "f5tts"],
        default="rvc", help="Conversion backend"
    )
    # RVC options
    parser.add_argument("--model", help="RVC model .pth file path")
    parser.add_argument("--pitch_shift", type=int, default=0, help="Pitch shift in semitones (RVC)")
    parser.add_argument("--f0_method", default="rmvpe", help="F0 extraction method (RVC)")
    # OpenVoice / F5-TTS options
    parser.add_argument("--voice_reference", help="Reference audio for target timbre")
    # ElevenLabs options
    parser.add_argument("--voice_id", help="ElevenLabs voice ID")
    parser.add_argument("--style", type=float, default=0.5, help="Style exaggeration 0-1 (ElevenLabs)")
    # F5-TTS options
    parser.add_argument("--transcription", default="", help="Text transcription of input (F5-TTS)")

    args = parser.parse_args()

    input_audio = Path(args.input)
    output_audio = Path(args.output)
    output_audio.parent.mkdir(parents=True, exist_ok=True)

    print(f"Backend: {args.backend}")
    print(f"Input:   {input_audio}")
    print(f"Output:  {output_audio}")

    if args.backend == "rvc":
        if not args.model:
            parser.error("--model required for RVC backend")
        print("Converting with RVC...")
        convert_rvc(input_audio, Path(args.model), output_audio, args.pitch_shift, args.f0_method)

    elif args.backend == "openvoice":
        if not args.voice_reference:
            parser.error("--voice_reference required for OpenVoice backend")
        print("Converting with OpenVoice v2...")
        convert_openvoice(input_audio, Path(args.voice_reference), output_audio)

    elif args.backend == "elevenlabs":
        if not args.voice_id:
            parser.error("--voice_id required for ElevenLabs backend")
        print("Converting with ElevenLabs Speech-to-Speech...")
        convert_elevenlabs(input_audio, args.voice_id, output_audio, args.style)

    elif args.backend == "f5tts":
        if not args.voice_reference:
            parser.error("--voice_reference required for F5-TTS backend")
        print("Converting with F5-TTS (zero-shot)...")
        convert_f5tts(input_audio, Path(args.voice_reference), output_audio, args.transcription)

    print(f"\nDone → {output_audio}")


if __name__ == "__main__":
    main()
