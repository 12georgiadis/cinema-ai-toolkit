# FCP Auteur Workflow

A-to-Z workflow for making auteur cinema (documentary, experimental, fiction) with Final Cut Pro, Claude Code, and open source tools.

**This is not a tutorial.** This is a living document showing how one filmmaker actually works -- hacking tools together, automating everything possible, and using AI as a creative collaborator, not just an assistant.

## Who is this for

- Independent filmmakers who want to push FCP beyond its defaults
- People curious about AI-assisted filmmaking workflows
- Anyone who thinks filmmaking tools should be open and hackable (Magic Lantern spirit)
- Claude Code users who want to see it applied to creative production

## Philosophy

1. **Hack everything.** If a tool doesn't do what you need, make it. Magic Lantern unlocked Canon cameras. CommandPost unlocks FCP. Claude Code unlocks your workflow.
2. **Local first.** Transcription, semantic search, color -- run it on your machine, not in a cloud. Privacy matters when you're making documentaries about sensitive subjects.
3. **Plain text is king.** Obsidian vaults, FCPXML, SRT files, Markdown scripts. Everything should be version-controlled and searchable.
4. **Automate the boring parts.** Renaming files, generating timelines, syncing metadata, creating proxies -- let the machine handle it so you can focus on the cut.

## Structure

```
workflow/           # A-to-Z pipeline: pre-prod → shoot → edit → grade → sound → deliver
plugins/            # Catalogue of every FCP plugin/tool with notes
claude-code/        # How Claude Code fits into a cinema workflow
obsidian/           # Obsidian vault setup for filmmaking (Fountain, logging, research)
scripts/            # Automation scripts (FCPXML manipulation, file management, etc.)
assets/             # Diagrams, screenshots
```

## The Stack

### Hardware
- Mac Mini M4 + Mac Studio M5 Ultra (summer 2026)
- 4x Windows workstations (RTX 5090/4090/3060) for rendering and AI
- 64TB NAS (UGREEN iDX) on 10GbE + QNAP backup
- Magic Lantern Canon cameras + open source cinema tools

### Software -- Editing
- **Final Cut Pro 12** (Jan 2026) -- Visual Search, Beat Detection, Transcript Search
- **CommandPost** -- automation, control surfaces, scripting
- **LateNite ecosystem** -- BRAW Toolbox, Gyroflow, Fast Collections, Marker Toolbox, LUT Robot
- **Lumberjack System** -- real-time documentary logging

### Software -- AI/Automation
- **Claude Code** -- FCPXML manipulation, script analysis, workflow automation, this doc
- **Whisper** (via Jojo Transcribe / MacWhisper) -- local transcription in 100+ languages
- **Jumper** -- semantic AI search in footage (offline)

### Software -- Organization
- **Obsidian** -- research vault, Fountain screenwriting, production bible
- **Notion** -- collaborative production management (via Marker Data bridge)
- **Kyno** -- media management and ingest

### Software -- Post
- **Color Finale 2 / Dehancer Pro / FilmConvert Nitrate** -- grading
- **iZotope RX** -- audio restoration
- **CrumplePop** -- quick audio fixes in FCP
- **X2Pro** -- FCP → Pro Tools roundtrip

## Current Projects

- "The Goldberg Variations" -- documentary (Villa Albertine 2026)
- "Virus" -- documentary on Mihai Ionut Paunescu

## Credits

Built by [Ismael Joffroy Chandoutis](https://ismaeljoffroychandoutis.com) with Claude Code (Opus 4.6).

Inspired by [Chris Hocking](https://github.com/latenitefilms) / [FCP Cafe](https://fcp.cafe) / the Magic Lantern community / everyone who hacks their tools to make better art.

## License

MIT
