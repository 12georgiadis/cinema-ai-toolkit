#!/usr/bin/env python3
"""
Analyse audio pour préparation voice cloning.
Usage: python analyze_audio.py <fichier.wav> [--output /chemin/rapport]
"""

import sys
import os
import numpy as np
import librosa
import librosa.display
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path

def analyze_file(audio_path, output_dir=None, duration_limit=300):
    """Analyse complète d'un fichier audio — spectrogram, bruit, qualité."""
    path = Path(audio_path)
    if output_dir is None:
        output_dir = path.parent / "analysis"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== ANALYSE : {path.name} ===")

    # Charger (limité à duration_limit secondes pour les gros fichiers)
    y, sr = librosa.load(audio_path, sr=16000, mono=True, duration=duration_limit)
    duration = len(y) / sr
    print(f"Durée analysée : {duration:.1f}s / sr={sr}Hz")

    # --- Métriques globales ---
    rms_global = np.sqrt(np.mean(y**2))
    rms_db = 20 * np.log10(rms_global + 1e-9)

    # Estimation du plancher de bruit (percentile bas du RMS par frames)
    frame_length = 2048
    hop_length = 512
    rms_frames = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    rms_frames_db = 20 * np.log10(rms_frames + 1e-9)
    noise_floor_db = float(np.percentile(rms_frames_db, 10))
    signal_peak_db = float(np.percentile(rms_frames_db, 90))
    snr_estimate = signal_peak_db - noise_floor_db

    print(f"Niveau moyen     : {rms_db:.1f} dBFS")
    print(f"Plancher bruit   : {noise_floor_db:.1f} dBFS")
    print(f"Pic voix (p90)   : {signal_peak_db:.1f} dBFS")
    print(f"SNR estimé       : {snr_estimate:.1f} dB", end="  ")
    if snr_estimate > 25:
        print("✓ EXCELLENT (>25dB)")
    elif snr_estimate > 15:
        print("~ BON (15-25dB)")
    elif snr_estimate > 8:
        print("⚠ MOYEN (8-15dB) — à traiter")
    else:
        print("✗ DÉGRADÉ (<8dB) — traitement urgent")

    # --- Détection bruit basse fréquence (frigo/compresseur) ---
    # Le compresseur de frigo = hum 50/60Hz + harmoniques
    # On analyse l'énergie dans 40-120Hz vs 200-3000Hz
    stft = np.abs(librosa.stft(y, n_fft=4096, hop_length=hop_length))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=4096)

    low_bins = np.where((freqs >= 40) & (freqs <= 120))[0]
    voice_bins = np.where((freqs >= 200) & (freqs <= 3000))[0]

    low_energy = stft[low_bins, :].mean(axis=0)
    voice_energy = stft[voice_bins, :].mean(axis=0)

    # Frames où le bruit bas fréquence est élevé SANS voix = candidats frigo
    silence_mask = rms_frames < np.percentile(rms_frames, 30)
    low_noise_ratio = low_energy / (voice_energy + 1e-9)

    fridge_events = []
    times = librosa.frames_to_time(np.arange(len(rms_frames)), sr=sr, hop_length=hop_length)
    in_event = False
    event_start = 0
    threshold = np.percentile(low_noise_ratio, 80)

    for i, (t, ratio, is_silence) in enumerate(zip(times, low_noise_ratio, silence_mask)):
        if is_silence and ratio > threshold:
            if not in_event:
                in_event = True
                event_start = t
        else:
            if in_event:
                duration_event = t - event_start
                if duration_event > 1.0:  # ignorer les events < 1 sec
                    fridge_events.append((event_start, t, duration_event))
                in_event = False

    if fridge_events:
        print(f"\nBruit basse fréquence détecté : {len(fridge_events)} événement(s)")
        for start, end, dur in fridge_events[:10]:
            print(f"  {start:.1f}s → {end:.1f}s  ({dur:.1f}s)")
        if len(fridge_events) > 10:
            print(f"  ... + {len(fridge_events)-10} autres")
    else:
        print("\nAucun bruit basse fréquence détecté.")

    # --- Segments de bonne qualité (candidats pour le voice cloning) ---
    # Critères : voix présente + SNR local > seuil
    rms_normalized = rms_frames / (rms_frames.max() + 1e-9)
    voice_active = rms_normalized > 0.1
    local_snr = rms_frames_db - noise_floor_db

    good_segments = []
    in_good = False
    seg_start = 0
    min_seg_duration = 5.0
    max_seg_duration = 30.0

    for i, (t, active, lsnr) in enumerate(zip(times, voice_active, local_snr)):
        if active and lsnr > 12:
            if not in_good:
                in_good = True
                seg_start = t
        else:
            if in_good:
                dur = t - seg_start
                if min_seg_duration <= dur <= max_seg_duration:
                    good_segments.append((seg_start, t, dur))
                elif dur > max_seg_duration:
                    # Découper en sous-segments
                    n = int(dur // max_seg_duration)
                    for j in range(n):
                        good_segments.append((seg_start + j*max_seg_duration,
                                             seg_start + (j+1)*max_seg_duration,
                                             max_seg_duration))
                in_good = False

    print(f"\nSegments voix propre (5-30s) : {len(good_segments)} trouvés")
    total_clean = sum(d for _, _, d in good_segments)
    print(f"Durée totale exploitable     : {total_clean:.0f}s ({total_clean/60:.1f} min)")
    if total_clean > 1800:
        print("✓ Suffisant pour Respeecher (>30 min)")
    elif total_clean > 600:
        print("✓ Suffisant pour ElevenLabs PVC (>10 min)")
    else:
        print("⚠ Insuffisant — besoin de plus de matériau")

    # --- FIGURE : spectrogramme + RMS + énergie basse fréq ---
    fig = plt.figure(figsize=(18, 10))
    fig.patch.set_facecolor('#0d1117')
    gs = gridspec.GridSpec(3, 1, height_ratios=[3, 1, 1], hspace=0.4)

    # Spectrogramme mel
    ax1 = fig.add_subplot(gs[0])
    D = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128), ref=np.max)
    librosa.display.specshow(D, sr=sr, hop_length=hop_length, x_axis='time', y_axis='mel',
                             ax=ax1, cmap='magma')
    ax1.set_facecolor('#0d1117')
    ax1.set_title(f'{path.name} — Spectrogramme Mel', color='white', fontsize=11, pad=8)
    ax1.tick_params(colors='#888', labelsize=8)
    ax1.set_xlabel('')
    ax1.spines[:].set_color('#333')
    # Marquer les événements frigo
    for start, end, _ in fridge_events:
        ax1.axvspan(start, end, alpha=0.25, color='cyan', label='frigo' if start == fridge_events[0][0] else '')
    if fridge_events:
        ax1.legend(loc='upper right', fontsize=8, facecolor='#1a1a2e', labelcolor='cyan')

    # Niveau RMS
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor('#0d1117')
    ax2.plot(times[:len(rms_frames_db)], rms_frames_db, color='#58a6ff', linewidth=0.8, alpha=0.9)
    ax2.axhline(noise_floor_db, color='red', linewidth=0.8, linestyle='--', alpha=0.7, label=f'noise floor {noise_floor_db:.0f}dB')
    ax2.axhline(signal_peak_db, color='#3fb950', linewidth=0.8, linestyle='--', alpha=0.7, label=f'voix p90 {signal_peak_db:.0f}dB')
    ax2.set_ylabel('dBFS', color='#888', fontsize=8)
    ax2.set_title(f'Niveau RMS  |  SNR ≈ {snr_estimate:.0f}dB', color='white', fontsize=9, pad=4)
    ax2.tick_params(colors='#888', labelsize=7)
    ax2.legend(loc='upper right', fontsize=7, facecolor='#1a1a2e', labelcolor='white')
    ax2.spines[:].set_color('#333')
    for start, end, _ in fridge_events:
        ax2.axvspan(start, end, alpha=0.2, color='cyan')

    # Ratio bruit bas / voix (indicateur frigo)
    ax3 = fig.add_subplot(gs[2])
    ax3.set_facecolor('#0d1117')
    ax3.plot(times[:len(low_noise_ratio)], low_noise_ratio, color='#f85149', linewidth=0.8, alpha=0.9)
    ax3.axhline(threshold, color='cyan', linewidth=0.8, linestyle='--', alpha=0.7, label='seuil détection')
    ax3.set_ylabel('ratio', color='#888', fontsize=8)
    ax3.set_xlabel('Temps (s)', color='#888', fontsize=8)
    ax3.set_title('Énergie basse fréquence 40-120Hz (rouge = potentiel frigo/hum)', color='white', fontsize=9, pad=4)
    ax3.tick_params(colors='#888', labelsize=7)
    ax3.legend(loc='upper right', fontsize=7, facecolor='#1a1a2e', labelcolor='white')
    ax3.spines[:].set_color('#333')

    out_img = output_dir / f"{path.stem}_analysis.png"
    plt.savefig(out_img, dpi=120, bbox_inches='tight', facecolor='#0d1117')
    plt.close()
    print(f"\nImage sauvegardée : {out_img}")

    # --- Rapport texte ---
    report = {
        "file": str(path.name),
        "duration_analyzed_s": round(duration, 1),
        "rms_db": round(rms_db, 1),
        "noise_floor_db": round(noise_floor_db, 1),
        "signal_peak_db": round(signal_peak_db, 1),
        "snr_estimate_db": round(snr_estimate, 1),
        "fridge_events": len(fridge_events),
        "fridge_events_detail": [(round(s,1), round(e,1)) for s,e,_ in fridge_events[:20]],
        "good_segments_count": len(good_segments),
        "good_segments_total_s": round(total_clean, 0),
    }

    return report, str(out_img)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Analyse tous les WAV du dossier courant
        target = Path(".")
        files = sorted(target.glob("*.wav")) + sorted(target.glob("*.mp3"))
        if not files:
            print("Usage: python analyze_audio.py <fichier.wav|mp3> [--limit N]")
            sys.exit(1)
    else:
        files = [Path(sys.argv[1])]

    limit = 300  # 5 min par défaut pour aller vite
    if "--limit" in sys.argv:
        idx = sys.argv.index("--limit")
        limit = int(sys.argv[idx+1])

    for f in files:
        if f.exists():
            analyze_file(f, duration_limit=limit)
        else:
            print(f"Fichier non trouvé : {f}")
