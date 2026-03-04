# 10 - Delivery

## Export from FCP

### Compressor
- Included with Creator Studio subscription
- Custom presets for every delivery format
- Batch processing
- Distributed encoding across multiple Macs

### Common delivery formats

| Destination | Format | Resolution | Codec | Audio |
|-------------|--------|------------|-------|-------|
| Festival DCP | JPEG 2000 | 2K/4K Flat/Scope | J2K | PCM 24bit 48kHz |
| Theatrical | ProRes 4444 XQ | 4K | ProRes | PCM 24bit 48kHz |
| Broadcast (France) | ProRes 422 HQ | HD 1080i/p | ProRes | PCM 16bit 48kHz |
| Web (YouTube/Vimeo) | H.264/H.265 | 4K or 1080p | HEVC preferred | AAC 320kbps |
| Streaming (Netflix etc.) | IMF package | 4K HDR | Various | 5.1/7.1/Atmos |
| Archive master | ProRes 4444 | Native resolution | ProRes | PCM 24bit 96kHz |

### DCP creation
- **DCP-o-matic**: free, open source DCP creation
- Or use professional service (Le Labo, Eclair, etc.)
- Test DCP on actual cinema projector before festival submission

## Subtitle delivery
- **Burn-in** for web/social: export with captions baked in
- **Separate file** for broadcast/festival: SRT, iTT, or CEA-608
- Multiple language versions: export with different caption roles enabled

## Quality control

### Before delivery
- Watch the entire film on a calibrated monitor
- Check audio levels (EBU R128 for broadcast, -14 LUFS for streaming)
- Verify subtitles timing and spelling
- Check first/last frames (no flash frames, proper fade to black)
- Color accuracy on reference monitor

### Claude Code for QC
```bash
# Analyze export file metadata
ffprobe -v quiet -print_format json -show_format -show_streams output.mov

# Claude Code can parse ffprobe output and flag issues
claude "Analyze this ffprobe output. Check if it meets broadcast specs:
1920x1080, ProRes 422 HQ, 25fps, audio 48kHz 24bit stereo,
loudness target -23 LUFS. Flag any issues." < ffprobe_output.json
```

## Festival submission

### Workflow
1. Export master ProRes 4444
2. Create DCP with DCP-o-matic (or service)
3. Generate screening copies: H.264 1080p with burn-in subtitles
4. Prepare press kit: stills (from Marker Data exports), synopsis, director's statement
5. Submit via FilmFreeway, Shortfilmdepot, or direct

### Marker Data for press kit
- Export stills from FCP markers to Notion
- Select best frames for press photos
- Generate PDF lookbooks with Pagemaker
