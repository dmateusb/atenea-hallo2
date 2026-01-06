#!/usr/bin/env python3
"""
Audio converter for Hallo2 - converts MP3 to WAV format
Hallo2 requires WAV audio at 16kHz mono for optimal speech processing
"""

import argparse
import subprocess
import sys
from pathlib import Path


def convert_to_wav(mp3_path: str, wav_path: str) -> bool:
    """
    Convert MP3 audio to WAV format using ffmpeg

    Args:
        mp3_path: Path to input MP3 file
        wav_path: Path to output WAV file

    Returns:
        True if conversion successful, False otherwise
    """
    mp3_file = Path(mp3_path)
    wav_file = Path(wav_path)

    # Validate input exists
    if not mp3_file.exists():
        print(f"❌ Error: Input MP3 file not found: {mp3_path}", file=sys.stderr)
        return False

    # Ensure output directory exists
    wav_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Convert to 16kHz mono WAV for speech processing
        # -ar 16000: sample rate 16kHz (standard for speech)
        # -ac 1: mono audio
        # -y: overwrite output file if exists
        cmd = [
            'ffmpeg',
            '-i', str(mp3_file),
            '-ar', '16000',
            '-ac', '1',
            '-y',
            str(wav_file)
        ]

        print(f"🔄 Converting {mp3_file.name} to WAV format...")

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )

        if wav_file.exists():
            print(f"✅ Audio converted: {wav_path}")
            return True
        else:
            print(f"❌ Error: Output file not created", file=sys.stderr)
            return False

    except subprocess.CalledProcessError as e:
        print(f"❌ Error: ffmpeg conversion failed: {e.stderr.decode()}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print(f"❌ Error: ffmpeg not found. Please install ffmpeg.", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Convert MP3 audio to WAV format for Hallo2'
    )
    parser.add_argument(
        '--input',
        required=True,
        help='Input MP3 file path'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Output WAV file path'
    )

    args = parser.parse_args()

    success = convert_to_wav(args.input, args.output)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
