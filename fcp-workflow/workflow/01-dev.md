# 01 - Development

## Research

### Obsidian as research vault
- All research notes in Obsidian vault (see `obsidian/setup.md`)
- **Media Extended** plugin: watch reference films directly in Obsidian, timestamp notes
- **Dataview** plugin: query your notes like a database (all interviews by date, all locations by country, etc.)
- Graph view reveals unexpected connections between subjects

### Claude Code for research
- Web search for background on subjects, legal context, historical facts
- Summarize long documents (court transcripts, leaked chats, news archives)
- Cross-reference multiple sources to build a factual timeline
- Generate research questions you hadn't thought of

## Writing

### Screenwriting in Obsidian
- **Fountain Editor** plugin: write in Fountain format directly in Obsidian
- **Fountain Screenwriter** plugin: proper page layout (78 chars, like Final Draft)
- **Fountain Support** plugin: index cards, rehearsal mode, scene TOC
- **Longform** plugin: compile scenes into a full manuscript
- All Fountain files are plain text → version controlled with git

### Documentary treatment
- Write treatments in Markdown
- Claude Code can help structure narrative arcs, identify gaps, suggest interview questions
- Keep multiple versions, compare with git diff

### Script analysis with Claude Code
```bash
# Example: analyze a Fountain screenplay
claude "Read this script and identify: 1) all characters and their arc,
2) thematic patterns, 3) structural issues, 4) documentary sequences
vs staged sequences" < script.fountain
```

## Storyboarding

### AI-assisted visualization
- Use image generation (DALL-E, Gemini) to create rough storyboards from descriptions
- Not for final art -- for communicating shots to crew
- Claude Code can batch-generate storyboard prompts from a shot list

### Storyclock
- **Storyclock Viewer** Obsidian plugin: circular narrative visualization
- Map story beats visually, identify pacing issues early

## Production Bible

### Notion for collaboration
- Share the production bible with producers, co-directors, crew
- Templates: [Filmmaking Base Camp](https://notion4film.gumroad.com/l/fixob)
- Call sheets, equipment lists, location scouting, contact database

### Obsidian for personal reference
- Mirror key info from Notion into Obsidian for offline/fast access
- Interlink everything: character notes ↔ interview transcripts ↔ location photos ↔ legal docs
