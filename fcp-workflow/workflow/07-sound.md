# 07 - Sound Design and Mix

## Philosophy

Sound is half the film. Documentary sound especially: room tone, ambient noise, breath, hesitation -- these are as important as the words.

## In FCP

### Quick fixes with CrumplePop
- **EchoRemover**: fix reverb/echo in bad interview rooms
- **WindRemover**: outdoor interview rescue
- **RustleRemover**: lavalier clothing noise
- **AudioDenoise**: general background noise
- **PopRemover**: plosives (P, B sounds)
- **LevelMatic**: auto-leveling for interviews with varying volume
- All work as FCP effects, real-time preview

### FCP built-in audio tools
- Audio Inspector: EQ, panning, volume automation
- Audio Roles: organize tracks (Dialogue, Ambience, Music, SFX, VO)
- Loudness normalization
- Spatial audio support

### DAWBridge
- Sync FCP timeline with Logic Pro or Pro Tools
- Make changes in the DAW, they appear in FCP
- Best of both worlds: edit in FCP, design sound in a real DAW

## Roundtrip to Pro Tools

### X2Pro Audio Convert
- Export FCP timeline → AAF/OMF for Pro Tools
- Preserves all audio metadata, markers, roles
- Send to sound designer/mixer
- They work in Pro Tools, deliver stems back
- Import stems into FCP for final master

### When to roundtrip
- Always for theatrical release / festival submissions
- Dolby Atmos requires Pro Tools or dedicated tools
- Simple web/broadcast: CrumplePop + FCP built-in can be enough

## Audio Restoration Tools

### iZotope RX 11 — ★★★★★
- Industry standard audio restoration, nothing comes close
- **Dialogue Isolate**: ML-based separation of voice from everything else
- **Spectral Repair**: visually identify and remove specific sounds
- **Voice De-reverb**: remove room reflections
- **De-noise**: adaptive noise removal
- **De-clip**: repair clipped/distorted audio
- **Mouth De-click**: remove mouth noises
- Works as standalone app or AAX/AU plugin
- Process individual clips before editing, or apply in Pro Tools
- For documentary: essential for interview rescue (bad rooms, unexpected noise)

### Supertone Clear — ★★★★☆
- ML-based de-reverb + de-noise, acquired by Adobe
- Excellent on voice recordings, strong competitor to RX on specific tasks
- Lighter and faster than RX for targeted voice cleanup

### Acon Digital Extract:Dialogue — ★★★★☆
- ML voice separation at a fraction of RX's price
- Good alternative when you only need dialogue isolation
- Won't replace RX's full spectral editing toolkit

### When to use what
- **Quick fix in FCP**: CrumplePop (★★★★☆) — no roundtrip needed
- **Serious restoration**: iZotope RX 11 (★★★★★) — spectral editing, complex problems
- **Budget voice separation**: Acon Extract:Dialogue (★★★★☆)
- **Fast voice cleanup**: Supertone Clear (★★★★☆) or iZotope VEA (★★★☆☆)

## Mixing Plugins

### Fabfilter Pro-Q 4 — ★★★★★
- Best EQ plugin available. Dynamic bands, mid/side, per-band spectrum
- Essential for surgical dialogue cleanup: room resonances, proximity effect, sibilance
- Visual spectral display makes problems obvious

### Fabfilter Pro-L 2 — ★★★★★
- Reference limiter for broadcast loudness (LUFS -23 EBU, -24 ATSC)
- True peak limiting for streaming platforms
- Use on final mix bus

### Fabfilter Pro-DS — ★★★★☆
- Split-band de-esser, transparent on voice
- More precise than RX de-ess for final mix stage

## Creative Sound Design

### Soundtoys 5 — ★★★★★
- Distortion (Decapitator), delay (EchoBoy), modulation (PhaseMistress)
- Not for restoration — for transforming sound, creating textures
- Useful for experimental documentary sound design

## Music

### Beat Detection (FCP 12)
- Analyze music tracks: bars, beats, song sections
- Beat Grid in timeline: visual guide for cutting to music
- Uses Logic Pro's ML engine
- Perfect for montage sequences

### Music sources
- Artlist, Musicbed, Epidemic Sound for licensed music
- Logic Pro for custom scoring
- Freesound.org for ambient/SFX (Creative Commons)
