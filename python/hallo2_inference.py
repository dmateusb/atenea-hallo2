#!/usr/bin/env python3
"""
Hallo2 Inference Script
Orchestrates Hallo2 video generation with audio conversion and config generation
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from audio_converter import convert_to_wav
from config_generator import generate_config, save_config


def find_hallo2_script() -> Path:
    """
    Find the Hallo2 inference script
    Looks in: hallo2/scripts/inference_long.py

    Returns:
        Path to inference script

    Raises:
        FileNotFoundError if script not found
    """
    # Try relative to project root
    script_paths = [
        Path(__file__).parent.parent / 'hallo2' / 'scripts' / 'inference_long.py',
        Path(__file__).parent.parent / 'hallo2' / 'scripts' / 'inference.py',
    ]

    for script_path in script_paths:
        if script_path.exists():
            return script_path

    raise FileNotFoundError(
        "❌ Hallo2 inference script not found. "
        "Please ensure hallo2/ directory exists with scripts/inference_long.py"
    )


def run_hallo2_inference(config_path: str, hallo2_script: Path) -> bool:
    """
    Run Hallo2 inference with generated config

    Args:
        config_path: Path to YAML config file
        hallo2_script: Path to Hallo2 inference script

    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"\n🎬 Running Hallo2 inference...")
        print(f"📝 Config: {config_path}")
        print(f"🐍 Script: {hallo2_script}")

        cmd = [
            sys.executable,  # Use current Python interpreter
            str(hallo2_script),
            '--config', str(config_path)
        ]

        # Run Hallo2 inference
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        # Stream output in real-time
        for line in result.stdout.splitlines():
            print(line)

        if result.returncode == 0:
            print(f"✅ Hallo2 inference completed successfully")
            return True
        else:
            print(f"❌ Hallo2 inference failed with code {result.returncode}", file=sys.stderr)
            return False

    except Exception as e:
        print(f"❌ Error running Hallo2: {str(e)}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Hallo2 Video Generation - End-to-end pipeline'
    )
    parser.add_argument(
        '--image',
        required=True,
        help='Source avatar image path'
    )
    parser.add_argument(
        '--audio',
        required=True,
        help='Audio file path (MP3 or WAV)'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Output video path'
    )
    parser.add_argument(
        '--fps',
        type=int,
        default=25,
        help='Frames per second (default: 25)'
    )
    parser.add_argument(
        '--steps',
        type=int,
        default=40,
        help='Inference steps - 40=balanced, 50=high quality (default: 40)'
    )
    parser.add_argument(
        '--resolution',
        type=int,
        default=512,
        help='Video resolution (512, 768, 1024) (default: 512)'
    )

    args = parser.parse_args()

    # Validate input files exist
    image_path = Path(args.image)
    audio_path = Path(args.audio)

    if not image_path.exists():
        print(f"❌ Error: Image file not found: {args.image}", file=sys.stderr)
        sys.exit(1)

    if not audio_path.exists():
        print(f"❌ Error: Audio file not found: {args.audio}", file=sys.stderr)
        sys.exit(1)

    # Create temporary directory for intermediate files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Convert audio to WAV if needed
        if audio_path.suffix.lower() == '.mp3':
            wav_path = temp_path / 'audio.wav'
            print(f"\n🔄 Converting MP3 to WAV...")
            if not convert_to_wav(str(audio_path), str(wav_path)):
                print(f"❌ Audio conversion failed", file=sys.stderr)
                sys.exit(1)
        elif audio_path.suffix.lower() == '.wav':
            wav_path = audio_path
            print(f"✅ Using WAV audio: {audio_path}")
        else:
            print(f"❌ Error: Unsupported audio format: {audio_path.suffix}", file=sys.stderr)
            print(f"   Supported formats: MP3, WAV", file=sys.stderr)
            sys.exit(1)

        # Generate Hallo2 config
        config_path = temp_path / 'hallo2_config.yaml'
        print(f"\n📝 Generating Hallo2 configuration...")

        config = generate_config(
            source_image=str(image_path),
            audio_wav=str(wav_path),
            output_path=args.output,
            resolution=args.resolution,
            fps=args.fps,
            steps=args.steps,
        )

        if not save_config(config, str(config_path)):
            print(f"❌ Config generation failed", file=sys.stderr)
            sys.exit(1)

        # Find Hallo2 inference script
        try:
            hallo2_script = find_hallo2_script()
        except FileNotFoundError as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)

        # Run Hallo2 inference
        if not run_hallo2_inference(str(config_path), hallo2_script):
            print(f"❌ Video generation failed", file=sys.stderr)
            sys.exit(1)

        # Verify output was created
        output_path = Path(args.output)
        if not output_path.exists():
            print(f"❌ Error: Output video not created: {args.output}", file=sys.stderr)
            sys.exit(1)

        print(f"\n✅ Video generation complete!")
        print(f"📹 Output: {args.output}")


if __name__ == '__main__':
    main()
