# Notion Bridge

How Notion connects to the FCP workflow for collaborative production management.

## Marker Data: FCP → Notion

### What it does
- Exports FCP markers (with metadata, stills, GIFs) directly to a Notion database
- One-click from FCP via Share Destination or Workflow Extension
- Each marker becomes a Notion page with: timecode, name, notes, thumbnail, color label

### Use cases
- **Shot library**: every good shot as a searchable Notion database
- **Feedback tracking**: markers from review sessions → Notion Kanban board
- **ADR list**: dialogue markers that need re-recording
- **Music cue sheet**: music markers with timecodes
- **VFX shots**: VFX markers with reference stills

### Setup
1. Install Marker Data (free, open source)
2. Connect to Notion workspace
3. Create a database template (or use Marker Data's default)
4. In FCP: Share > Marker Data > Notion

## Production Management in Notion

### Recommended databases
- **Scenes**: scene number, status (written/shot/edited/graded), notes
- **Shots**: shot list with type, equipment, location, status
- **Schedule**: calendar view of shoot days
- **Crew**: contacts, roles, availability
- **Locations**: scouting data, permits, photos
- **Equipment**: inventory, rental needs, checklists
- **Feedback**: round, reviewer, status, resolution
- **Deliverables**: format, destination, deadline, status

### Templates
- [Filmmaking Base Camp](https://notion4film.gumroad.com/l/fixob) (free)
- Notion Marketplace: search "film production" or "video production"
- Build your own: Claude Code can generate Notion database schemas

### Integration with Claude Code
- Claude Code has a Notion MCP server installed
- Can read and write to Notion databases
- Automate: create pages from scripts, update status, generate reports

```bash
# Example: sync edit progress to Notion
claude "Read the FCP project FCPXML and for each sequence,
update the corresponding Notion 'Scenes' database entry
with: duration, number of clips, last modified date, status."
```

## Frame.io ↔ Notion

### Bridge workflow
1. Export Frame.io comments as CSV
2. Import CSV into Notion database
3. Each comment becomes a trackable task
4. Or: use Marker Toolbox to import Frame.io comments as FCP markers first,
   then Marker Data to send those markers to Notion

## Obsidian ↔ Notion

### Division of labor
| Obsidian | Notion |
|----------|--------|
| Script writing | Call sheets |
| Research notes | Schedule |
| Creative decisions | Crew management |
| Personal production diary | Shared feedback |
| Offline work | Collaborative tracking |

### Linking
- Paste Notion page URLs in Obsidian notes for cross-reference
- Export Notion databases as Markdown → import into Obsidian for offline backup
- Claude Code can automate this sync
