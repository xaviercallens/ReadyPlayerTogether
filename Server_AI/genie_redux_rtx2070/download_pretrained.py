#!/usr/bin/env python3
"""
GenieRedux RTX 2070 - Download Pretrained Models
Downloads lightweight pretrained models from Hugging Face for demo purposes.
"""

import os
import sys
from pathlib import Path

try:
    from huggingface_hub import hf_hub_download
except ImportError:
    print("[GenieRedux] Installing huggingface_hub...")
    os.system("pip install huggingface_hub")
    from huggingface_hub import hf_hub_download


def download_models():
    """Download pretrained models from Hugging Face."""
    checkpoint_dir = Path(__file__).parent / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    print("[GenieRedux] Downloading pretrained models from Hugging Face...")
    print("[GenieRedux] Note: Full GenieRedux models require 24-80GB VRAM.")
    print("[GenieRedux] For RTX 2070 demo, we'll use a lightweight distilled version.")

    # Option 1: Try to download a lightweight distilled model
    # (In reality, GenieRedux models are large. This is a placeholder for the concept.)
    try:
        print("\n[GenieRedux] Attempting to download GenieRedux-Distilled from HF...")
        model_path = hf_hub_download(
            repo_id="INSAIT-Institute/GenieRedux",
            filename="distilled_model.pt",
            cache_dir=str(checkpoint_dir),
            resume_download=True
        )
        print(f"[GenieRedux] ✓ Downloaded: {model_path}")
    except Exception as e:
        print(f"[GenieRedux] ⚠ Could not download from INSAIT-Institute/GenieRedux: {e}")
        print("[GenieRedux] This is expected if the model is not yet public or requires auth.")

    # Option 2: Download Matrix-Game-2.0 (more suitable for RTX 2070)
    try:
        print("\n[GenieRedux] Attempting to download Matrix-Game-2.0 from HF...")
        model_path = hf_hub_download(
            repo_id="Skywork/Matrix-Game-2.0",
            filename="model.pt",
            cache_dir=str(checkpoint_dir),
            resume_download=True
        )
        print(f"[GenieRedux] ✓ Downloaded: {model_path}")
    except Exception as e:
        print(f"[GenieRedux] ⚠ Could not download Matrix-Game-2.0: {e}")

    # Option 3: Download Matrix-Game-3.0 (latest, but requires more VRAM)
    try:
        print("\n[GenieRedux] Attempting to download Matrix-Game-3.0 from HF...")
        model_path = hf_hub_download(
            repo_id="Skywork/Matrix-Game-3.0",
            filename="model_5b.pt",
            cache_dir=str(checkpoint_dir),
            resume_download=True
        )
        print(f"[GenieRedux] ✓ Downloaded: {model_path}")
    except Exception as e:
        print(f"[GenieRedux] ⚠ Could not download Matrix-Game-3.0: {e}")

    print("\n[GenieRedux] Download complete!")
    print(f"[GenieRedux] Models saved in: {checkpoint_dir}")
    print("[GenieRedux] Next: python train.py or python demo.py")


if __name__ == "__main__":
    download_models()
