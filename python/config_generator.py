#!/usr/bin/env python3
"""
Configuration generator for Hallo2
Generates YAML config files from CLI parameters
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

import yaml

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)


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
    Generate Hallo2 configuration dictionary matching the expected format
    from hallo2/configs/inference/long.yaml

    Args:
        source_image: Path to source avatar image
        audio_wav: Path to audio WAV file
        output_path: Path for output video (parent directory will be used as save_path)
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
        Configuration dictionary matching Hallo2 expected format
    """
    # The save_path should be the directory where output will be saved
    # The script will create subdirectories within it
    output_file = Path(output_path)
    save_path = str(output_file.parent.resolve())

    config = {
        'source_image': str(Path(source_image).resolve()),
        'driving_audio': str(Path(audio_wav).resolve()),
        'weight_dtype': 'fp16',
        'data': {
            'n_motion_frames': 2,
            'n_sample_frames': 16,
            'source_image': {
                'width': resolution,
                'height': resolution,
            },
            'driving_audio': {
                'sample_rate': 16000,
            },
            'export_video': {
                'fps': fps,
            },
        },
        'inference_steps': steps,
        'cfg_scale': guidance_scale,
        'use_mask': True,
        'mask_rate': 0.25,
        'use_cut': True,
        'audio_ckpt_dir': './pretrained_models/hallo2',
        'save_path': save_path,
        'cache_path': './.cache',
        'base_model_path': './pretrained_models/stable-diffusion-v1-5',
        'motion_module_path': './pretrained_models/motion_module/mm_sd_v15_v2.ckpt',
        'face_analysis': {
            'model_path': './pretrained_models/face_analysis',
        },
        'wav2vec': {
            'model_path': './pretrained_models/wav2vec/wav2vec2-base-960h',
            'features': 'all',
        },
        'audio_separator': {
            'model_path': './pretrained_models/audio_separator/Kim_Vocal_2.onnx',
        },
        'vae': {
            'model_path': './pretrained_models/sd-vae-ft-mse',
        },
        'face_expand_ratio': face_expand_ratio,
        'pose_weight': pose_weight,
        'face_weight': face_weight,
        'lip_weight': lip_weight,
        'unet_additional_kwargs': {
            'use_inflated_groupnorm': True,
            'unet_use_cross_frame_attention': False,
            'unet_use_temporal_attention': False,
            'use_motion_module': True,
            'use_audio_module': True,
            'motion_module_resolutions': [1, 2, 4, 8],
            'motion_module_mid_block': True,
            'motion_module_decoder_only': False,
            'motion_module_type': 'Vanilla',
            'motion_module_kwargs': {
                'num_attention_heads': 8,
                'num_transformer_block': 1,
                'attention_block_types': ['Temporal_Self', 'Temporal_Self'],
                'temporal_position_encoding': True,
                'temporal_position_encoding_max_len': 32,
                'temporal_attention_dim_div': 1,
            },
            'audio_attention_dim': 768,
            'stack_enable_blocks_name': ['up', 'down', 'mid'],
            'stack_enable_blocks_depth': [0, 1, 2, 3],
        },
        'enable_zero_snr': True,
        'noise_scheduler_kwargs': {
            'beta_start': 0.00085,
            'beta_end': 0.012,
            'beta_schedule': 'linear',
            'clip_sample': False,
            'steps_offset': 1,
            'prediction_type': 'v_prediction',
            'rescale_betas_zero_snr': True,
            'timestep_spacing': 'trailing',
        },
        'sampler': 'DDIM',
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


def get_quality_preset(quality: str) -> dict:
    """
    Get settings for a specific quality preset
    
    Args:
        quality: One of 'balanced', 'high', 'ultra'
        
    Returns:
        Dictionary with resolution, steps, lip_weight, etc.
    """
    presets = {
        'balanced': {
            'resolution': 512,
            'steps': 40,
            'lip_weight': 1.0,
            'cfg_scale': 3.5,
        },
        'high': {
            'resolution': 768,
            'steps': 50,
            'lip_weight': 1.1,
            'cfg_scale': 3.8,
        },
        'ultra': {
            'resolution': 768,  # 768 is safer than 1024 for stability
            'steps': 60,
            'lip_weight': 1.0,
            'cfg_scale': 4.5,
        }
    }
    return presets.get(quality, presets['balanced'])


def main():
    parser = argparse.ArgumentParser(
        description='Generate Hallo2 configuration file'
    )
    parser.add_argument('--image', required=True, help='Source avatar image')
    parser.add_argument('--audio', required=True, help='Audio WAV file')
    parser.add_argument('--output', required=True, help='Output video path')
    parser.add_argument('--config', required=True, help='Output config path')
    parser.add_argument('--quality', choices=['balanced', 'high', 'ultra'], default='balanced', help='Quality preset')
    
    parser.add_argument('--resolution', type=int, help='Video resolution (overrides quality)')
    parser.add_argument('--fps', type=int, default=25, help='Frames per second')
    parser.add_argument('--steps', type=int, help='Inference steps (overrides quality)')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    parser.add_argument('--lip-weight', type=float, help='Lip weight (overrides quality)')
    parser.add_argument('--cfg-scale', type=float, help='Guidance scale (overrides quality)')

    args = parser.parse_args()

    # Apply quality preset
    preset = get_quality_preset(args.quality)
    
    # Override preset with explicit args if provided
    steps = args.steps if args.steps is not None else preset['steps']
    resolution = args.resolution if args.resolution is not None else preset['resolution']
    lip_weight = args.lip_weight if args.lip_weight is not None else preset['lip_weight']
    cfg_scale = args.cfg_scale if args.cfg_scale is not None else preset['cfg_scale']

    config = generate_config(
        source_image=args.image,
        audio_wav=args.audio,
        output_path=args.output,
        resolution=resolution,
        fps=args.fps,
        steps=steps,
        seed=args.seed,
        lip_weight=lip_weight,
        guidance_scale=cfg_scale,
    )

    success = save_config(config, args.config)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
