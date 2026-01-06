#!/usr/bin/env python3
"""
Download Hallo2 pretrained models from HuggingFace
"""

import sys
from pathlib import Path
from huggingface_hub import snapshot_download


def main():
    """Download all Hallo2 pretrained models"""
    print("🚀 Downloading Hallo2 pretrained models from HuggingFace...")
    print("This may take a while (several GB of data)\n")

    try:
        repo_id = "fudan-generative-ai/hallo2"
        local_dir = Path(__file__).parent.parent / "pretrained_models"

        print(f"📥 Downloading from: {repo_id}")
        print(f"📁 Saving to: {local_dir}\n")

        snapshot_download(
            repo_id=repo_id,
            local_dir=str(local_dir),
            local_dir_use_symlinks=False,
            resume_download=True,
        )

        print("\n✅ Download complete!")
        print(f"Models saved to: {local_dir}")

    except Exception as e:
        print(f"\n❌ Error downloading models: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
