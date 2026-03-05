# FCPXML Generator

**Python CLI for generating valid FCPXML 1.11 timelines from structured data.**

Produces FCP-ready timelines with title clips, markers, chapters, gaps, and compound clips — from JSON or programmatic input.

## Why

When your film structure lives in markdown/JSON (bible, treatment, storyform), you want to push it into FCP without manual rebuilding. This tool bridges narrative architecture and editing timeline.

## Usage

```bash
# Generate from JSON structure
python fcpxml-generator.py --from-json structure.json --output timeline.fcpxml

# Print the expected JSON schema
python fcpxml-generator.py --schema
```

### JSON Input Schema

```json
{
  "project_name": "My Film",
  "fps": 24,
  "sequences": [
    {
      "title": "Act 1 — Opening",
      "type": "title",
      "duration_seconds": 120,
      "markers": [
        { "name": "Key moment", "offset_seconds": 30, "type": "chapter" }
      ]
    },
    {
      "title": "Interview A",
      "type": "gap",
      "duration_seconds": 300,
      "markers": []
    }
  ]
}
```

### Output

Valid FCPXML 1.11 with:
- `<fcpxml version="1.11">` root
- Proper `<resources>` with format and effect declarations
- `<spine>` containing title clips (with text overlay) and gap clips
- Chapter markers and to-do markers on clips
- Compound clips for grouped sequences

## Data Model

```python
@dataclass
class Marker:
    name: str
    offset: str        # FCP time format "30/1s"
    marker_type: str   # "chapter" | "todo" | "standard"

@dataclass
class TitleClip:
    name: str
    duration: str
    text: str
    markers: list[Marker]

@dataclass
class GapClip:
    name: str
    duration: str
    markers: list[Marker]
```

## Integration

Works with the [NCP storyform](../docs/ncp-storyform.md) JSON format — feed your narrative structure directly into FCP.

```bash
# Storyform → FCPXML pipeline
python fcpxml-generator.py --from-json storyform-sequences.json --output edit-v1.fcpxml
```

## Requirements

- Python 3.10+
- No external dependencies (uses stdlib `xml.etree.ElementTree`)

## FCP Compatibility

Tested with Final Cut Pro 11 / 12. FCPXML 1.11 is backward-compatible with FCP 10.8+.

## License

MIT
