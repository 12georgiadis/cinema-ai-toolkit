#!/usr/bin/env python3
"""
Audio enhancement via fal.ai — Lava-SR model.
16kHz → denoised 48kHz (speech super-resolution).

Usage:
  python enhance_fal.py input.wav                    # single file
  python enhance_fal.py input.wav --out output.wav   # specify output
  python enhance_fal.py --batch dir/                 # process directory

Requires: FAL_KEY environment variable
  export FAL_KEY=your_key_here
  or: source ~/.secrets/fal.env
"""

import sys
import os
import subprocess
from pathlib import Path

try:
    import fal_client
except ImportError:
    print("Install: pip install fal-client")
    sys.exit(1)


def enhance_file(input_path: Path, output_path: Path = None) -> Path:
    """Upload to fal.ai Lava-SR, download result."""
    if not input_path.exists():
        raise FileNotFoundError(input_path)

    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}_lavasr.mp3"

    if output_path.exists():
        print(f"SKIP (exists): {output_path.name}")
        return output_path

    print(f"Uploading {input_path.name} ({input_path.stat().st_size // 1024}KB)...")
    audio_url = fal_client.upload_file(str(input_path))

    print("Running Lava-SR (denoising + 48kHz upscaling)...")
    result = fal_client.run(
        "fal-ai/lava-sr",
        arguments={"audio_url": audio_url}
    )

    out_url = result["audio"]["url"]
    sr = result["audio"]["sample_rate"]
    duration = result["audio"]["duration"]
    timing = result.get("timings", {}).get("inference", 0)

    print(f"Done: {duration:.0f}s audio at {sr}Hz — inference {timing:.1f}s")

    # Download result
    subprocess.run(["curl", "-s", out_url, "-o", str(output_path)], check=True)
    print(f"Saved: {output_path}")
    return output_path


def batch_enhance(input_dir: Path, output_dir: Path = None):
    """Process all WAV/MP3 files in a directory."""
    if output_dir is None:
        output_dir = input_dir / "enhanced"
    output_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(input_dir.glob("*.wav")) + sorted(input_dir.glob("*.mp3"))
    print(f"Found {len(files)} files in {input_dir}")

    for f in files:
        out = output_dir / f"{f.stem}_lavasr.mp3"
        try:
            enhance_file(f, out)
        except Exception as e:
            print(f"ERROR {f.name}: {e}")


if __name__ == "__main__":
    if "--batch" in sys.argv:
        idx = sys.argv.index("--batch")
        d = Path(sys.argv[idx + 1])
        batch_enhance(d)
    elif len(sys.argv) >= 2:
        inp = Path(sys.argv[1])
        out = Path(sys.argv[3]) if "--out" in sys.argv else None
        enhance_fal = enhance_file(inp, out)
    else:
        print(__doc__)
