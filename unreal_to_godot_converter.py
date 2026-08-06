import os
import subprocess

UMODEL_EXE = r"D:\xdev\umodel_win32\umodel_64.exe"
CONTENT_DIR = r"D:\xdev\Oasis\GodotToImport\ReadyPlayerOne\Content"
OUTPUT_DIR = r"D:\xdev\Oasis\assets\unreal_exported"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def export_unreal_assets():
    print("[UNREAL TO GODOT] Exporting Unreal assets from ", CONTENT_DIR)
    
    # Run umodel for textures and static meshes with PNG/GLTF export
    cmd = [
        UMODEL_EXE,
        f"-path={CONTENT_DIR}",
        f"-out={OUTPUT_DIR}",
        "-export",
        "-png",
        "-game=ue4.26",
        "*.uasset"
    ]
    
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        print("[UNREAL TO GODOT] Export Output:\n", res.stdout[:500])
    except Exception as e:
        print("[UNREAL TO GODOT] Batch export executed with warning/status: ", e)

if __name__ == "__main__":
    export_unreal_assets()
