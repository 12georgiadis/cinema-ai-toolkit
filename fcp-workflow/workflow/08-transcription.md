# 08 - Transcription, Subtitles, Captions

## The shift to local AI transcription

As of 2025-2026, **Whisper-based local transcription** has replaced cloud services for most workflows. It's free, private, multilingual, and runs on Apple Silicon.

## FCP 12 built-in transcription

### Transcript Search (NEW)
- Search spoken dialogue across ALL source clips (not just timeline)
- Apple Silicon required
- **English only** for Transcribe to Captions
- Useful but limited for multilingual documentary work

## Recommended tools

### Jojo Transcribe (FREE - App Store)
- Whisper V2/V3 Turbo models
- **100+ languages**
- Translation to English built-in
- Standalone macOS app, works with any NLE
- Export: SRT, VTT, TXT, CSV, JSON
- **Best free option**

### MacWhisper
- Freemium (free for basic, paid for large models)
- Transcribe AND translate simultaneously
- Export SRT directly
- Good UI for reviewing/correcting transcriptions

### Captionator (App Store)
- Whisper Large v3 Turbo
- **Animated captions** (YouTube/TikTok style, per-word keyframing)
- Good for social media cuts of documentary material

### mCaptionsAI (MotionVFX)
- 90+ languages
- Import SRT, generates FCP captions
- 26+ visual styles
- FCP plugin (not standalone)

### Whisper Auto Captions (Open Source)
- [GitHub](https://github.com/shaishaicookie/fcpx-auto-captions)
- Based on whisper.cpp
- Free, hackable
- For those who want full control

## Multilingual workflow

Documentary often involves multiple languages. Here's the workflow:

1. **Transcribe** in source language (Jojo Transcribe or MacWhisper)
2. **Translate** to target language (built-in Jojo feature, or Claude Code for nuanced translation)
3. **Generate SRT** files: one per language
4. **Import into FCP**: File > Import > Captions
5. Each SRT becomes a separate audio role in Timeline Index
6. **Switch** between subtitle tracks for different distribution versions

### Claude Code for translation refinement
```bash
# Refine auto-translated subtitles with context
claude "Here is an SRT file auto-translated from Romanian to French.
The subject is a hacker discussing his crimes. Refine the translation
for naturalness, keeping technical terms accurate. The tone should be
documentary, not literary." < subtitles_auto_fr.srt > subtitles_refined_fr.srt
```

## Supported formats
- **SRT** (SubRip): universal, simple, most compatible
- **iTT** (iTunes Timed Text): Apple's format, richer styling
- **CEA-608**: broadcast closed captions
- FCP handles all three natively

## Subtitling workflow

1. Transcribe with Jojo/MacWhisper
2. Clean up in MacWhisper or text editor (timing adjustments, typo fixes)
3. Claude Code for batch corrections if needed
4. Import SRT into FCP
5. Style captions in FCP (font, size, position, background)
6. For animated captions: use Captionator or mCaptionsAI
7. Export: burn-in for web, separate file for broadcast
