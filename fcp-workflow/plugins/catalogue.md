# FCP Plugin Catalogue

Complete catalogue of recommended tools for auteur documentary filmmaking. Updated February 2026.

## Legend
- **$** = under $20 | **$$** = $20-50 | **$$$** = $50-100 | **$$$$** = $100+
- **MAS** = Mac App Store | **Web** = direct download | **FxF** = FxFactory

---

## LateNite Films Ecosystem (Chris Hocking)

The backbone of a serious FCP workflow. Open source, actively maintained.

| Tool | Price | Source | What it does |
|------|-------|--------|--------------|
| **CommandPost** | Free* | Web | Automation, control surfaces, Lua scripting, Search Console. *Requires 1 paid LateNite app. |
| **BRAW Toolbox** | $$ | MAS | Native Blackmagic RAW import. Keyframe ISO, Exposure, Color Temp. |
| **Gyroflow Toolbox** | $$ | MAS | Gyroscope-based stabilization from Gyroflow data. |
| **LUT Robot** | $$ | MAS | Auto-apply Camera LUTs by filename matching. |
| **Fast Collections** | $ | MAS | Generate Smart Collections from keyword lists. |
| **Marker Toolbox** | $$ | MAS | Import Vimeo/Wipster/Frame.io/email feedback as markers. ChatGPT integration. |
| **Recall Toolbox** | $ | MAS | Shared clipboard with iCloud sync. |
| **Capacitor** | $ | MAS | Convert between FCPXML versions (v1.6-v1.14). |
| **Metaburner** | $$ | MAS | Advanced metadata generator, 25 text layers, Lua scripting. |
| **Transfer Toolbox** | $$ | MAS | Convert Mac FCP libraries to iPad FCP projects. |

**Bundles:**
- Pro Editor Bundle: $100 (BRAW, Gyroflow, Marker, Recall, Fast Collections)
- Pro Editor Bundle v2: $150 (+ LUT Robot, Capacitor)
- Pro Editor Bundle v3: $179.99 (everything)

---

## Stabilization

| Tool | Price | Source | Notes |
|------|-------|--------|-------|
| **Gyroflow Toolbox** | $$ | MAS | Best if you have gyro data. Works with BRAW Toolbox. |
| **CoreMelt Lock & Load X** | $$ | Web | 4x faster than FCP built-in. Rolling shutter, batch processing. |
| **CrumplePop BetterStabilizer** | $$ | Web | Presets: handheld walk, bike mount, car mount, etc. |
| **FCP built-in stabilization** | Free | — | Good enough for simple cases. |

---

## Color Grading

| Tool | Price | Source | Notes |
|------|-------|--------|-------|
| **FCP built-in** | Free | — | Color Wheels, Curves, Color Match, HDR. Solid basics. |
| **Color Finale 2** | $$$ | Web | Dedicated grading UI inside FCP. Secondaries, masks, tracking. |
| **FilmConvert Nitrate** | $$$ | Web | Real film stock emulation with camera profiles. |
| **Dehancer Pro** | $$$ | Web | Analog look: halation, bloom, grain, color. |
| **LUT Robot** | $$ | MAS | Auto Camera LUT application. |
| **Magic Bullet Suite** | $$$$ | Web | Red Giant/Maxon complete grading suite. |
| **mFilmLook** (MotionVFX) | $$ | Web | All-in-one cinematic look plugin. |
| **Cinema Grade** | $$$ | Web | Grade directly in the viewer. |

---

## Audio

### Restoration & Repair

| Tool | Rating | AI | Price | Source | Notes |
|------|--------|-----|-------|--------|-------|
| **iZotope RX 11** | ★★★★★ | Yes | $$$$ | Web | Industry standard. Dialogue Isolate, Spectral Repair, De-reverb, De-noise, De-clip. Nothing rivals it. |
| **Cedar DNS One** | ★★★★★ | No | $$$$ | Web | Broadcast standard de-noise. Real-time. Used in TV/news worldwide. |
| **Supertone Clear** | ★★★★☆ | Yes | $$$ | Web | Excellent ML de-reverb + de-noise. Acquired by Adobe. Strong on voice. |
| **CrumplePop Audio Suite** | ★★★★☆ | Yes | $$$ | Web | 8 plugins: echo, noise, wind, rustle, plosives, leveling. Works as FCP effects. Quick fixes without roundtrip. |
| **Acon Digital Extract:Dialogue** | ★★★★☆ | Yes | $$ | Web | ML voice separation. Direct competitor to RX Dialogue Isolate at lower price. |
| **iZotope VEA** | ★★★☆☆ | Yes | $$ | Web | One-button AI voice enhancer. Fast but limited control for serious work. |
| **Klevgrand Brusfri** | ★★★☆☆ | No | $ | Web | Budget de-noise. Decent, lightweight, limited. |
| **Adobe Podcast Enhance** | ★★★☆☆ | Yes | Free | Web | Web-only voice cleanup. OK for quick rough edits. |
| **Audo.ai** | ★★☆☆☆ | Yes | Freemium | Web | Basic web-only cleanup. Not production-grade. |

### Mixing & Processing

| Tool | Rating | AI | Price | Source | Notes |
|------|--------|-----|-------|--------|-------|
| **Fabfilter Pro-Q 4** | ★★★★★ | No | $$$ | Web | Best EQ plugin. Dynamic EQ, mid/side, spectral display. Essential for dialogue cleanup. |
| **Fabfilter Pro-L 2** | ★★★★★ | No | $$$ | Web | Best limiter. Broadcast loudness (LUFS). True peak limiting. |
| **Fabfilter Pro-DS** | ★★★★☆ | No | $$ | Web | Precise split-band de-esser. Transparent on voice. |
| **Waves NS1** | ★★★☆☆ | No | $ | Web | One-knob noise suppressor. Quick and dirty, useful in rough cuts. |

### Creative & Sound Design

| Tool | Rating | AI | Price | Source | Notes |
|------|--------|-----|-------|--------|-------|
| **Soundtoys 5 Bundle** | ★★★★★ | No | $$$$ | Web | Legendary creative effects: distortion, delay, modulation. For sound design, not restoration. |
| **Audio Design Desk** | ★★★★☆ | Yes | $$$ | Web | AI-powered SFX and music placement. Workflow Extension. |

### Workflow & Roundtrip

| Tool | Rating | AI | Price | Source | Notes |
|------|--------|-----|-------|--------|-------|
| **X2Pro Audio Convert** | ★★★★★ | No | $$$ | Web | FCP → Pro Tools roundtrip (AAF/OMF export). The only serious option. |
| **DAWBridge** | ★★★☆☆ | No | $$ | Web | Sync FCP with Logic Pro / Pro Tools. Useful but can be finicky. |

---

## Transcription & Subtitles

| Tool | Price | Source | Notes |
|------|-------|--------|-------|
| **FCP 12 built-in** | Free | — | Transcript Search (all clips), Transcribe to Captions (English only). |
| **Jojo Transcribe** | Free | MAS | Whisper V2/V3 Turbo. 100+ languages. Translation. Best free option. |
| **MacWhisper** | Freemium | Web | Transcribe + translate simultaneously. Good UI for corrections. |
| **Captionator** | $$ | MAS | Animated captions (YouTube/TikTok style). Per-word keyframing. |
| **mCaptionsAI** (MotionVFX) | $$ | Web | 90+ languages, 26+ styles, FCP plugin. |
| **Transcriber** (FxFactory) | $$ | FxF | Whisper + optional ChatGPT punctuation. |
| **Whisper Auto Captions** | Free | GitHub | Open source, whisper.cpp based. |
| **Simon Says** | Subscription | Web | Cloud transcription, 100+ languages. Workflow Extension. |

---

## Titles & Motion Graphics

| Tool | Price | Source | Notes |
|------|-------|--------|-------|
| **Apple Motion** | $49.99 or sub | MAS | Custom FCP titles/transitions/effects/generators. |
| **MotionVFX mPacks** | Various | Web | Gold standard. GPU rendered, Apple Silicon optimized. |
| **CoreMelt TrackX** | $$$ | Web | mocha tracking for pinning graphics to surfaces. |
| **Yanobox Motype** | $$$ | FxF | 250+ animated typography presets. |
| **Universe** (Red Giant) | $$$$ | Web | Titles, transitions, motion graphics. |
| **Documentary Tools** (FxF) | $$ | FxF | Titles, transitions, LUTs specifically for broadcast doc. |

---

## VFX & Compositing

| Tool | Price | Source | Notes |
|------|-------|--------|-------|
| **Hawaiki Keyer 5** | $$$ | FxF | Pro chroma key with AI tracking. Simon Ubsdell. |
| **Neat Video** | $$$ | Web | Professional noise reduction (wavelet algorithms). |
| **Flicker Free** | $$ | Web | LED flicker, slow-mo, drone flicker removal. |
| **Face Blur** (FxFactory) | $ | FxF | Auto face tracking and blur. Documentary privacy. |
| **Natron** | Free | Web | Open source node-based compositing (like Nuke). |

---

## Collaboration & Organization

| Tool | Price | Source | Notes |
|------|-------|--------|-------|
| **Frame.io** | $15/user/mo | Web | Review, timestamped comments. Native FCP Workflow Extension. |
| **PostLab** (Hedge) | Perpetual | Web | Version control, project locking for FCP teams. |
| **Marker Data** (The Acharya) | Free/Open | GitHub | FCP markers → Notion, Airtable, PDF, web galleries. |
| **Lumberjack System** | $25/mo | Web | Real-time documentary logging (iOS + web). |
| **Lumberjack Builder** | Included | Web | Text-driven editing from transcripts. |

---

## Media Management

| Tool | Price | Source | Notes |
|------|-------|--------|-------|
| **Kyno** (Signiant) | $$$ | Web | Preview, rename, tag, transcode. Cross-platform. Apple Silicon (v1.9). |
| **evrExpanse** | $$ | Web | Finder as MAM. Metadata bridge DaVinci Resolve ↔ FCP. |
| **Sync-N-Link** | $$ | MAS | Multi-camera/audio waveform sync. |

---

## AI & Semantic Search

| Tool | Price | Source | Notes |
|------|-------|--------|-------|
| **FCP 12 Visual Search** | Free | — | Natural language search in footage. Apple Silicon. |
| **Jumper** (Witchcraft) | TBD | Web | AI footage search, 100% offline. Natural language queries. |
| **ChatFCP** | TBD | Web | LLM integration in FCP. Workflow Extension. |
| **Picture This...** | TBD | Web | Text-to-image generation from markers. Local ML. |

---

## Control Surfaces

Configured via **CommandPost**:

| Surface | Price | Notes |
|---------|-------|-------|
| **Tangent Wave** | $$$$$ | Pro color grading. Trackballs + dials. |
| **Tangent Ripple** | $$$ | Budget Tangent. 3 trackballs. |
| **Stream Deck** (all variants) | $$ | Programmable buttons. Visual feedback. |
| **TourBox** | $$ | Jog wheel + buttons. Good for scrolling/navigating. |
| **Monogram/Palette** | $$$ | Modular physical controls. |
| **Loupedeck** (all variants) | $$$ | Touchscreen + dials. |
| **DaVinci Resolve keyboards** | $$-$$$ | Speed Editor, Editor Keyboard (work with FCP via CommandPost). |
| **MIDI devices** | Various | Including TouchOSC (iPad as controller). |
