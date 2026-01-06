#!/usr/bin/env python3
"""
Configuration generator for Hallo2
Generates YAML config files from CLI parameters
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

import yaml


def generate_config(
    source_image: str,
    audio_wav: str,
    output_path: str,
    resolution: int = 512,
    fps: int = 25,
    steps: int = 40,
    seed: int = 42,
    guidance_scale: float = 3.5,
    pose_weight: float = 1.0,
    face_weight: float = 1.0,
    lip_weight: float = 1.0,
    face_expand_ratio: float = 1.2,
) -> dict:
    """
    Generate Hallo2 configuration dictionary

    Args:
        source_image: Path to source avatar image
        audio_wav: Path to audio WAV file
        output_path: Path for output video
        resolution: Video width/height (512, 768, 1024)
        fps: Frames per second (25, 30)
        steps: Number of inference steps (40=balanced, 50=high quality)
        seed: Random seed for reproducibility
        guidance_scale: Classifier-free guidance scale
        pose_weight: Weight for pose control
        face_weight: Weight for face control
        lip_weight: Weight for lip sync control
        face_expand_ratio: Face region expansion ratio

    Returns:
        Configuration dictionary
    """
    config = {
        'source_image': str(Path(source_image).resolve()),
        'driving_audio': str(Path(audio_wav).resolve()),
        'output': str(Path(output_path).resolve()),
        'fps': fps,
        'seed': seed,
        'num_inference_steps': steps,
        'guidance_scale': guidance_scale,
        'width': resolution,
        'height': resolution,
        'pose_weight': pose_weight,
        'face_weight': face_weight,
        'lip_weight': lip_weight,
        'face_expand_ratio': face_expand_ratio,
    }

    return config


def save_config(config: dict, config_path: str) -> bool:
    """
    Save configuration to YAML file

    Args:
        config: Configuration dictionary
        config_path: Path to save YAML file

    Returns:
        True if successful, False otherwise
    """
    try:
        config_file = Path(config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)

        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        print(f"✅ Config generated: {config_path}")
        return True

    except Exception as e:
        print(f"❌ Error: Failed to save config: {str(e)}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Generate Hallo2 configuration file'
    )
    parser.add_argument('--image', required=True, help='Source avatar image')
    parser.add_argument('--audio', required=True, help='Audio WAV file')
    parser.add_argument('--output', required=True, help='Output video path')
    parser.add_argument('--config', required=True, help='Output config path')
    parser.add_argument('--resolution', type=int, default=512, help='Video resolution (512, 768, 1024)')
    parser.add_argument('--fps', type=int, default=25, help='Frames per second')
    parser.add_argument('--steps', type=int, default=40, help='Inference steps (40=balanced, 50=high quality)')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')

    args = parser.parse_args()

    config = generate_config(
        source_image=args.image,
        audio_wav=args.audio,
        output_path=args.output,
        resolution=args.resolution,
        fps=args.fps,
        steps=args.steps,
        seed=args.seed,
    )

    success = save_config(config, args.config)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
