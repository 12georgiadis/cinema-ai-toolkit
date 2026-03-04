# 06 - Color Grading

## Approach

Auteur cinema grading is about mood and meaning, not just "correct" color. The grade should feel like a creative decision, not a technical fix.

## FCP built-in tools

### Color Wheels / Color Curves
- Shadows, Midtones, Highlights wheels
- Hue/Saturation curves for targeted adjustments
- Color Board for quick broad adjustments

### Enhance Light and Color (FCP 12)
- ML-based auto correction
- Good starting point: apply first, then refine manually
- Handles exposure and white balance well
- Not a replacement for creative grading

### Color Match
- Match between shots using reference frames
- Useful for consistency across interview setups

### HDR
- FCP supports HDR editing natively
- HDR tools in Color Inspector for Rec. 2020 / HLG / PQ

## Plugins

### Color Finale 2
- Dedicated grading interface within FCP
- Color wheels, curves, vectors, film emulation
- Secondary corrections, masks, tracking
- For serious grading without leaving FCP

### FilmConvert Nitrate
- Real film stock emulation (Kodak, Fuji stocks)
- Camera-specific profiles (knows how YOUR camera renders color)
- Grain simulation from actual film scans
- Perfect for auteur look: choose a stock that matches your story's era/mood

### Dehancer Pro
- Analog film look: color, contrast, halation, bloom, grain, vignette
- Based on measurements of real analog processes
- More "artistic" than FilmConvert -- more control over individual analog effects

### LUT Robot (LateNite)
- Automatically applies Camera LUTs by matching filenames
- Essential for multi-camera shoots with different cameras
- Set it once at ingest, forget about it

## Grading with control surfaces

### Tangent panels via CommandPost
- **Tangent Wave** (~900$) or **Tangent Ripple** (~330$)
- CommandPost is the bridge: FCP parameters → Tangent Mapper
- Track balls for lift/gamma/gain
- Physical dials for fine adjustments (faster and more precise than mouse)

### TourBox
- Jog wheel for scrolling through timeline
- Programmable buttons for switching tools
- Configure via CommandPost

## Workflow

1. **LUT Robot** applies camera LUTs at ingest (technical base)
2. **Enhance Light and Color** as first pass (ML correction)
3. **Adjustment Clips** for scene-wide looks (new in FCP 12)
4. **Color Finale 2** or **Dehancer** for creative look per scene
5. **Color Match** for shot-to-shot consistency within scenes
6. Control surfaces for precision adjustments
7. Export reference stills for continuity
