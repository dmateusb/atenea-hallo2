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

Follow the instructions in `hallo2/README.md` to download pretrained models.

Typically, you'll need to download models to `hallo2/pretrained_models/`.

### 4. Prepare Your Assets

- Add an avatar image to `data/images/avatar.png`
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
| `--steps <number>` | Inference steps (40=balanced, 50=high quality) | `40` |

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

## Performance

- RTX 4090: ~5-8 minutes for 1-minute video
- RTX 3090: ~8-12 minutes for 1-minute video
- CPU only: Not recommended (very slow)

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

1. **Avatar Images**: Use high-quality frontal face photos with clear features
2. **Text Input**: Keep sentences natural and conversational for best lip sync
3. **Audio Caching**: The system automatically caches generated audio files to avoid redundant OpenAI API calls
4. **Steps Parameter**: Use 40 steps for balanced quality/speed, 50 for higher quality

## Credits

- [Hallo2](https://github.com/fudan-generative-vision/hallo2) - Video generation
- [OpenAI](https://openai.com) - Text-to-Speech API

## License

MIT

## Support

For issues and questions, please open an issue on GitHub.
