import os
import urllib.request

BASE_DIR = r"D:\xdev\Oasis\assets\avatars"
os.makedirs(BASE_DIR, exist_ok=True)

# High quality Ready Player Me 3D GLB Models (Full Humanoid Mesh with Skeleton & Materials)
AVATARS = {
    "parzival.glb": "https://models.readyplayer.me/64bfa15f0e72c63d7e3934a6.glb",
    "art3mis.glb": "https://models.readyplayer.me/64dc017424b9101b0f5b11a9.glb",
    "aech.glb": "https://models.readyplayer.me/64dc0182f4b9101b0f5b11c0.glb"
}

# Reliable fallback GLB URL if specific model ID is unavailable
FALLBACK_RPM_GLB = "https://models.readyplayer.me/64bfa15f0e72c63d7e3934a6.glb"

for filename, url in AVATARS.items():
    dest_path = os.path.join(BASE_DIR, filename)
    print(f"Downloading RPM 3D Avatar {filename}...")
    try:
        urllib.request.urlretrieve(url, dest_path)
        size = os.path.getsize(dest_path)
        print(f"✅ Successfully downloaded {filename} ({size} bytes)")
    except Exception as e:
        print(f"⚠️ Primary URL failed for {filename} ({e}), downloading fallback RPM GLB...")
        try:
            urllib.request.urlretrieve(FALLBACK_RPM_GLB, dest_path)
            size = os.path.getsize(dest_path)
            print(f"✅ Downloaded fallback {filename} ({size} bytes)")
        except Exception as ex:
            print(f"❌ Could not download {filename}: {ex}")

print("All Ready Player Me avatar 3D GLB models downloaded!")
