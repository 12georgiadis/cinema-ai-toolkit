# D3.js Documentary Visualizations

**Self-contained HTML visualizations for documentary film development.**

Two visualization types built for real production use: character relationship maps and narrative emotion curves. Both output standalone HTML files that open in any browser — no server needed.

## Relationship Map

Force-directed graph inspired by Mark Lombardi's network drawings. Visualizes character interconnections from a film bible or research database.

### Features

- Color-coded node types (protagonist, persona, journalist, family, institution, etc.)
- Radial layout with protagonist at center, related characters in concentric rings
- Edge types with distinct styles (solid, dashed, dotted) for relationship categories
- Click-to-inspect info panel with character details and connection list
- Drag to rearrange, scroll to zoom
- Dark theme (#0a0a0a background)

### Node Types

| Type | Color | Description |
|------|-------|-------------|
| PROTAGONIST | `#e74c3c` | Main subject |
| PERSONA | `#9b59b6` | Identities / aliases |
| FBI | `#2c3e50` | Law enforcement |
| FAMILY | `#27ae60` | Family members |
| JOURNALIST | `#f39c12` | Reporters, researchers |
| VICTIM | `#e67e22` | Targets |
| ANTAGONIST | `#c0392b` | Adversaries |
| INSTITUTION | `#3498db` | Organizations |
| FILMMAKER | `#1abc9c` | Documentary team |

### Edge Types

| Type | Style | Description |
|------|-------|-------------|
| CONTROLS | Solid, thick | Created / operates |
| INVESTIGATES | Dashed | Research / investigation |
| TARGETS | Solid arrow | Directed action |
| FAMILY | Solid, thin | Family connection |
| PROFESSIONAL | Dotted | Work relationship |
| ONLINE_INTERACTION | Solid, thin | Digital communication |
| MANIPULATES | Solid red | Deception |
| COLLABORATES | Solid blue | Cooperation |

### Data Format

```json
{
  "nodes": [
    {"id": "subject", "name": "Main Subject", "type": "PROTAGONIST", "description": "..."},
    {"id": "contact-a", "name": "Contact A", "type": "JOURNALIST", "description": "..."}
  ],
  "links": [
    {"source": "subject", "target": "contact-a", "type": "INVESTIGATES", "label": "interviewed", "weight": 3}
  ]
}
```

## Emotion Curve

Multi-layer temporal visualization of narrative emotional arcs across a film's structure.

### Features

- X-axis: film timeline (acts, sequences)
- Y-axis: emotional intensity (-1 to +1)
- Multiple overlapping curves (tension, empathy, revelation, discomfort)
- Act dividers with labels
- Hover tooltips with sequence details
- Responsive SVG with zoom

### Data Format

```json
{
  "acts": [
    {"name": "Act 1", "start_pct": 0, "end_pct": 25}
  ],
  "sequences": [
    {
      "name": "Opening",
      "position_pct": 5,
      "tension": 0.3,
      "empathy": 0.5,
      "revelation": 0.1,
      "discomfort": 0.2
    }
  ]
}
```

## Technical Stack

- **D3.js v7** (loaded from CDN)
- Pure HTML/CSS/JS, no build step
- Dark theme optimized for presentations
- All data embedded inline in the HTML

## Usage

These are templates. To generate visualizations from your own data:

1. Prepare your data as JSON (see formats above)
2. Embed it in the HTML template as `const data = {...}`
3. Open in browser

For automated generation from a film bible, see the Claude Code skills in this repo's parent project.

## License

MIT
