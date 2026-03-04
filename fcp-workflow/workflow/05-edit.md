# 05 - Editing

## FCP 12 setup

### CommandPost configuration
- Install **CommandPost** (already done via `brew install --cask commandpost`)
- Grant Accessibility permissions
- Configure control surfaces:
  - **Stream Deck** for most-used actions
  - **Tangent panels** for color work
  - **TourBox** for scroll/jog
- Set up **Search Console** (global shortcut to trigger any FCP action)
- Explore **Lua scripting** for custom automations

### FCP 12 new features to leverage
- **Visual Search**: type natural language to find shots ("person walking on beach", "close-up of hands")
- **Transcript Search**: search spoken dialogue across ALL source clips
- **Beat Detection**: auto-detect music structure for cutting to music
- **Adjustment Clips**: apply effects to everything below (finally native)
- **Enhance Light and Color**: ML-based auto correction (good starting point before manual grade)

### Workspace
- Mac Mini M4: 3 screens (timeline, viewer, browser)
- Or MBP M5: 2 external + laptop (timeline, viewer on externals, browser on laptop)
- CommandPost manages workspace switching per task

## Assembly cut

### Strategy for documentary
1. Import Lumberjack logs (pre-rated, pre-keyworded)
2. Use **Fast Collections** to create Smart Collections by character/theme
3. Start with interview selects -- build the spoken narrative first
4. Layer B-roll, archive, graphics
5. Don't polish -- just get the structure

### Lumberjack Builder
- **Text-driven editing**: read transcripts, select passages, build timeline from text
- 3x faster than watching footage
- Perfect for interview-heavy documentaries
- Exports FCPXML → import into FCP

### Claude Code for assembly
```bash
# Analyze a transcript and suggest a narrative structure
claude "Here's the transcript of a 2-hour interview with [subject].
Identify the 10 strongest moments for a documentary about [theme].
For each moment, give me the timecode range and why it's important." \
< interview_transcript.srt
```

## Rough cut

### Marker-based feedback
- Export rough cut to **Frame.io** (native workflow extension)
- Collaborators leave timestamped comments
- **Marker Toolbox** imports Frame.io comments as FCP markers
- Also works with Vimeo, Wipster, Dropbox Replay, email

### Notion tracking
- **Marker Data** exports FCP markers to Notion database
- Track: which scenes are done, which need work, feedback status
- Notion views: Kanban board by status, timeline by sequence, table by character

### PostLab for collaboration
- If working with co-editor: **PostLab** for version control
- Project locking prevents conflicts
- Event sharing across editors
- Works like git for FCP libraries

## Fine cut

### Semantic search with Jumper
- **Jumper**: AI-powered footage search, 100% offline
- Natural language: "sunset over water", "person laughing", "archival footage"
- Finds shots you forgot you had
- Crucial for documentaries with hundreds of hours of footage

### Sound and music
- **Beat Detection** (FCP 12): analyze music tracks, snap cuts to beats
- **DAWBridge**: sync FCP timeline with Logic Pro for sound design
- Temp music placement, sound effects

### Roles
- Use FCP Roles extensively:
  - Video: Main, B-roll, Archive, Graphics, Titles
  - Audio: Dialogue, Ambience, Music, SFX, Voiceover
  - Roles enable → quick muting, separate exports, clear organization
