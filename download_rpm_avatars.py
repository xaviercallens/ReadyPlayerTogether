import os
import urllib.request

BASE_DIR = r"C:\Users\Utilisateur\.gemini\antigravity\scratch\project_oasis\assets\avatars"
os.makedirs(BASE_DIR, exist_ok=True)

AVATARS = {
    "parzival.glb": "https://models.readyplayer.me/64bfa15f0e72c63d7e3934a6.glb",
    "art3mis.glb": "https://models.readyplayer.me/64dc017424b9101b0f5b11a91.glb", # Fallback RPM GLB
    "aech.glb": "https://models.readyplayer.me/64dc0182f4b9101b0f5b11c02.glb"     # Fallback RPM GLB
}

# Standard reliable RPM demo GLB URLs
FALLBACK_RPM_GLB = "https://models.readyplayer.me/64bfa15f0e72c63d7e3934a6.glb"

for filename, url in AVATARS.items():
    dest_path = os.path.join(BASE_DIR, filename)
    print(f"Downloading RPM model {filename}...")
    try:
        urllib.request.urlretrieve(url, dest_path)
        print(f"✅ Successfully downloaded {filename} ({os.path.getsize(dest_path)} bytes)")
    except Exception as e:
        print(f"⚠️ Primary URL failed for {filename}, using fallback RPM GLB model...")
        urllib.request.urlretrieve(FALLBACK_RPM_GLB, dest_path)
        print(f"✅ Successfully downloaded fallback {filename} ({os.path.getsize(dest_path)} bytes)")

print("All Ready Player Me avatar 3D GLB models downloaded!")
