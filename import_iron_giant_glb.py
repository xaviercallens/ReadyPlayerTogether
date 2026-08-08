#!/usr/bin/env python3
"""
Script to generate the correct .import file for the Iron Giant GLB
and trigger Godot to import it with the correct UID.
"""

import os
import hashlib
import subprocess
import time

GLB_PATH = r"D:\xdev\Oasis\assets\iron_giant\3d_iron_giant_assignment.glb"
IMPORT_PATH = GLB_PATH + ".import"
GODOT_PATH = r"D:\xdev\Oasis\Godot4.exe"
PROJECT_PATH = r"D:\xdev\Oasis"

def generate_import_file():
    """Generate a valid .import file for the GLB."""
    
    # Read the GLB file to generate a hash
    with open(GLB_PATH, 'rb') as f:
        glb_data = f.read()
    
    # Generate MD5 hash of the file
    file_hash = hashlib.md5(glb_data).hexdigest()
    
    # Create the import file content
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
    
    # Write the import file
    with open(IMPORT_PATH, 'w') as f:
        f.write(import_content)
    
    print(f"✓ Created {IMPORT_PATH}")
    print(f"  File hash: {file_hash}")
    return file_hash

def trigger_godot_import():
    """Launch Godot to trigger the import process."""
    print("\n▶ Launching Godot to import GLB...")
    
    # Kill any existing Godot instances
    os.system("taskkill /f /im Godot4.exe 2>nul")
    time.sleep(1)
    
    # Launch Godot with the project
    subprocess.Popen([
        GODOT_PATH,
        "--headless",
        "--import",
        PROJECT_PATH
    ])
    
    print("  Godot import process started...")
    time.sleep(5)
    
    # Kill Godot after import
    os.system("taskkill /f /im Godot4.exe 2>nul")
    print("✓ Import complete")

if __name__ == "__main__":
    print("=" * 60)
    print("Iron Giant GLB Import Generator")
    print("=" * 60)
    
    if not os.path.exists(GLB_PATH):
        print(f"✗ GLB file not found: {GLB_PATH}")
        exit(1)
    
    file_hash = generate_import_file()
    trigger_godot_import()
    
    print("\n" + "=" * 60)
    print("✓ Iron Giant GLB import setup complete!")
    print("=" * 60)
