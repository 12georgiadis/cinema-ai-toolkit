# How Claude Code Fits Into a Cinema Workflow

This is not theoretical. This is how we actually use Claude Code in filmmaking production.

## The Big Picture

Claude Code is not a video editor. It can't watch your footage or listen to your audio. What it CAN do is manipulate everything around the creative decisions:

- **Text files**: scripts, treatments, FCPXML, SRT subtitles, metadata, CSV, JSON
- **Automation**: rename files, generate timelines, batch operations, build tools
- **Research**: find information, cross-reference sources, analyze documents
- **Code**: write scripts, build web tools, create visualizations
- **Organization**: structure vaults, generate documentation, maintain production bibles

The creative decisions remain yours. Claude Code removes friction so you can make more of them.

---

## Phase-by-Phase Integration

### 1. Development / Research

**What Claude Code does:**
- Web research on subjects, legal context, historical background
- Summarize long documents (court records, leaked documents, news archives)
- Build factual timelines from multiple sources
- Draft interview questions based on research
- Analyze reference films and extract structural patterns

**Real example:**
```bash
# Research a documentary subject
claude "Research Joshua Ryne Goldberg. Compile a factual timeline
from court documents, news reports, and academic papers.
Flag any contradictions between sources."
```

### 2. Writing

**What Claude Code does:**
- Help structure narrative arcs (acts, sequences, beats)
- Analyze Fountain screenplays for structural issues
- Generate alternative scene orderings
- Translate scripts between languages
- Format and clean up interview transcripts into usable script form

**Real example:**
```bash
# Analyze script structure
claude "Read this Fountain script for a documentary.
Identify: 1) the narrative throughline, 2) where the argument
is weakest, 3) what's missing from the story, 4) suggested
restructuring." < treatment.fountain
```

### 3. Pre-production

**What Claude Code does:**
- Generate equipment lists from location requirements
- Draft contracts, releases, permit applications from templates
- Create call sheet templates in Notion format
- Build keyword taxonomies for logging
- Set up Obsidian vault structure for the project

### 4. Ingest / Organization

**What Claude Code does:**
- Write custom rename scripts (Kyno can't handle every naming convention)
- Generate FCPXML with pre-built keyword structures
- Parse and clean up Lumberjack exports
- Create Smart Collection definitions from keyword lists
- Build checksum verification scripts for backup integrity

**Real example:**
```bash
# Batch rename rushes with intelligent pattern
claude "Write a Python script that renames video files using this pattern:
{project}_{date from EXIF}_{camera serial}_{sequence:04d}.{ext}
Handle: .mov, .mp4, .braw, .mlv files.
Skip files that already match the pattern."
```

### 5. Editing

**What Claude Code does:**
- Analyze transcripts to suggest narrative structure
- Generate paper edits from transcript analysis
- Manipulate FCPXML directly (move clips, change timing, batch modify metadata)
- Create timeline comparison reports between versions
- Generate string-outs from keyword-tagged transcripts

**Real example:**
```bash
# Generate a paper edit from interview transcripts
claude "Here are transcripts from 5 interviews about radicalization.
Create a paper edit for a 15-minute sequence that covers:
1) How it started, 2) The escalation, 3) The consequences.
For each selected passage, give timecode and the interviewee's name.
Output as an EDL or FCPXML." < all_transcripts.txt
```

### 6. FCPXML Manipulation

This is Claude Code's superpower for FCP workflows. FCPXML is just XML, and Claude Code can read, modify, and generate it.

**What's possible:**
- Reorder clips in a timeline programmatically
- Batch apply keywords to clips matching criteria
- Extract all markers and their metadata
- Generate timelines from spreadsheets or databases
- Compare two versions of a project and list all changes
- Convert between FCPXML versions (or use Capacitor)

**Real example:**
```bash
# Diff two FCPXML versions
claude "Compare these two FCPXML files. For each difference, tell me:
- What changed (clip added/removed/moved, effect changed, timing changed)
- The timecode of the change
- A human-readable description of what happened
Output as a markdown table." \
< <(diff -u v11.fcpxml v12.fcpxml)
```

### 7. Transcription & Subtitles

**What Claude Code does:**
- Post-process Whisper transcriptions (fix names, technical terms, punctuation)
- Translate subtitles with context awareness (not just word-for-word)
- Reformat SRT files (merge short lines, adjust timing, fix encoding)
- Generate subtitle files from transcript + timecode data
- QC subtitles (check timing, reading speed, line length)

**Real example:**
```bash
# QC subtitles
claude "Check this SRT file for issues:
1) Lines over 42 characters (broadcast limit)
2) Display time under 1 second or over 7 seconds
3) Reading speed over 200 words per minute
4) Overlapping timecodes
5) Common OCR/ASR errors
Output a report with line numbers." < subtitles.srt
```

### 8. Color / Sound

**What Claude Code does:**
- Generate LUT application scripts
- Analyze ffprobe output for QC
- Build ffmpeg commands for specific conversion needs
- Parse audio loudness reports and flag compliance issues
- Generate Compressor presets from specifications

### 9. Delivery

**What Claude Code does:**
- Verify export meets delivery specs (resolution, codec, audio, loudness)
- Generate DCP packaging scripts
- Build ffmpeg encode commands for specific platforms
- Create archive manifests with checksums
- Generate press kit materials from FCP marker exports

**Real example:**
```bash
# Verify broadcast delivery specs
ffprobe -v quiet -print_format json -show_format -show_streams master.mov | \
claude "Check if this file meets CSA/France broadcast specs:
- 1920x1080, 25fps interlaced or progressive
- ProRes 422 HQ or higher
- Audio: 48kHz, 24bit, stereo or 5.1
- EBU R128 loudness (-23 LUFS)
Flag any issues."
```

### 10. Meta / Workflow

**What Claude Code does:**
- Maintain this very documentation
- Build custom tools and scripts as needs emerge
- Create visualizations of project data (D3.js, Mermaid)
- Set up and manage the Obsidian vault
- Interface with Notion via MCP server
- Generate reports from production data

---

## What Claude Code CANNOT Do (Yet)

- Watch video or listen to audio directly
- Make creative editing decisions (it can suggest, based on transcripts/metadata)
- Replace a colorist's eye (it can set up technical parameters)
- Mix audio (it can prepare files and check specs)
- Use FCP's GUI (no screen control, only file manipulation)

## What Changes With Each Model Upgrade

As LLMs get better at processing longer contexts and multimedia:
- Longer FCPXML files can be analyzed in full
- More complex timeline manipulations become possible
- Eventually: direct video/audio analysis will remove the "transcript intermediary" step
- Voice mode could enable dictating edit notes that Claude Code executes as FCPXML changes

## The Philosophy

The filmmaker makes the creative decisions. Claude Code handles everything that isn't a creative decision. The goal is to spend 90% of your time in the timeline making choices about story, rhythm, and emotion -- and 0% on file management, format conversion, metadata entry, or googling ffmpeg flags.
