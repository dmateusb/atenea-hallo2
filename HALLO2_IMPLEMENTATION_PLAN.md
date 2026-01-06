# Hallo2 Implementation Plan
## Clean Repo: atenea-hallo2

Based on analysis and user requirements, we'll create a **new focused repository** with only what's needed for professional Hallo2 video generation.

---

## Why New Repo?

**Problems with current approach:**
- ❌ Mixing two different models (SadTalker + Hallo2) adds complexity
- ❌ Hallo2 has completely different architecture (diffusion vs 3D face modeling)
- ❌ Risk of breaking working SadTalker setup
- ❌ Confusing documentation trying to cover both models

**Benefits of new repo:**
- ✅ Clean, focused implementation
- ✅ Simpler to understand and maintain
- ✅ Keep working atenea (SadTalker) as fallback
- ✅ Can optimize specifically for Hallo2
- ✅ Easier to onboard contributors

---

## Repository Structure

```
atenea-hallo2/
├── python/
│   ├── hallo2_inference.py        # Main inference script
│   ├── audio_converter.py         # MP3 → WAV conversion
│   └── config_generator.py        # YAML config from CLI args
├── src/
│   ├── cli.ts                     # TypeScript CLI (from atenea)
│   ├── tts.ts                     # OpenAI TTS with caching (from atenea)
│   └── video-generator.ts         # Hallo2-specific orchestrator
├── hallo2/                        # Git submodule or clone
│   └── (official Hallo2 repo)
├── configs/
│   └── default.yaml               # Template config
├── data/
│   ├── images/                    # Avatar images
│   └── audio/                     # Cached TTS audio
├── scripts/
│   ├── setup.sh                   # One-command setup
│   └── download_models.sh         # Model download script
├── .env.example
├── .gitignore
├── package.json
├── requirements.txt
├── tsconfig.json
└── README.md
```

---

## What We Keep from Current Atenea

### ✅ Keep (Proven & Working)

1. **TTS Integration** (`src/tts.ts`)
   - OpenAI API integration
   - Voice selection (nova, alloy, etc.)
   - Error handling

2. **Audio Caching** (`src/tts.ts`)
   - SHA256 hash-based caching
   - Saves API costs
   - Deterministic filenames

3. **CLI Structure** (`src/cli.ts`)
   - Commander.js setup
   - Options parsing
   - Spinner/progress indicators

4. **TypeScript Orchestration** (`src/video-generator.ts`)
   - Clean separation Node.js ↔ Python
   - subprocess management
   - Error handling

### ❌ Remove (Hallo2-Specific)

1. **SadTalker wrapper** - Not needed
2. **Multi-model logic** - Single model only
3. **MPS/Mac support** - Focus on CUDA/RunPod
4. **NumPy 2.x patches** - Hallo2 handles this
5. **Conservative mode** - Different memory management

---

## Core Functionality

### User Flow
```
1. User writes text → input.txt
2. npm run generate
3. TTS generates speech → cached MP3
4. MP3 converted to WAV (Hallo2 requirement)
5. Hallo2 generates video → output.mp4
6. Done!
```

### Technical Flow
```
CLI (TypeScript)
  ↓
  calls TTS → audio/speech_<hash>.mp3
  ↓
  calls audio_converter.py → audio/speech_<hash>.wav
  ↓
  calls hallo2_inference.py
    ↓
    generates config YAML
    ↓
    calls hallo2/scripts/inference_long.py
    ↓
    returns video path
  ↓
  moves to output.mp4
```

---

## Implementation Components

### 1. Python Layer

#### `python/audio_converter.py`
```python
def convert_to_wav(mp3_path, wav_path):
    # ffmpeg conversion
    # 16kHz mono for speech
    # validates input/output
```

#### `python/config_generator.py`
```python
def generate_config(
    source_image,
    audio_wav,
    output_path,
    resolution=512,
    fps=25,
    steps=40
):
    # creates YAML config
    # from CLI parameters
```

#### `python/hallo2_inference.py`
```python
def main():
    # parse args
    # generate config YAML
    # convert audio to WAV if needed
    # call hallo2/scripts/inference_long.py
    # handle output location
    # cleanup temp files
```

### 2. TypeScript Layer

#### `src/tts.ts` (from atenea)
- Keep exactly as is
- Already has caching
- Already works perfectly

#### `src/video-generator.ts` (simplified)
```typescript
export async function generateVideo(params) {
  // 1. Call hallo2_inference.py
  // 2. Stream output
  // 3. Return video path
  // Simple - no model selection needed
}
```

#### `src/cli.ts` (simplified)
```typescript
program
  .command('generate')
  .option('-i, --input <file>', 'Input text')
  .option('-a, --avatar <image>', 'Avatar image')
  .option('-v, --voice <voice>', 'TTS voice')
  .option('--fps <number>', 'Frame rate', '25')
  .option('--steps <number>', 'Inference steps', '40')
  .action(async (options) => {
    // 1. Read input text
    // 2. Generate speech (TTS)
    // 3. Generate video (Hallo2)
    // 4. Done!
  });
```

---

## Setup Script

### `scripts/setup.sh`
```bash
#!/bin/bash
# One-command setup for atenea-hallo2

# 1. Install system deps (ffmpeg)
# 2. Install Node.js deps
# 3. Create Python venv
# 4. Install Python deps
# 5. Clone Hallo2 official repo
# 6. Download models (~8GB)
# 7. Create default config
# 8. Done!
```

---

## Configuration

### Default Config (`configs/default.yaml`)
```yaml
# Hallo2 default configuration
fps: 25
seed: 42
num_inference_steps: 40  # 40=balanced, 50=high quality
guidance_scale: 3.5
width: 512
height: 512
pose_weight: 1.0
face_weight: 1.0
lip_weight: 1.0
face_expand_ratio: 1.2
```

Users can override via CLI:
```bash
npm run generate -- --steps 50 --fps 30
```

---

## Dependencies

### Python (`requirements.txt`)
```
# Core Hallo2 deps (from official repo)
torch>=2.0.0
diffusers
transformers
accelerate
safetensors
omegaconf
einops
opencv-python
mediapipe
insightface
librosa
moviepy
av
ffmpeg-python

# Our additions
pyyaml  # for config generation
```

### Node.js (`package.json`)
```json
{
  "dependencies": {
    "commander": "^12.1.0",
    "chalk": "^5.3.0",
    "ora": "^8.1.1",
    "openai": "^4.77.3",
    "dotenv": "^16.4.7"
  }
}
```

---

## Testing Strategy

### Unit Tests
1. `audio_converter.py` - test MP3→WAV conversion
2. `config_generator.py` - test YAML generation
3. `tts.ts` - test caching logic

### Integration Test
```bash
# Full end-to-end test
echo "Test video generation" > test.txt
npm run generate -- -i test.txt
# Should produce output.mp4
```

### RunPod Test
1. Clone repo on RunPod
2. Run setup.sh
3. Generate test video
4. Measure: time, VRAM, quality
5. Document actual performance

---

## Documentation

### README.md
- Quick start (5-minute setup)
- Usage examples
- Troubleshooting
- Performance benchmarks (actual, not estimates)

### SETUP.md
- Detailed setup for RunPod
- Detailed setup for local NVIDIA GPU
- Model download instructions

### API.md
- CLI options reference
- Configuration YAML reference
- Python API reference (if exposing)

---

## Migration Path

### For Current Atenea Users

**Keep atenea repo for SadTalker:**
```bash
# Fast, proven, works
cd atenea
npm run generate  # 3-4 min, good quality
```

**Use atenea-hallo2 for professional content:**
```bash
# Slower, excellent quality
cd atenea-hallo2
npm run generate  # 5-8 min, state-of-the-art
```

**Share resources:**
- Same avatar images (copy or symlink)
- Same .env file (OpenAI API key)
- Same input text files

---

## Timeline

### Phase 1: Core Implementation (4-6 hours)
- [ ] Create repo structure
- [ ] Port TTS integration
- [ ] Implement audio converter
- [ ] Implement config generator
- [ ] Implement hallo2_inference.py
- [ ] Create setup script
- [ ] Basic CLI

### Phase 2: Testing & Polish (2-3 hours)
- [ ] Test on RunPod RTX 4090
- [ ] Measure actual performance
- [ ] Write documentation
- [ ] Add error handling
- [ ] Create examples

### Phase 3: Release (1 hour)
- [ ] Final testing
- [ ] README with examples
- [ ] Push to GitHub
- [ ] Tag v1.0.0

**Total: 7-10 hours** (vs 4-6 hours for messy integration into atenea)

---

## Success Criteria

### Must Have
- ✅ Generate 512x512 video from text input
- ✅ Use OpenAI TTS
- ✅ Cache audio to save costs
- ✅ Work on RunPod RTX 4090
- ✅ < 8 minutes for 60s video
- ✅ Professional quality output

### Nice to Have
- Custom avatar images
- Voice selection
- Resolution options
- FPS options
- Inference steps tuning

### Out of Scope (for v1.0)
- Multi-model support (just Hallo2)
- Local Mac support (CUDA only)
- Video editing features
- Batch processing
- Web UI

---

## Next Steps

1. **Create new repo:**
   ```bash
   cd ~/code
   mkdir atenea-hallo2
   cd atenea-hallo2
   git init
   ```

2. **Copy proven code from atenea:**
   - src/tts.ts (exact copy)
   - src/cli.ts (simplified)
   - package.json (minimal)

3. **Implement Hallo2-specific code:**
   - python/audio_converter.py
   - python/config_generator.py
   - python/hallo2_inference.py

4. **Test on RunPod:**
   - Full end-to-end
   - Measure actual performance
   - Document findings

5. **Polish & release:**
   - Documentation
   - Examples
   - GitHub README

---

## Decision Log

| Decision | Rationale |
|----------|-----------|
| New repo vs refactor | Clean separation, less risk |
| Keep TTS/caching | Proven, works well |
| Subprocess vs import | Simpler, more maintainable |
| CUDA-only | Focus on quality (RunPod/GPU) |
| Single model | Complexity reduction |
| TypeScript + Python | Best tool for each layer |

---

**Ready to proceed?**
This plan gives us a professional, maintainable Hallo2 implementation without the baggage of multi-model support.
