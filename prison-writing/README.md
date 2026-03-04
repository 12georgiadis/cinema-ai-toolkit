# prison-writing-analyzer

OCR + graphological analysis + data mining from photographs of handwritten documents and prison correspondence. Built for documentary research.

Processes HEIC / DNG / JPEG photos of letters, handwritten notes, typed mail, psychiatric reports, court documents — and outputs structured transcriptions, categorizations, and analysis.

---

## What it does

For each image in a folder (763 images, 400+ in a typical documentary research batch):

1. **Transcription** — Word-for-word OCR with illegibility markers and strikethrough detection
2. **Document classification** — Handwritten letter, prison email (JPay/CorrLinks), psychiatric report, legal document, personal note, envelope, etc.
3. **Graphological analysis** — Pressure, slant, letter size, regularity, legibility, free observations
4. **Data mining** — Persons named, locations, dates mentioned, themes, apparent emotional state
5. **Consolidated corpus** — Full transcription, categorization table, graphology report, data mining summary

Low-confidence images (< 70%) are automatically flagged for recheck with the Pro model.

---

## Model choice: Gemini 3 Flash Preview

### Why not a pure OCR tool?

The goal isn't just text extraction — it's understanding, categorizing, and analyzing simultaneously. Pure OCR tools (Tesseract, etc.) achieve ~64% accuracy on handwriting and can't do multi-task analysis in one pass.

### OCR benchmark — state of the art, March 2026

| Model | Handwriting | Complex docs | Cost | Notes |
|-------|-------------|-------------|------|-------|
| **Gemini 3 Flash** | ~90% | ★★★★★ | $0.50/1M tokens | #2 OCR Arena (ELO 1704, 80% win rate) |
| GPT-5 | ~90%+ | ★★★★★ | $$$ | Best pure handwriting, high cost |
| Gemini 2.5 Pro | ~90% | ★★★★★ | $$ | Slower, used for recheck pass |
| Mistral OCR 3 | 88.9% | ★★★★☆ | $1/1000 pages | Strong tables/formulas, −43% vs Gemini on complex parsing (LlamaIndex) |
| Google Document AI | ~85% | ★★★★☆ | $1.5–15/1000 pages | Complex setup |
| olmOCR-2-7B | 82.4% (benchmark) | ★★★★☆ | Free (local) | Allen Institute, open-source |
| Apple Vision | unquantified | ★★★☆☆ | Free (local) | Fast, no context understanding |
| PaddleOCR-VL-1.5 | 94.5% (OmniDocBench) | ★★★★☆ | Free (local, 0.9B) | Optimized for multilingual/Asian scripts |
| Tesseract | ~64% | ★★☆☆☆ | Free | Not suitable for handwriting |

**Sources:**
- [OCR Arena leaderboard](https://huggingface.co/spaces/echo840/ocrbench-leaderboard) (OCRBench v2, Feb 2026)
- [Mistral OCR vs Gemini — reducto.ai](https://reducto.ai/blog/lvm-ocr-accuracy-mistral-gemini)
- [Jerry Liu (LlamaIndex)](https://x.com/jerryjliu0/status/1898037050185859395) — Gemini outperforms Mistral on complex document parsing
- [olmOCR-2 — Allen Institute](https://arxiv.org/html/2510.19817v1)
- [PaddleOCR-VL-1.5](https://ernie.baidu.com/blog/posts/paddleocr-vl-1-5/)

### Two-pass architecture

- **Pass 1 — Gemini 3 Flash**: Fast, cheap, ~90% handwriting → processes all images
- **Pass 2 — Gemini 2.5 Pro**: Only low-confidence images (< 70%) → targeted recheck

Estimated cost for 763 images: **$2–5 total**.

---

## Requirements

```bash
pip install google-genai  # Python 3.10
# sips is macOS-native — no install needed for HEIC/DNG conversion
```

API key: `GEMINI_API_KEY` in environment or `~/.claude/secrets/opc-skills.env`

---

## Usage

```bash
# Test on 5 images
python prison_writing_analyzer.py /path/to/images/ --sample 5

# Process all images
python prison_writing_analyzer.py /path/to/images/

# Resume if interrupted
python prison_writing_analyzer.py /path/to/images/ --resume

# Recheck low-confidence images
python prison_writing_analyzer.py /path/to/images/ --recheck-only

# Rebuild corpus from existing JSON (no reprocessing)
python prison_writing_analyzer.py /path/to/images/ --consolidate

# Custom project context + output directory
python prison_writing_analyzer.py /path/to/images/ \
  --context-file contexts/my-project.json \
  --output-dir /path/to/output/
```

### Custom context (reusable for any project)

Create `contexts/my-project.json`:

```json
{
  "project": "Project name",
  "subject": "Subject name",
  "subject_description": "Description of the subject for Gemini context",
  "doc_types": ["handwritten_letter", "official_form", "personal_note", "report", "other"],
  "prompt_context": "Additional context to inject into the prompt (optional)"
}
```

---

## Output structure

```
output/
├── json/                    ← 1 JSON per image (OCR + metadata + graphology)
├── corpus/
│   ├── transcription_complete.md
│   ├── categorisation.md
│   ├── graphologie.md
│   └── data_mining.md       ← persons, places, themes, timeline
└── _temp_jpeg/              ← temp DNG/HEIC conversions (auto-cleaned)
```

### JSON format per image

```json
{
  "transcription": "...",
  "type_document": "lettre_manuscrite",
  "date_document": "2021-09-16",
  "destinataire": "...",
  "expediteur": "...",
  "medium": "stylo_bille",
  "support": "papier_ligne",
  "graphologie": {
    "pression": "moyenne",
    "inclinaison": "droite",
    "taille": "petite",
    "regularite": "irreguliere",
    "lisibilite": "moyenne",
    "observations": "..."
  },
  "personnes_citees": ["..."],
  "themes": ["..."],
  "etat_emotionnel": "anxieux",
  "contenu_notable": "...",
  "confidence_transcription": 0.85,
  "_meta": {
    "fichier": "IMG_4638.HEIC",
    "model_utilise": "gemini-3-flash-preview",
    "traite_le": "2026-03-02T...",
    "needs_recheck": false
  }
}
```

---

## Architecture

Two-pass pipeline, mirrors the [VHS Analyzer](https://github.com/yourusername/vhs-analyzer) architecture:
- Progress tracking (resume after interruption)
- Exponential retry (15s / 45s / 120s)
- Flash pass + Pro recheck for difficult images
- Automatic corpus consolidation at end of batch

---

## License

MIT — built for documentary research, reusable for any corpus of photographed documents.
