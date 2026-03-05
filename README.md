<p align="center">
  <img src="header-banner.jpg" alt="Cinema AI Toolkit" width="100%"/>
</p>

# Cinema AI Toolkit

**Documentary filmmaker's AI toolkit — voice repair, VHS analysis, FCP workflows, OCR, FCPXML generation, narrative visualization.**

Built for real productions, not demos.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Gemini](https://img.shields.io/badge/Gemini_3_Flash-API-4285F4?style=flat-square&logo=google)
![Final Cut Pro](https://img.shields.io/badge/Final_Cut_Pro-12-purple?style=flat-square)

---

## Author

[Ismaël Joffroy Chandoutis](https://ismaeljoffroychandoutis.com) — filmmaker and artist. **César 2022**, Cannes, IDFA, Hot Docs, Ars Electronica.

These tools were built during active production of feature documentaries. They solve problems I actually have.

---

## What's inside

Six independent tools, one repo. Each has its own README with full documentation.

```
cinema-ai-toolkit/
├── voice-pipeline/       # Voice repair for documentary subjects
├── vhs-pipeline/         # VHS/Hi8/miniDV analysis with Gemini → FCP markers
├── fcp-workflow/          # Final Cut Pro auteur workflow + Claude Code integration
├── prison-writing/       # OCR + graphological analysis for handwritten documents
├── fcpxml-generator/     # Generate FCPXML 1.11 timelines from JSON structure
├── d3-documentary-visu/  # D3.js relationship maps + emotion curves
└── ETHICS.md             # Ethics statement for documentary AI tools
```

---

## Tools

### [Voice Pipeline](voice-pipeline/)

Voice direction for documentary filmmakers working with non-professional subjects. The subject's voice is authentic and irreplaceable — this pipeline repairs the performance, not the voice.

```
RAW RECORDINGS → Denoise → Isolate → Diarize → Segment → Normalize
                          → Enhance → Inpaint → Fix delivery → Voice clone ready
```

**Stack:** DeepFilterNet 3, Resemble Enhance, ElevenLabs, Sesame CSM, Chatterbox

---

### [VHS Pipeline](vhs-pipeline/)

Analyze hours of analog archive footage (VHS, Hi8, miniDV, Super8) with Gemini. Export colored markers directly to Final Cut Pro 12.

```
Archive footage → ffmpeg proxy → Gemini analysis → FCPXML colored markers → FCP 12
```

| Marker Color | Meaning |
|------|---------|
| Red | Strong interest — must review |
| Orange | Narrative structure moment |
| Blue | Standard marker |
| Green | Glitch / artifact |

**Stack:** Gemini 3 Flash, ffmpeg, FCPXML

---

### [FCP Workflow](fcp-workflow/)

A-to-Z workflow for auteur cinema with Final Cut Pro, Claude Code, and open source tools.

**Philosophy:** Hack everything. Local first. Plain text is king. Automate the boring parts.

---

### [Prison Writing Analyzer](prison-writing/)

OCR + graphological analysis + data mining from photographs of handwritten documents and prison correspondence. Built for documentary research.

For each image:
1. **Transcription** — word-for-word OCR with illegibility markers
2. **Classification** — letter, prison email, psychiatric report, legal document...
3. **Graphological analysis** — pressure, slant, regularity, legibility
4. **Data mining** — persons, locations, dates, themes, emotional state

**Stack:** Gemini 3 Flash (primary) + Gemini 2.5 Pro (recheck low-confidence)

| Model | Handwriting accuracy | Cost |
|-------|---------------------|------|
| Gemini 3 Flash | ~90% | $0.50/1M tokens |
| GPT-5 | ~90%+ | $$$ |
| Tesseract (local) | ~64% | Free |

---

### [FCPXML Generator](fcpxml-generator/)

Generate valid FCPXML 1.11 timelines from structured JSON. Push your narrative architecture (acts, sequences, markers) directly into Final Cut Pro without manual rebuilding.

```
JSON structure → Python CLI → FCPXML 1.11 → FCP 12
```

**Stack:** Python 3.10+, stdlib only (no dependencies)

---

### [D3.js Documentary Visualizations](d3-documentary-visu/)

Self-contained HTML visualizations for documentary development. Two types:

- **Relationship Map** — Force-directed graph (Lombardi-style) of character interconnections
- **Emotion Curve** — Multi-layer temporal visualization of narrative arcs

Both output standalone HTML files. Dark theme, interactive, no server needed.

**Stack:** D3.js v7, vanilla HTML/CSS/JS

---

## Ethics

All tools in this repo follow the ethics statement in [ETHICS.md](ETHICS.md). Documentary AI tools operate on real people's lives. The technology is never neutral.

---

## Install

Each tool has its own requirements. See the README in each directory.

```bash
# Voice pipeline
cd voice-pipeline && pip install -r requirements.txt

# VHS pipeline
cd vhs-pipeline && pip install -r requirements.txt
```

---

**Consolidated from:** [cinema-voice-pipeline](https://github.com/12georgiadis/cinema-voice-pipeline) · [vhs-ai-pipeline](https://github.com/12georgiadis/vhs-ai-pipeline) · [fcp-auteur-workflow](https://github.com/12georgiadis/fcp-auteur-workflow) · [prison-writing-analyzer](https://github.com/12georgiadis/prison-writing-analyzer)
