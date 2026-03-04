#!/usr/bin/env python3
"""
Pipeline de préparation audio pour voice cloning — Goldberg / Joshua
Ordre : Dénoise (DeepFilterNet) → Normalisation → Segmentation

RÈGLE : ne jamais modifier les originaux. Tout va dans processed/

Usage:
  python process_pipeline.py <fichier.wav>          # traiter un fichier
  python process_pipeline.py --batch                 # traiter tous les prioritaires
  python process_pipeline.py --segment-only <fichier_enhancé.wav>
"""

import sys
import os
import subprocess
import shutil
import json
import argparse
from pathlib import Path
import numpy as np
import librosa
import soundfile as sf
from datetime import datetime

# Chemins configurables via --audio-dir et --output-dir
# Défaut : structure relative au script (pour le repo public)
_DEFAULT_AUDIO = Path(__file__).parent / "2026-tournage-zoom/audio"
_DEFAULT_OUTPUT = Path(__file__).parent / "processed"

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--audio-dir", type=Path, default=_DEFAULT_AUDIO)
parser.add_argument("--output-dir", type=Path, default=_DEFAULT_OUTPUT)
_args, _ = parser.parse_known_args()

AUDIO_DIR = _args.audio_dir
PROCESSED = _args.output_dir
DIR_ENHANCED = PROCESSED / "01-enhanced"
DIR_SEGMENTS = PROCESSED / "02-segments"
DIR_NORMALIZED = PROCESSED / "03-normalized"
DIR_REPORTS = PROCESSED / "analysis-reports"

for d in [DIR_ENHANCED, DIR_SEGMENTS, DIR_NORMALIZED, DIR_REPORTS]:
    d.mkdir(parents=True, exist_ok=True)

# Fichiers prioritaires (triés par qualité)
PRIORITY_FILES = [
    "F260228_003_Mic12.wav",   # 56min, mic ext, SNR 35.5dB — SOURCE PRINCIPALE
    "F260228_002_Mic12.wav",   # 17min, mic ext, SNR excellent
    "F260302_005_Tr1.wav",     # 58min, Canon, SNR 31.3dB
    "F260302_003_Tr1.wav",     # 52min, Canon, SNR 31.5dB
    "F260303_006_Tr1.wav",     # 27min, Canon (3 mars)
    "F260303_007_Tr1.wav",     # 12min, Canon (3 mars)
]


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def denoise_deepfilter(input_path: Path, output_path: Path) -> bool:
    """Débruite avec DeepFilterNet. Retourne True si succès."""
    if output_path.exists():
        log(f"  SKIP (déjà fait) : {output_path.name}")
        return True

    log(f"  DeepFilterNet → {output_path.name}")
    tmp_dir = DIR_ENHANCED / "_tmp"
    tmp_dir.mkdir(exist_ok=True)

    # DeepFilterNet CLI : deepFilter input.wav -o output_dir/
    result = subprocess.run(
        ["deepFilter", str(input_path), "-o", str(tmp_dir)],
        capture_output=True, text=True
    )

    # DeepFilter écrit dans output_dir/basename.wav
    tmp_out = tmp_dir / input_path.name
    if tmp_out.exists():
        shutil.move(str(tmp_out), str(output_path))
        tmp_dir.rmdir() if not list(tmp_dir.iterdir()) else None
        log(f"  ✓ Enhanced : {output_path.name}")
        return True
    else:
        log(f"  ✗ Erreur DeepFilterNet : {result.stderr[:200]}")
        return False


def normalize_file(input_path: Path, output_path: Path,
                   target_rms_db: float = -18.0, true_peak_db: float = -3.0) -> dict:
    """Normalise à -18 dBFS RMS, true peak -3 dBFS."""
    if output_path.exists():
        log(f"  SKIP (déjà fait) : {output_path.name}")
        return {}

    y, sr = librosa.load(str(input_path), sr=None, mono=True)

    current_rms = np.sqrt(np.mean(y**2))
    current_rms_db = 20 * np.log10(current_rms + 1e-9)
    gain = 10 ** ((target_rms_db - current_rms_db) / 20)
    y_norm = y * gain

    # True peak limiting
    peak = np.abs(y_norm).max()
    peak_db = 20 * np.log10(peak + 1e-9)
    if peak_db > true_peak_db:
        y_norm = y_norm * (10 ** (true_peak_db / 20)) / peak

    sf.write(str(output_path), y_norm, sr, subtype='PCM_24')
    final_rms_db = 20 * np.log10(np.sqrt(np.mean(y_norm**2)) + 1e-9)
    log(f"  ✓ Normalisé : {current_rms_db:.1f}dB → {final_rms_db:.1f}dB RMS")
    return {"input_rms_db": round(current_rms_db, 1), "output_rms_db": round(final_rms_db, 1)}


def segment_file(input_path: Path, output_dir: Path,
                 min_dur: float = 5.0, max_dur: float = 30.0,
                 top_db: float = 40.0) -> list:
    """
    Découpe le fichier en segments de voix propre (5-30s).
    top_db : seuil silence en dB sous le pic (40 = détecte tout sauf silence profond)
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    existing = list(output_dir.glob(f"{input_path.stem}_seg_*.wav"))
    if existing:
        log(f"  SKIP segmentation (déjà {len(existing)} segments)")
        return [str(f) for f in sorted(existing)]

    log(f"  Segmentation : {input_path.name}")
    y, sr = librosa.load(str(input_path), sr=None, mono=True)

    # Détecter les intervalles de non-silence
    intervals = librosa.effects.split(y, top_db=top_db, frame_length=2048, hop_length=512)

    segments = []
    seg_idx = 0

    for start_sample, end_sample in intervals:
        dur = (end_sample - start_sample) / sr
        if dur < min_dur:
            continue
        if dur <= max_dur:
            seg = y[start_sample:end_sample]
            out = output_dir / f"{input_path.stem}_seg_{seg_idx:04d}.wav"
            sf.write(str(out), seg, sr, subtype='PCM_24')
            segments.append(str(out))
            seg_idx += 1
        else:
            # Découper en sous-segments de max_dur
            pos = start_sample
            while pos < end_sample:
                end_pos = min(pos + int(max_dur * sr), end_sample)
                seg = y[pos:end_pos]
                seg_dur = len(seg) / sr
                if seg_dur >= min_dur:
                    out = output_dir / f"{input_path.stem}_seg_{seg_idx:04d}.wav"
                    sf.write(str(out), seg, sr, subtype='PCM_24')
                    segments.append(str(out))
                    seg_idx += 1
                pos = end_pos

    total_dur = sum(
        librosa.get_duration(path=s) for s in segments
    )
    log(f"  ✓ {len(segments)} segments, {total_dur/60:.1f} min total")
    return segments


def process_file(filename: str, denoise: bool = True,
                 normalize: bool = True, segment: bool = True) -> dict:
    """Pipeline complet sur un fichier. Retourne un rapport."""
    src = AUDIO_DIR / filename
    if not src.exists():
        log(f"✗ Fichier introuvable : {src}")
        return {}

    stem = Path(filename).stem
    log(f"\n{'='*50}")
    log(f"TRAITEMENT : {filename}")
    log(f"{'='*50}")

    report = {"file": filename, "steps": {}}

    # Étape 1 — Débruitage
    enhanced_path = DIR_ENHANCED / f"{stem}_enhanced.wav"
    if denoise:
        log("Étape 1 : Débruitage DeepFilterNet")
        ok = denoise_deepfilter(src, enhanced_path)
        report["steps"]["denoise"] = "ok" if ok else "error"
        if not ok:
            log("  Fallback : copie sans débruitage")
            shutil.copy2(str(src), str(enhanced_path))
            report["steps"]["denoise"] = "skipped"
    else:
        if not enhanced_path.exists():
            log("Étape 1 : Copie (pas de débruitage)")
            shutil.copy2(str(src), str(enhanced_path))
        report["steps"]["denoise"] = "skipped"

    # Étape 2 — Normalisation
    norm_path = DIR_NORMALIZED / f"{stem}_norm.wav"
    if normalize:
        log("Étape 2 : Normalisation -18dB RMS")
        stats = normalize_file(enhanced_path, norm_path)
        report["steps"]["normalize"] = stats

    # Étape 3 — Segmentation
    seg_dir = DIR_SEGMENTS / stem
    if segment:
        log("Étape 3 : Segmentation (5-30s)")
        source_for_seg = norm_path if norm_path.exists() else enhanced_path
        segs = segment_file(source_for_seg, seg_dir)
        report["steps"]["segment"] = {"count": len(segs), "total_min": 0}
        if segs:
            total = sum(librosa.get_duration(path=s) for s in segs)
            report["steps"]["segment"]["total_min"] = round(total / 60, 1)

    # Sauvegarder le rapport
    report_path = DIR_REPORTS / f"{stem}_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    log(f"\nRapport sauvegardé : {report_path.name}")

    return report


def batch_process():
    """Traiter tous les fichiers prioritaires en séquence."""
    log("=== BATCH PROCESSING — Pipeline Goldberg ===")
    log(f"Fichiers prioritaires : {len(PRIORITY_FILES)}")
    reports = []
    for fname in PRIORITY_FILES:
        r = process_file(fname)
        reports.append(r)

    # Rapport global
    summary_path = DIR_REPORTS / "batch_summary.json"
    with open(summary_path, "w") as f:
        json.dump(reports, f, indent=2)

    total_segments = sum(
        r.get("steps", {}).get("segment", {}).get("count", 0) for r in reports
    )
    total_min = sum(
        r.get("steps", {}).get("segment", {}).get("total_min", 0) for r in reports
    )
    log(f"\n{'='*50}")
    log(f"BATCH TERMINÉ")
    log(f"Total segments : {total_segments}")
    log(f"Durée exploitable : {total_min:.0f} min")
    if total_min >= 60:
        log("✓ Suffisant pour Respeecher (>60 min)")
    elif total_min >= 30:
        log("✓ Suffisant pour ElevenLabs PVC (>30 min)")


if __name__ == "__main__":
    if "--batch" in sys.argv:
        batch_process()
    elif "--segment-only" in sys.argv:
        idx = sys.argv.index("--segment-only")
        f = Path(sys.argv[idx + 1])
        seg_dir = DIR_SEGMENTS / f.stem
        segment_file(f, seg_dir)
    elif len(sys.argv) > 1:
        process_file(sys.argv[1])
    else:
        print("Usage:")
        print("  python process_pipeline.py F260228_003_Mic12.wav")
        print("  python process_pipeline.py --batch")
        print("  python process_pipeline.py --segment-only processed/03-normalized/F260228_003_Mic12_norm.wav")
