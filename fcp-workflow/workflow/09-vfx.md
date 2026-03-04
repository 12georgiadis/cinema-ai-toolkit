# 09 - Visual Effects and Motion Graphics

## In FCP

### Built-in
- **Object Tracker**: ML-based tracking for attaching effects/titles to moving objects
- **Cinematic Mode** depth editing (iPhone footage)
- Keyframing, compositing, blend modes
- Motion Templates for custom effects

### MotionVFX
- Gold standard FCP plugin ecosystem
- GPU-rendered, Apple Silicon optimized
- mPacks for titles, transitions, effects
- mCaptionsAI for animated subtitles
- Templates are customizable in Apple Motion

### CoreMelt
- **TrackX**: mocha tracking integrated in FCP (pin graphics to surfaces)
- **SliceX / DriveX**: shape-based masking and animation
- **Lock & Load X**: stabilization (see stabilization section)

### FxFactory
- Plugin marketplace: hundreds of effects, titles, transitions
- Notable: **Documentary Tools** bundle (titles, transitions, LUTs for broadcast doc)
- **Face Blur**: automatic face tracking and blur (documentary privacy protection)
- **Hawaiki Keyer 5**: professional chroma key with AI tracking

## Apple Motion

### What it is
- Apple's motion graphics app (included with Creator Studio subscription or $49.99 standalone)
- Creates custom FCP titles, transitions, effects, generators
- Real-time rendering in FCP via Motion Templates

### When to use it
- Custom lower thirds with your film's typography
- Animated maps (documentary staple)
- Data visualization (timelines, statistics)
- Custom transitions that match your film's visual language

### Claude Code + Motion
```bash
# Claude Code can help generate Motion XML templates
# or write scripts for batch-generating Motion projects
claude "Generate an Apple Motion template for a documentary lower third
with: name (large), title (small), location (italic).
Style: minimal, white text, subtle fade in/out."
```

## Compositing and VFX

### For complex VFX: roundtrip
- FCP → After Effects or Natron (open source) for heavy compositing
- Export individual clips, comp, re-import
- Or use Boris FX suite directly in FCP

### Natron (open source)
- Node-based compositing (like Nuke)
- Free and open source
- For filmmakers who want compositing without Adobe/Foundry subscription

## Documentary-specific VFX

### Screen recordings and digital content
- Documentaries about internet/digital subjects need clean screen captures
- OBS for screen recording
- Claude Code can help create animated recreations of chat logs, social media posts, etc.

### Archive footage treatment
- Grain matching between archive and new footage
- Format conversion (4:3 → 16:9 treatment)
- Dehancer for aging new footage to match archive
- Stabilization of old/shaky archive with Gyroflow or Lock & Load X

### Maps and data visualization
- Motion for animated maps
- D3.js (via Claude Code) for data visualizations rendered as video
- Screen capture of interactive visualizations
