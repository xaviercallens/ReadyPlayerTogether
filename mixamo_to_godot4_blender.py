# Mixamo to Godot 4 Automated Blender Pipeline
# Based on bogdanMerkulow/MixamoToGodot
# Run in Blender: blender --background --python mixamo_to_godot4_blender.py -- <input_folder> <output_folder>

import bpy
import sys
import os

def convert_mixamo_fbx_to_glb(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    fbx_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.fbx')]
    print(f"[MixamoToGodot] Found {len(fbx_files)} FBX files to process.")
    
    for fbx_file in fbx_files:
        # Clear existing mesh objects
        bpy.ops.wm.read_factory_settings(use_empty=True)
        
        fbx_path = os.path.join(input_dir, fbx_file)
        print(f"[MixamoToGodot] Importing {fbx_file}...")
        bpy.ops.import_scene.fbx(filepath=fbx_path)
        
        # Rename mixamorig armature if needed for Godot 4 SkeletonProfileHumanoid
        for obj in bpy.context.scene.objects:
            if obj.type == 'ARMATURE':
                obj.name = "GeneralSkeleton"
                
        # Export as GLB with animation and root motion setup
        glb_name = os.path.splitext(fbx_file)[0] + ".glb"
        glb_path = os.path.join(output_dir, glb_name)
        
        bpy.ops.export_scene.gltf(
            filepath=glb_path,
            export_format='GLB',
            export_animations=True,
            export_current_frame=False
        )
        print(f"[MixamoToGodot] Exported -> {glb_path}")

if __name__ == "__main__":
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    in_dir = args[0] if len(args) > 0 else "./mixamo_raw"
    out_dir = args[1] if len(args) > 1 else "./assets/animations"
    if os.path.exists(in_dir):
        convert_mixamo_fbx_to_glb(in_dir, out_dir)
    else:
        print(f"[MixamoToGodot] Input folder '{in_dir}' does not exist yet. Pipeline ready.")
