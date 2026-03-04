# Cinema Voice Pipeline

**Voice direction for documentary filmmakers working with non-professional subjects.**

The problem: your subject recorded their voice-over. The voice is authentic — it's theirs, irreplaceable. But the delivery is inconsistent. You can't go back and re-record. You need to fix the performance after the fact.

This is ADR logic applied through AI. Not replacing the voice — repairing the performance.

---

## Full Pipeline Overview

```
RAW RECORDINGS
      │
      ▼
[Phase 0 — Source Cleaning]          ← This doc, new section below
Denoise → Isolate → Diarize → Segment → Normalize
      │
      ▼
[Phase 1 — Voice Direction]
Enhance → Inpaint → Fix delivery → Regenerate
(Resemble Fill)  (Respeecher)   (Sesame CSM / Chatterbox)
      │
      ▼
VOICE CLONE READY
```

---

## Phase 0 — Source Cleaning (Before Any Voice Direction)

Your recordings exist. Before any voice direction work, you need clean, isolated, segmented audio. This section documents the full preparation pipeline.

### 0.1 — Analyze First

Before applying any tool, generate a spectrogram and measure SNR.

```bash
pip install librosa matplotlib soundfile
python analyze_audio.py recording.wav
```

The script generates: spectrogram, RMS over time, low-frequency noise detection (fridge/hum), estimated SNR. Makes the problem visible before treating it.

See [`scripts/analyze_audio.py`](scripts/analyze_audio.py).

---

### 0.2 — Denoise

**Tested on documentary voice-over material (16kHz Zoom recordings):**

| Tool | SNR gain | Notes | Local/Cloud |
|------|----------|-------|-------------|
| **[DeepFilterNet 3](https://github.com/Rikorose/DeepFilterNet)** | +15 dB | Best denoising, fast, runs on CPU | Local |
| **[Lava-SR](https://fal.ai/models/fal-ai/lava-sr)** | +1 dB denoising | Adds 16→48kHz upscaling, 7s for 5min | Cloud (fal.ai) |
| **[Resemble Enhance](https://github.com/resemble-ai/resemble-enhance)** | High | Best perceptual quality, Linux/CUDA only | Local (Linux) |
| **[ElevenLabs Voice Isolator](https://elevenlabs.io/voice-isolator)** | High | Best cloud quality | Cloud — check ToS |
| **[UVR](https://ultimatevocalremover.com/)** | High | Local GUI, neural voice isolation | Local |

**Optimal pipeline (macOS without GPU):**
```bash
# Step 1 — Denoise locally (DeepFilterNet, 16kHz in/out)
pip install deepfilternet
deepFilter recording.wav -o output/

# Step 2 — Upscale to 48kHz (Lava-SR via fal.ai, 7s per 5min)
pip install fal-client
python scripts/enhance_fal.py output/recording_DeepFilterNet3.wav
```

**If you have "pure noise" recordings** (room tone alone, fridge alone): use Audacity's *Noise Reduction* with *Get Noise Profile*. The most precise approach for a known noise source — no ML needed.

---

### 0.3 — Isolate Voice (UVR)

For recordings with heavy background or multiple room elements, [Ultimate Vocal Remover](https://ultimatevocalremover.com/) — free, local, GUI — runs Demucs, MDX-Net, and VR Architecture models.

Recommended model: **UVR-DeNoise** or **MDX23C** for voice isolation from background.

---

### 0.4 — Separate Speakers (Diarization)

If your recording contains multiple voices (interview, conversation), identify and extract the target speaker before cloning.

```bash
pip install whisperx
whisperx recording.wav --diarize --hf_token YOUR_TOKEN --min_speakers 1 --max_speakers 3
```

WhisperX outputs: timestamped transcript with speaker labels. Filter by target speaker, extract those segments.

For standalone diarization without transcription: [pyannote-audio](https://github.com/pyannote/pyannote-audio).

---

### 0.5 — Remove Long Silences + Segment

Extract usable speech segments (5–30s), discard silence > 2s.

```bash
python scripts/process_pipeline.py recording_cleaned.wav
# Outputs: processed/02-segments/*.wav
```

What to keep: natural breath pauses (< 1s) — voice cloners need them for naturalness.
What to discard: silences > 2s, takes with audible noise events, takes where the subject is not the target speaker.

---

### 0.6 — Normalize

Target spec for voice cloning input:
- **-18 dBFS RMS** (ElevenLabs Professional Voice Clone requirement)
- **True peak < -3 dBFS**
- **WAV 48kHz 24-bit mono**

```bash
python scripts/process_pipeline.py recording_cleaned.wav  # handles normalization
# Or in Logic Pro / FCP: Loudness → Target -18 LUFS
```

**FCP 12** has built-in tools for this under *Audio Inspector → Audio Enhancements*:
- **Voice Isolation** — ML-based, good quality for basic cleanup
- **Noise Removal** slider
- **Hum Removal** — 50/60Hz electrical hum
- **Loudness** — target LUFS normalization

---

### 0.7 — Minimum Material for Voice Cloning

| Service | Minimum clean audio |
|---------|-------------------|
| Respeecher (S2S) | 1 hour |
| ElevenLabs Professional Voice Clone | 30 minutes |
| Chatterbox (zero-shot clone) | 5 seconds |
| Sesame CSM (context audio) | 30 seconds |

---

## The Intervention Hierarchy

After cleaning, apply voice direction. Always start with the minimal intervention.

```
Minimal                                          Maximum
   │                                                │
   ▼                                                ▼
Enhance → Inpaint specific words → Fix delivery → Regenerate full take
(free)      (Resemble Fill)      (Respeecher)    (Sesame CSM / Chatterbox)
```

---

## Tier 0 — Before Everything: Enhance

**[Resemble Enhance](https://github.com/resemble-ai/resemble-enhance)** — Open source, Apache 2.0

Run this on every recording before making any editorial judgment. Neural denoising + enhancement. Takes audio recorded in any conditions — room, phone, car — and brings it to studio level. Preserves the speaker's idiosyncrasies. Free.

```bash
pip install resemble-enhance
resemble_enhance input.wav output_enhanced.wav --denoise --enhance
```

---

## Tier 1 — Fix Specific Moments: Inpainting

**[Resemble Fill](https://www.resemble.ai/fill/)** — Commercial (Resemble AI)

Audio inpainting. You mark the exact word, phrase, or line that doesn't work. Resemble Fill regenerates only that segment in the cloned voice — preserving everything around it: breath, room tone, adjacent delivery. The rest of the take stays untouched.

This is the right tool when the problem is localized: one line delivered flat, one word clipped, one pause too long. You don't replace the take — you repair the specific failure.

---

## Tier 2 — Fix the Delivery: Speech-to-Speech

When the problem is the entire delivery of a take — the pacing, the rhythm, the register — you need speech-to-speech: feed the take in, get the same voice with corrected performance.

### **[Respeecher](https://www.respeecher.com)** — The cinema standard

Respeecher is the professional benchmark for voice work in film. Credits include:

- *The Mandalorian* — young Luke Skywalker
- *The Book of Boba Fett* — young Luke Skywalker
- *Obi-Wan Kenobi* — Darth Vader (restoring James Earl Jones' original register)
- *The Brutalist* (2024)
- *Emilia Pérez* (2024)
- *GOLIATH* (Showtime/Paramount+) — posthumous narration from Wilt Chamberlain's archival recordings
- *In Event of Moon Disaster* (IDFA 2019, Emmy) — Richard Nixon documentary narration

Their core model is **speech-to-speech native** — not TTS with voice clone added on top. You feed a take (from any speaker, including yourself doing the delivery you want), they convert it to the target voice while preserving the prosody, pacing, and emotional register.

> For the inner voice of a documentary subject: record yourself or a stand-in doing the delivery you want to hear. Respeecher converts it to the subject's voice. The subject's timbre, your direction.

**Pricing** (pay-as-you-go, accessible to independents):
- $27 → 30 min speech-to-speech
- $70 → 100 min speech-to-speech
- $250 → 500 min speech-to-speech

**Ethical framework**: 4 C's — Credit, Consent, Control, Compensation. Works with deepfake detection partners (Pindrop, Reality Defender). Endorsed the NO FAKES Act.

**Access**: [respeecher.com/marketplace/filmmakers](https://www.respeecher.com/marketplace/filmmakers)

---

### **[Seed-VC](https://github.com/Plachtaa/seed-vc)** — Open source alternative for S2S

Zero-shot V2V, no training required. 1–30 sec of reference audio. Real-time option. V2 adds accent + emotion conversion.

> Practical shortcut: use a well-delivered take from the same subject as the style reference. The subject directs themselves.

```bash
pip install seed-vc
seed-vc \
  --source bad_take.wav \
  --target good_take_reference.wav \
  --output fixed_take.wav
```

---

### **[Resemble AI Speech-to-Speech](https://www.resemble.ai/voice-cloning/)** — Commercial

Real-time STS, ADR-specific workflow. Per-word timestamps for editorial precision. On-premise deployment available (important for productions with legal sensitivities around voice data). Andy Warhol's voice reconstructed from 3 minutes of archive for Netflix documentary.

**⚠️ ElevenLabs ToS note**: ElevenLabs updated their Terms of Service in 2025 to claim perpetual, irrevocable, royalty-free rights over voice data. For a film involving a real person's voice in a legally sensitive context, verify the current ToS before uploading.

**[ElevenLabs v3 Speech-to-Speech](https://elevenlabs.io/blog/eleven-v3)** — Commercial

Most expressive commercial STS. Audio tags for in-script emotion control (`[whispering]`, `[hesitant pause]`). 70+ languages. Multi-speaker dialogue in one pass. Quality benchmark in the space — but see ToS note above.

---

## Tier 3 — Full Regeneration: Rebuild from Script

When a take is beyond repair and you need to regenerate from text.

### **[Sesame CSM-1B](https://github.com/SesameAILabs/csm)** — Open source, Apache 2.0

The most cinematically relevant architecture for inner monologue / documentary narration. Designed to cross the uncanny valley in *conversational* speech — not clean TTS but speech with micro-pauses, breath patterns, register shifts. Processes previous audio as context, so long-form narration stays coherent in feel.

This is the model architecturally closest to the register of an inner voice monologue.

```bash
# Community wrapper with Gradio + voice cloning
# github.com/phildougherty/sesame_csm_openai
# Supports CUDA, MLX (Apple Silicon), CPU
```

### **[Chatterbox](https://github.com/resemble-ai/chatterbox)** — Open source, MIT (Resemble AI)

Best open-source TTS for regeneration. Emotion exaggeration control. Beats ElevenLabs in blind tests (63.8% preference). Zero-shot clone from 5 seconds. 23 languages.

```bash
pip install chatterbox-tts
python -c "
from chatterbox.tts import ChatterboxTTS
model = ChatterboxTTS.from_pretrained('resemble-ai/chatterbox')
wav = model.generate(
    'Text to regenerate.',
    audio_prompt_path='subject_reference.wav',
    exaggeration=0.4
)
model.save(wav, 'output/result.wav')
"
```

---

## Supporting Open-Source Models

| Model | License | Notes |
|-------|---------|-------|
| [Fish Speech V1.5](https://github.com/fishaudio/fish-speech) | CC-BY-NC | ELO 1339 TTS Arena. Best benchmark score open source. Non-commercial only. |
| [CosyVoice 3](https://github.com/FunAudioLLM/CosyVoice) | Apache 2.0 | Instruction-based delivery: "speak hesitantly, slowly, with long pauses" |
| [F5-TTS](https://github.com/SWivid/F5-TTS) | MIT | Zero-shot, fast, reliable baseline |
| [RVC + Applio](https://github.com/IAHispano/Applio) | Open | V2V with trained model. 100k+ community voice models. |
| [Kyutai Pocket TTS](https://kyutai.org/tts) | Open | 100M params, CPU real-time, voice cloning. Jan 2026. |
| [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) | MIT | 1 min of audio to train a full model |

**Live leaderboards** (field moves weekly):
- [TTS Arena V2](https://tts-agi-tts-arena-v2.hf.space/leaderboard)
- [Artificial Analysis](https://artificialanalysis.ai/text-to-speech/models)

---

## Full Workflow for Documentary Post-Production

```
1. ENHANCE ALL RECORDINGS
   └── Resemble Enhance on everything (free, open source)
       → studio baseline regardless of original conditions

2. EDIT FIRST
   └── The edit reveals which takes are fixable and which need intervention

3. IDENTIFY INTERVENTION LEVEL per take
   ├── Bad word/phrase only?
   │   └── Resemble Fill (inpaint the specific segment)
   ├── Bad delivery of full take?
   │   └── Respeecher S2S (record the delivery you want → convert to subject's voice)
   │       OR Seed-VC (use a good take as style reference)
   └── No good take exists, working from script?
       └── Sesame CSM (long-form conversational narration)
           OR Chatterbox (best open-source TTS clone)

4. MATCH ROOM TONE
   └── Any generated segment needs to match the acoustic environment
       of surrounding material. Impulse response convolution in
       DaVinci Fairlight, Pro Tools, or Audacity.

5. FINAL MIX
   └── DaVinci Fairlight / Pro Tools: levels, EQ, compression
```

---

## Audio Preprocessing

| Tool | Function |
|------|----------|
| **[Resemble Enhance](https://github.com/resemble-ai/resemble-enhance)** | Denoising + enhancement. Start here. Open source. |
| **Whisper large-v3** | Transcription + word timestamps |
| **[WhisperX](https://github.com/m-bain/whisperX)** | Whisper + speaker diarization (20.4k stars) |
| **[Demucs](https://github.com/facebookresearch/demucs)** | Vocal isolation |
| **[DeepFilterNet](https://github.com/Rikorose/DeepFilterNet)** | Neural noise reduction |

---

## Ethical Framework

See [ETHICS.md](ETHICS.md).

Required conditions for use on real persons:
1. Written consent specifying the production and use
2. Declared artistic frame in the released work
3. Subject approval rights on released material

On data custody: Resemble AI and Respeecher offer on-premise and privacy-first options. ElevenLabs (as of 2025) claims perpetual rights over uploaded voice data — verify current ToS for legally sensitive productions.

Respeecher's framework: Credit, Consent, Control, Compensation.

---

## Installation

```bash
git clone https://github.com/12georgiadis/cinema-voice-pipeline
cd cinema-voice-pipeline
pip install -r requirements.txt

pip install resemble-enhance   # Tier 0 — enhance all recordings first
pip install seed-vc            # Tier 2 — zero-shot V2V (open source)
pip install chatterbox-tts     # Tier 3 — best open-source TTS regen
```

Python 3.10+, ffmpeg. GPU recommended for Sesame CSM; Resemble Enhance and Seed-VC (small model) run on CPU.

---

Part of the [ai-cinema-research](https://github.com/12georgiadis/ai-cinema-research) ecosystem.

MIT License.
