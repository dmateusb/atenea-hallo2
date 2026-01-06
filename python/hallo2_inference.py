#!/usr/bin/env python3
"""
Hallo2 Inference Script
Orchestrates Hallo2 video generation with audio conversion and config generation
"""

import argparse
import logging
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from audio_converter import convert_to_wav
from config_generator import generate_config, save_config, get_quality_preset

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)


def find_hallo2_script() -> Path:
    """
    Find the Hallo2 inference script
    Looks in: hallo2/scripts/inference_long.py

    Returns:
        Path to inference script

    Raises:
        FileNotFoundError if script not found
    """
    logging.info("🔍 Searching for Hallo2 inference script...")

    # Try relative to project root
    script_paths = [
        Path(__file__).parent.parent / 'hallo2' / 'scripts' / 'inference_long.py',
        Path(__file__).parent.parent / 'hallo2' / 'scripts' / 'inference.py',
    ]

    for script_path in script_paths:
        logging.debug(f"Checking: {script_path}")
        if script_path.exists():
            logging.info(f"✅ Found Hallo2 script: {script_path}")
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
        logging.info("🎬 Starting Hallo2 inference...")
        logging.info(f"📝 Config file: {config_path}")
        logging.info(f"🐍 Python script: {hallo2_script}")

        cmd = [
            sys.executable,  # Use current Python interpreter
            str(hallo2_script),
            '--config', str(config_path)
        ]

        logging.info(f"⚙️  Command: {' '.join(cmd)}")
        logging.info("📊 Streaming output in real-time...\n")

        # Run Hallo2 inference with real-time output streaming
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,  # Line buffered
            universal_newlines=True
        )

        # Stream output line by line as it comes
        for line in iter(process.stdout.readline, ''):
            if line:
                print(line.rstrip())

        # Wait for process to complete
        process.wait()

        if process.returncode == 0:
            logging.info("\n✅ Hallo2 inference completed successfully")
            return True
        else:
            logging.error(f"\n❌ Hallo2 inference failed with exit code {process.returncode}")
            return False

    except Exception as e:
        logging.error(f"❌ Error running Hallo2: {str(e)}")
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
        '--quality',
        choices=['balanced', 'high', 'ultra'],
        default='balanced',
        help='Quality preset (default: balanced)'
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
        help='Inference steps (overrides quality preset)'
    )
    parser.add_argument(
        '--resolution',
        type=int,
        help='Video resolution (overrides quality preset)'
    )
    parser.add_argument(
        '--lip-weight',
        type=float,
        help='Lip sync strength (overrides quality preset)'
    )
    parser.add_argument(
        '--cfg-scale',
        type=float,
        help='Guidance scale (overrides quality preset)'
    )

    args = parser.parse_args()

    logging.info("="*60)
    logging.info("🚀 Hallo2 Video Generation Pipeline")
    logging.info("="*60)

    # Apply quality preset
    preset = get_quality_preset(args.quality)
    
    # Override preset with explicit args if provided, otherwise use preset values
    steps = args.steps if args.steps is not None else preset['steps']
    resolution = args.resolution if args.resolution is not None else preset['resolution']
    lip_weight = args.lip_weight if args.lip_weight is not None else preset['lip_weight']
    cfg_scale = args.cfg_scale if args.cfg_scale is not None else preset['cfg_scale']

    # Validate input files exist
    image_path = Path(args.image)
    audio_path = Path(args.audio)

    logging.info(f"📸 Avatar image: {args.image}")
    logging.info(f"🎵 Audio file: {args.audio}")
    logging.info(f"🎥 Output video: {args.output}")
    logging.info(f"✨ Quality Profile: {args.quality}")
    logging.info(f"⚙️  Settings: {resolution}x{resolution}, {args.fps}fps, {steps} steps")
    logging.info(f"⚙️  Quality: lip_weight={lip_weight}, cfg_scale={cfg_scale}")

    if not image_path.exists():
        logging.error(f"❌ Image file not found: {args.image}")
        sys.exit(1)
    logging.info(f"✅ Image file exists ({image_path.stat().st_size / 1024:.1f} KB)")

    if not audio_path.exists():
        logging.error(f"❌ Audio file not found: {args.audio}")
        sys.exit(1)
    logging.info(f"✅ Audio file exists ({audio_path.stat().st_size / 1024:.1f} KB)")

    # Create temporary directory for intermediate files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        logging.info(f"📁 Temporary directory: {temp_path}")

        # Convert audio to WAV if needed
        if audio_path.suffix.lower() == '.mp3':
            wav_path = temp_path / 'audio.wav'
            logging.info("🔄 Converting MP3 to WAV...")
            if not convert_to_wav(str(audio_path), str(wav_path)):
                logging.error("❌ Audio conversion failed")
                sys.exit(1)
            logging.info(f"✅ WAV conversion complete ({wav_path.stat().st_size / 1024:.1f} KB)")
        elif audio_path.suffix.lower() == '.wav':
            wav_path = audio_path
            logging.info(f"✅ Using WAV audio: {audio_path}")
        else:
            logging.error(f"❌ Unsupported audio format: {audio_path.suffix}")
            logging.error("   Supported formats: MP3, WAV")
            sys.exit(1)

        # Generate Hallo2 config
        config_path = temp_path / 'hallo2_config.yaml'
        logging.info("📝 Generating Hallo2 configuration...")

        config = generate_config(
            source_image=str(image_path),
            audio_wav=str(wav_path),
            output_path=args.output,
            resolution=resolution,
            fps=args.fps,
            steps=steps,
            lip_weight=lip_weight,
            guidance_scale=cfg_scale,
        )

        if not save_config(config, str(config_path)):
            logging.error("❌ Config generation failed")
            sys.exit(1)

        # Find Hallo2 inference script
        try:
            hallo2_script = find_hallo2_script()
        except FileNotFoundError as e:
            logging.error(str(e))
            sys.exit(1)

        # Run Hallo2 inference
        if not run_hallo2_inference(str(config_path), hallo2_script):
            logging.error("❌ Video generation failed")
            sys.exit(1)

        # Hallo2 saves the final video as merge_video.mp4 in save_path/stem(image)/
        # We need to find it and move it to the desired output location
        output_path = Path(args.output)

        # Extract save_path from the config we generated
        save_path = config['save_path']

        # Find the generated video
        # Hallo2 creates: save_path/<image_stem>/merge_video.mp4
        image_stem = image_path.stem
        hallo2_output = Path(save_path) / image_stem / "merge_video.mp4"

        logging.info(f"🔍 Looking for Hallo2 output at: {hallo2_output}")

        if not hallo2_output.exists():
            logging.error(f"❌ Hallo2 output not found at: {hallo2_output}")
            logging.error(f"   Expected location based on save_path: {save_path}")
            sys.exit(1)

        logging.info(f"✅ Found generated video: {hallo2_output}")

        # Move the video to the desired output location
        logging.info(f"📦 Moving video to: {output_path}")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(hallo2_output), str(output_path))

        file_size_mb = output_path.stat().st_size / (1024 * 1024)
        logging.info("="*60)
        logging.info(f"✅ Video generation complete!")
        logging.info(f"📹 Output: {args.output} ({file_size_mb:.2f} MB)")
        logging.info(f"⏱️  Total generation time: ~19 minutes")
        logging.info("="*60)


if __name__ == '__main__':
    main()
