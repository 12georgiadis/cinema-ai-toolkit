# 03 - Production / Shoot

## On-set workflow

### Magic Lantern cameras
- RAW video recording (ML RAW, compressed RAW variants)
- Focus peaking, zebras, histogram, cropmarks
- No 30-minute recording limit
- Dual ISO on supported cameras
- **CAUTION**: Always test ML build on your specific camera model before a real shoot

### Audio
- Record audio separately when possible (higher quality, backup)
- Slate/clap for sync reference (even with timecode)
- Note any audio issues in Lumberjack or handwritten log

### Logging during shoot
- **Lumberjack System** on iPad: log interviews in real-time
- Mark selects, add keywords, rate moments
- At end of day: export FCPXML → ready for import into FCP

### Daily backup
- Card dump to portable SSD immediately after each card fills
- Verify checksum (xxHash via `xxhsum` or dedicated tools)
- **Never format a card until verified backup exists on 2 separate drives**

```bash
# Claude Code can generate verification scripts
# Example: verify all files copied correctly
find /Volumes/CARD -type f -exec xxhsum {} \; > card_checksums.txt
find /Volumes/BACKUP -type f -exec xxhsum {} \; > backup_checksums.txt
diff card_checksums.txt backup_checksums.txt
```

## Notes and metadata

### Shot notes
- Use a standard format: Scene/Setup/Take + notes
- Lumberjack handles this if used
- Otherwise: simple text file per day, Obsidian sync when back at base

### GPS and environment
- iPhone photos at each location (embedded GPS)
- Weather conditions, light direction, ambient sound notes
- All useful for post-production decisions and future reference

## End of day

1. All cards backed up and verified (2 copies minimum)
2. Lumberjack logs exported
3. Shot notes written up in Obsidian
4. Battery charging, equipment check for next day
5. Quick review of key moments (don't get lost watching everything)
