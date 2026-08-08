#!/usr/bin/env python3
"""
Force Godot to import the Iron Giant GLB by modifying the .import file
and triggering a full reimport cycle.
"""

import os
import subprocess
import time
import shutil

GODOT_PATH = r"D:\xdev\Oasis\Godot4.exe"
PROJECT_PATH = r"D:\xdev\Oasis"
GLB_PATH = r"D:\xdev\Oasis\assets\iron_giant\3d_iron_giant_assignment.glb"
IMPORT_PATH = GLB_PATH + ".import"
IMPORTED_DIR = r"D:\xdev\Oasis\.godot\imported"

def cleanup_old_imports():
    """Remove any old import files for this GLB."""
    for filename in os.listdir(IMPORTED_DIR):
        if "iron_giant" in filename.lower():
            filepath = os.path.join(IMPORTED_DIR, filename)
            try:
                os.remove(filepath)
                print(f"  Removed: {filename}")
            except Exception as e:
                print(f"  Error removing {filename}: {e}")

def create_import_file():
    """Create a valid .import file."""
    import hashlib
    
    with open(GLB_PATH, 'rb') as f:
        glb_data = f.read()
    
    file_hash = hashlib.md5(glb_data).hexdigest()
    
    import_content = f"""[remap]

importer="gltf2"
importer_version=2
type="PackedScene"
uid="uid://d3xmk4ypwqmjh"
path="res://.godot/imported/3d_iron_giant_assignment.glb-{file_hash}.scn"

[deps]

source_file="res://assets/iron_giant/3d_iron_giant_assignment.glb"
dest_files=["res://.godot/imported/3d_iron_giant_assignment.glb-{file_hash}.scn"]

[params]

meshes/ensure_tangents=false
meshes/generate_lods=true
meshes/create_shadow_meshes=false
skins/use_named_skins=true
animation/import=true
animation/bake_reset_animation=false
animation/fps=30
animation/trimming=false
animation/remove_immutable_tracks=true
reimport_skeleton_bones=false
meshes/lightmap_texel_size=0.2
"""
    
    with open(IMPORT_PATH, 'w') as f:
        f.write(import_content)
    
    print(f"✓ Created .import file with hash: {file_hash}")
    return file_hash

def launch_godot_import():
    """Launch Godot to trigger the import."""
    print("\n▶ Launching Godot import...")
    
    # Kill any existing Godot instances
    os.system("taskkill /f /im Godot4.exe 2>nul")
    time.sleep(1)
    
    # Launch Godot with import flag
    proc = subprocess.Popen([
        GODOT_PATH,
        "--headless",
        "--import",
        PROJECT_PATH
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for import to complete
    time.sleep(8)
    
    # Kill Godot
    os.system("taskkill /f /im Godot4.exe 2>nul")
    print("✓ Import process completed")

def verify_import():
    """Check if the import was successful."""
    for filename in os.listdir(IMPORTED_DIR):
        if "iron_giant" in filename.lower() and filename.endswith(".scn"):
            print(f"✓ Import successful! Found: {filename}")
            return True
    
    print("⚠ Import file not found - Godot may not have generated it")
    return False

if __name__ == "__main__":
    print("=" * 60)
    print("Force Iron Giant GLB Import")
    print("=" * 60)
    
    print("\n1. Cleaning up old imports...")
    cleanup_old_imports()
    
    print("\n2. Creating .import file...")
    create_import_file()
    
    print("\n3. Launching Godot import...")
    launch_godot_import()
    
    print("\n4. Verifying import...")
    verify_import()
    
    print("\n" + "=" * 60)
    print("Import process complete!")
    print("=" * 60)
