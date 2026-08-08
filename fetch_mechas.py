#!/usr/bin/env python3
"""
Fetch Iron Giant and MechaGodzilla GLB files from Google Drive.
"""

import os
import gdown

# Google Drive folder containing the GLB files
DRIVE_URL = "https://drive.google.com/drive/folders/134-vXOihpwAHnxeEz7hi88wh9VIx5CD7"
DOWNLOAD_DIR = r"D:\xdev\Oasis\GodotToImport"

def download_assets():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    print("🤖 [OASIS Pipeline] Connecting to Google Drive...")
    
    try:
        gdown.download_folder(url=DRIVE_URL, output=DOWNLOAD_DIR, quiet=False, remaining_ok=True)
        print(f"✅ Download complete. GLB files are in {DOWNLOAD_DIR}")
    except Exception as e:
        print(f"❌ Download failed: {e}")
        print(f"⚠️  Make sure the folder is publicly accessible or you have the correct URL")

if __name__ == "__main__":
    download_assets()
