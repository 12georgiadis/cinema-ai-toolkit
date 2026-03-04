# 11 - Archive

## Archive strategy

### What to keep
- **Camera originals**: always. Never delete source footage.
- **FCP Library**: the complete .fcpbundle with all projects/events
- **FCPXML exports**: XML representation of all project versions (lightweight, text-based)
- **Audio stems**: final mix, M&E, dialogue-only
- **Master exports**: ProRes 4444 archive master
- **Subtitle files**: all languages, all formats
- **Production documents**: scripts, treatments, contracts, releases (Obsidian vault + Notion export)
- **Stills**: hero images, press kit photos

### What you can delete (after delivery)
- Proxy media (can regenerate)
- Optimized media (can regenerate)
- Render files (can regenerate)
- Temp exports / review copies

## Storage

### Primary: NAS UGREEN iDX (64TB, 10GbE)
- All active and recent projects
- RAID for redundancy
- 10GbE for fast access

### Backup: QNAP TS-453BT3
- Mirror of completed projects
- Can be accessed via Thunderbolt 3 for fast restore

### Offsite
- Encrypted drives stored at separate location
- Or cloud backup for critical files (B2, Glacier)
- At minimum: one copy off-site for each completed film

## FCPXML as version control

### Why FCPXML matters
- FCPXML is the text representation of your FCP project
- It's XML -- human-readable, diffable, version-controllable
- You can track every edit decision in git

### Workflow
```bash
# Export FCPXML at every major version
# Store in git alongside your production documents
git add "Goldberg_v12_fine_cut.fcpxml"
git commit -m "Fine cut v12: restructured act 2, added archive sequence"

# Claude Code can diff FCPXML versions
claude "Compare these two FCPXML files and list all changes:
added/removed clips, moved clips, changed effects, timing changes." \
< <(diff old.fcpxml new.fcpxml)
```

### Capacitor (LateNite)
- Convert between FCPXML versions (v1.6 to v1.14)
- Essential for opening old projects in new FCP versions
- Or sharing with editors on different FCP versions

## Long-term preservation

### File format considerations
- ProRes 4444 is a safe archival format (Apple commitment, industry standard)
- Keep camera originals in their native format
- SRT/Fountain/Markdown: plain text, will always be readable
- Avoid proprietary-only formats for critical documents

### Metadata
- Embed metadata in files where possible (XMP, EXIF)
- Maintain a plain-text index of all project files
- Claude Code can generate a comprehensive archive manifest

```bash
# Generate archive manifest
claude "Create a detailed archive manifest for this film project.
List all files organized by category (source, project, exports, docs),
with file sizes, checksums, and descriptions."
```
