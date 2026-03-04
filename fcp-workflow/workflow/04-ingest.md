# 04 - Ingest

## Media management with Kyno

### What Kyno does
- Preview any format without transcoding
- Batch rename with metadata-based rules
- Add metadata, keywords, ratings before import
- Transcode/proxy generation
- Search across drives
- Works on Mac and Windows

### Ingest workflow
1. Open Kyno, point to backup drive
2. Review and tag footage (star ratings, keywords, color labels)
3. Batch rename with consistent scheme: `PROJECT_DATE_CAMERA_CLIP.ext`
4. Generate proxies if needed (ProRes Proxy or H.264)
5. Export metadata as CSV/sidecar for reference

### Claude Code for renaming
```bash
# Generate rename rules based on your project naming convention
# Claude Code can write custom rename scripts that Kyno can't handle

# Example: extract date from EXIF, combine with camera serial
python rename_rushes.py --pattern "{date}_{camera}_{sequence:04d}" --input /Volumes/RUSHES/
```

## FCP Library setup

### Structure
```
PROJECT_NAME.fcpbundle/
├── Event: 01_Interviews/
│   ├── Smart Collection: Selects
│   ├── Smart Collection: By Character
│   └── Keyword Collections from Lumberjack
├── Event: 02_Broll/
├── Event: 03_Archive/
├── Event: 04_Audio/
├── Event: 05_Graphics/
└── Project: Assembly_v01
```

### Import strategy
- Import Lumberjack FCPXML first (pre-logged, pre-keyworded)
- Import remaining footage with "Leave files in place" (no copying)
- Apply Camera LUTs automatically with **LUT Robot**
- Generate optimized media for edit machine, proxies for laptop

### Keyword taxonomy
Define before import. Example for documentary:
- Character names (JOSHUA, ANNA, DETECTIVE, etc.)
- Themes (RADICALIZATION, IDENTITY, INTERNET, FAMILY)
- Type (INTERVIEW, BROLL, ARCHIVE, REENACTMENT, SCREEN_CAPTURE)
- Quality (SELECT, MAYBE, TECHNICAL_ISSUE)
- Location (PARIS, FLORIDA, ONLINE)

Use **Fast Collections** to generate Smart Collections from keyword lists instantly.

## Backup and NAS

### NAS workflow
- Primary: UGREEN iDX NAS (64TB, 10GbE) -- all media lives here
- Backup: QNAP TS-453BT3 -- mirror of critical data
- FCP Library on local SSD for speed, media referenced on NAS
- Thunderbolt 3 direct connection for high-bandwidth transfers

### Proxy workflow for mobile editing
- Generate ProRes Proxy (1/4 resolution) for all media
- Store proxies on laptop SSD
- Edit on MBA M3 / MBP M5 with UGREEN Revodok dock
- Reconnect to full-res media on NAS when back at atelier

## Analog archive AI analysis (VHS, Hi8, miniDV)

For documentary projects working with analog archives, there's a dedicated pipeline
to semantically analyze footage with Gemini and export colored markers directly to FCP12.

**→ [vhs-ai-pipeline](https://github.com/12georgiadis/vhs-ai-pipeline)**

What it does:
- Creates 480p 1fps proxies with burned-in timecodes (ffmpeg)
- Sends footage to Gemini via Files API (temporary -- deleted after each call)
- Two-pass analysis: blind pass (no framework) + targeted pass (your analytical grid)
- Exports FCPXML with colored markers → import directly into FCP12
- Generates a Markdown rush log per video

Cost: ~$15-22 for 12 hours of footage. No footage stored in the cloud.

Integrates with Jumper: marker notes contain the full Gemini interpretation,
so Jumper can search across all analyzed footage by concept.
