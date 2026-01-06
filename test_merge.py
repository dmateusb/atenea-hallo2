
import sys
import os
from pathlib import Path

# Add hallo2 directory to path
sys.path.append(os.path.join(os.getcwd(), 'hallo2'))

from hallo.utils.util import merge_videos

def run_merge():
    input_dir = "/workspace/atenea-hallo2/avatar/seg_video"
    output_file = "/workspace/atenea-hallo2/output_fixed.mp4"
    
    print(f"Merging videos from {input_dir} to {output_file}...")
    try:
        merge_videos(input_dir, output_file)
        print("✅ Merge complete!")
    except Exception as e:
        print(f"❌ Merge failed: {e}")

if __name__ == "__main__":
    run_merge()
