# Atenea-Hallo2

AI Avatar Video Generator using Hallo2 - Professional talking head videos with natural expressions and lip sync.

## Features

- **Text-to-Speech**: OpenAI TTS with voice selection (nova, alloy, echo, fable, onyx, shimmer)
- **Audio Caching**: Deterministic hash-based caching to avoid regenerating identical audio
- **Hallo2 Integration**: State-of-the-art video generation with natural expressions and lip movements
- **Simple CLI**: Easy-to-use command-line interface
- **Automated Pipeline**: End-to-end orchestration from text to video

## Prerequisites

- Node.js 20+
- Python 3.10+
- ffmpeg
- CUDA-capable GPU (recommended for faster generation)
- OpenAI API key

## Quick Start

### 1. Installation

Run the automated setup script:

```bash
npm run setup
```

This will:
- Install Node.js dependencies
- Create Python virtual environment
- Install Python dependencies
- Clone Hallo2 repository
- Install Hallo2 dependencies
- Create necessary directories

### 2. Configuration

Edit `.env` file and add your OpenAI API key:

```bash
OPENAI_API_KEY=sk-your-key-here
TTS_VOICE=nova
TTS_MODEL=tts-1
```

### 3. Download Hallo2 Models

Download all required pretrained models from HuggingFace:

```bash
npm run download-models
```

This will download ~10GB of models including:
- InsightFace models for face analysis
- Hallo2 checkpoints
- Stable Diffusion v1.5
- Audio separator models
- Wav2vec models
- And other required dependencies

**Note**: This download may take 10-30 minutes depending on your internet speed.

### 4. Prepare Your Assets

- Add an avatar image to `data/images/avatar.png`
  - Use a high-quality frontal face photo
  - Square aspect ratio (will be resized to 512x512)
  - Face should occupy 50-70% of the image
  - Rotation angle less than 30° (no side profiles)
- Create a text file `input.txt` with your script

### 5. Generate Video

```bash
npm run generate
```

Or with custom options:

```bash
npm run generate -- \
  --input input.txt \
  --avatar data/images/avatar.png \
  --output output.mp4 \
  --voice nova \
  --fps 25 \
  --steps 40
```

## CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --input <file>` | Input text file | `input.txt` |
| `-a, --avatar <image>` | Avatar image path | `data/images/avatar.png` |
| `-o, --output <file>` | Output video path | `output.mp4` |
| `-v, --voice <voice>` | TTS voice | `nova` |
| `--fps <number>` | Frame rate | `25` |
| `--steps <number>` | Inference steps (20=fast, 40=balanced, 50=high quality) | `40` |
| `--lip-weight <number>` | Lip sync strength (1.0=default, 1.5-2.0=stronger) | `1.0` |
| `--cfg-scale <number>` | Guidance scale for audio adherence | `3.5` |

### Available TTS Voices

- `nova` - Balanced and natural (default)
- `alloy` - Neutral and clear
- `echo` - Male voice
- `fable` - British accent
- `onyx` - Deep male voice
- `shimmer` - Soft female voice

## Architecture

### TypeScript Layer (src/)
- `cli.ts` - Command-line interface
- `tts.ts` - OpenAI TTS with caching
- `video-generator.ts` - Python process orchestration
- `types.ts` - TypeScript type definitions

### Python Layer (python/)
- `hallo2_inference.py` - Main orchestration script
- `audio_converter.py` - MP3 to WAV conversion (16kHz mono)
- `config_generator.py` - YAML config generation for Hallo2

### Pipeline Flow

```
Text Input → OpenAI TTS → MP3 Audio → WAV Conversion → Hallo2 Config → Hallo2 Inference → Output Video
```

## Performance & Speed Optimization

### Generation Times (Approximate)
- RTX 4090: ~10-20 minutes for 1-minute video (40 steps)
- RTX 3090: ~15-30 minutes for 1-minute video (40 steps)
- CPU only: Not recommended (extremely slow)

### Speed vs Quality Trade-offs

**Fast Mode (2-3x faster)**
```bash
npm run generate -- --steps 20 --resolution 512
```
- ~5-10 minutes for 1-minute video on RTX 4090
- Good for testing and previews
- Slightly less smooth lip sync

**Balanced Mode (Default)**
```bash
npm run generate -- --steps 40 --resolution 512
```
- ~10-20 minutes for 1-minute video on RTX 4090
- Best quality/speed balance
- Natural lip movements

**High Quality Mode (Slower)**
```bash
npm run generate -- --steps 50 --resolution 768
```
- ~20-40 minutes for 1-minute video on RTX 4090
- Best lip sync accuracy
- Higher resolution output

### Key Speed Factors

1. **Inference Steps** - Biggest impact on speed
   - 20 steps: ~50% faster, slight quality reduction
   - 40 steps: Balanced (default)
   - 50+ steps: ~25% slower, marginal quality improvement

2. **Resolution** - Affects both speed and VRAM
   - 512x512: Fastest, lowest VRAM (recommended)
   - 768x768: ~40% slower, moderate VRAM
   - 1024x1024: ~2x slower, high VRAM (24GB+ GPU)

3. **Video Length** - Linear scaling
   - Each second of audio adds proportional generation time
   - Keep test videos under 30 seconds for faster iteration

## Project Structure

```
atenea-hallo2/
├── src/                    # TypeScript source
│   ├── cli.ts             # CLI interface
│   ├── tts.ts             # TTS generation
│   ├── video-generator.ts # Video orchestration
│   └── types.ts           # Type definitions
├── python/                # Python scripts
│   ├── hallo2_inference.py    # Main inference script
│   ├── audio_converter.py     # Audio conversion
│   └── config_generator.py    # Config generation
├── scripts/               # Setup scripts
│   └── setup.sh          # Automated setup
├── data/                  # Data directories
│   ├── images/           # Avatar images
│   ├── audio/            # Generated audio (cached)
│   └── videos/           # Output videos
├── configs/              # Generated YAML configs
└── hallo2/              # Hallo2 repository (cloned)
```

## Troubleshooting

### ffmpeg not found

Install ffmpeg:
- macOS: `brew install ffmpeg`
- Ubuntu: `sudo apt-get install ffmpeg`
- Windows: Download from [ffmpeg.org](https://ffmpeg.org)

### CUDA out of memory

Try reducing resolution:
```bash
npm run generate -- --resolution 512
```

### Hallo2 models not found

Make sure you've downloaded the pretrained models to `hallo2/pretrained_models/`.

See `hallo2/README.md` for download instructions.

### Python module not found

Activate the virtual environment and reinstall dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
cd hallo2
pip install -r requirements.txt
```

## Development

### Build TypeScript

```bash
npm run build
```

### Type Checking

```bash
npm run typecheck
```

### Format Code

```bash
npm run format
```

## Best Practices

### Avatar Image Quality
1. **High-quality frontal face photos** with clear features
2. **Square aspect ratio** - will be resized to 512x512
3. **Face占50-70% of image** - not too close, not too far
4. **Minimal rotation** - less than 30° rotation angle
5. **Good lighting** - even lighting on face, no harsh shadows
6. **Neutral expression** - slight smile works best as base

### Improving Lip Sync Quality

Based on HALLO2's cross-attention mechanism and patch-drop augmentation:

1. **Audio Quality is Critical**
   - Use clear, high-quality TTS voices (nova, alloy recommended)
   - Avoid background noise or music in audio
   - HALLO2's audio separator works best with clean vocals

2. **Increase Lip Weight** for stronger sync
   ```bash
   npm run generate -- --lip-weight 1.5
   ```
   - Default: 1.0 (natural)
   - Stronger: 1.5-2.0 (more pronounced lip movements)
   - Too high (>2.5): May look exaggerated

3. **Adjust Guidance Scale** for better audio adherence
   ```bash
   npm run generate -- --cfg-scale 4.0
   ```
   - Default: 3.5 (balanced)
   - Higher (4.0-5.0): Stricter audio-visual alignment
   - Lower (2.5-3.0): More creative freedom, less strict sync

4. **Increase Inference Steps** for smoother motion
   ```bash
   npm run generate -- --steps 50
   ```
   - More denoising iterations = smoother transitions
   - Diminishing returns beyond 50 steps

5. **Combine Settings** for best results
   ```bash
   npm run generate -- \
     --steps 50 \
     --lip-weight 1.5 \
     --cfg-scale 4.0 \
     --resolution 768
   ```

### General Best Practices

1. **Text Input**: Keep sentences natural and conversational for best lip sync
2. **Audio Caching**: The system automatically caches generated audio files to avoid redundant OpenAI API calls
3. **Testing Workflow**: Start with fast mode (--steps 20) for testing, then use high quality for final render
4. **VRAM Management**: If you get CUDA out of memory errors, reduce resolution to 512

## Credits

- [Hallo2](https://github.com/fudan-generative-vision/hallo2) - Video generation
- [OpenAI](https://openai.com) - Text-to-Speech API

## License

MIT

## Support

For issues and questions, please open an issue on GitHub.
