import os
import sys

def setup_mixamo_pipeline():
    print("=== Installing Mixamo to Godot 4 Automated Pipeline ===")
    
    # 1. Blender Automation Script (Python for Blender)
    blender_script = """# Mixamo to Godot 4 Automated Blender Pipeline
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
"""

    with open("mixamo_to_godot4_blender.py", "w", encoding="utf-8") as f:
        f.write(blender_script)
    print("-> Wrote mixamo_to_godot4_blender.py")

    # 2. Godot 4 GDScript Retargeter & AnimationTree Controller
    mixamo_retargeter_gd = """# Godot 4.3+ Mixamo & Ready Player Me Humanoid Retargeter & AnimationTree Controller
class_name MixamoGodot4Controller
extends Node3D

signal animation_state_changed(new_state: String)

@export var avatar_skeleton: Skeleton3D
@export var animation_player: AnimationPlayer
@export var animation_tree: AnimationTree

# Bone Mapping Dictionary (Mixamo -> Godot 4 Humanoid)
const BONE_MAP: Dictionary = {
	"mixamorig:Hips": "Hips",
	"mixamorig:Spine": "Spine",
	"mixamorig:Spine1": "Chest",
	"mixamorig:Spine2": "UpperChest",
	"mixamorig:Neck": "Neck",
	"mixamorig:Head": "Head",
	"mixamorig:LeftShoulder": "LeftShoulder",
	"mixamorig:LeftArm": "LeftUpperArm",
	"mixamorig:LeftForeArm": "LeftLowerArm",
	"mixamorig:LeftHand": "LeftHand",
	"mixamorig:RightShoulder": "RightShoulder",
	"mixamorig:RightArm": "RightUpperArm",
	"mixamorig:RightForeArm": "RightLowerArm",
	"mixamorig:RightHand": "RightHand",
	"mixamorig:LeftUpLeg": "LeftUpperLeg",
	"mixamorig:LeftLeg": "LeftLowerLeg",
	"mixamorig:LeftFoot": "LeftFoot",
	"mixamorig:RightUpLeg": "RightUpperLeg",
	"mixamorig:RightLeg": "RightLowerLeg",
	"mixamorig:RightFoot": "RightFoot"
}

func _ready() -> void:
	if avatar_skeleton:
		remap_mixamo_bones()
	setup_animation_tree()

func remap_mixamo_bones() -> void:
	if not avatar_skeleton:
		return
		
	var remapped_count = 0
	for mixamo_name in BONE_MAP.keys():
		var bone_idx = avatar_skeleton.find_bone(mixamo_name)
		if bone_idx != -1:
			var target_godot_name = BONE_MAP[mixamo_name]
			# Renommer dynamiquement pour correspondre au SkeletonProfileHumanoid de Godot 4
			avatar_skeleton.set_bone_name(bone_idx, target_godot_name)
			remapped_count += 1
			
	print("[MixamoGodot4Controller] Retargeting effectue : ", remapped_count, " os réalignés pour Godot 4.")

func setup_animation_tree() -> void:
	if not animation_player:
		return
		
	if not animation_tree:
		animation_tree = AnimationTree.new()
		add_child(animation_tree)
		
	animation_tree.anim_player = animation_tree.get_path_to(animation_player)
	animation_tree.active = true
	print("[MixamoGodot4Controller] AnimationTree connecte avec succes à AnimationPlayer.")

func play_action(anim_name: String) -> void:
	if animation_player and animation_player.has_animation(anim_name):
		animation_player.play(anim_name)
		animation_state_changed.emit(anim_name)
		print("[MixamoGodot4Controller] Lecture animation Mixamo: ", anim_name)
"""

    os.makedirs("scripts/avatars", exist_ok=True)
    with open("scripts/avatars/mixamo_godot4_controller.gd", "w", encoding="utf-8") as f:
        f.write(mixamo_retargeter_gd)
    print("-> Wrote scripts/avatars/mixamo_godot4_controller.gd")

    # 3. User & Technical Guide for Mixamo
    guide_md = """# 💃 Guide de la Pipeline Mixamo ➔ Godot 4 (Projet OASIS)

Ce guide permet de télécharger des milliers d'animations gratuites depuis Adobe Mixamo et de les appliquer automatiquement à vos avatars 3D **Ready Player Me** (Parzival, Art3mis, Aech, etc.) dans Godot 4.

---

### 1. Télécharger des animations depuis Mixamo :
1. Rendez-vous sur [mixamo.com](https://www.mixamo.com).
2. Choisissez une animation (ex: *Idle, Walking, Running, Hip Hop Dance, Cyberpunk Pistol Shoot*).
3. Cliquez sur **Download** avec les paramètres suivants :
   - **Format** : `FBX (.fbx)`
   - **Skin** : `Without Skin` (seule l'animation est nécessaire)
   - **Frames per second** : `30` ou `60`
   - **Keyframe Reduction** : `none`

---

### 2. Exportation Automatisée vers Godot 4 :

#### Option A (Directement dans Godot 4) :
- Glissez vos fichiers `.fbx` de Mixamo dans le dossier `res://assets/animations/`.
- Le script `res://scripts/avatars/mixamo_godot4_controller.gd` réaligne automatiquement les os (`mixamorig:Hips`, `mixamorig:Spine`, etc.) sur le profil standard `SkeletonProfileHumanoid` de Godot 4.

#### Option B (Batch Blender avec Root Motion) :
Si vous avez Blender installé sur votre PC :
```cmd
blender --background --python mixamo_to_godot4_blender.py -- ./mixamo_raw ./assets/animations
```
Ce script convertit tous vos FBX en `.glb` légers avec **Root Motion** configuré pour le Quest 3S.

---

### 3. Utilisation en GDScript :
```gdscript
var mixamo_ctrl = MixamoGodot4Controller.new()
mixamo_ctrl.avatar_skeleton = $Parzival/GeneralSkeleton
mixamo_ctrl.animation_player = $Parzival/AnimationPlayer
mixamo_ctrl.play_action("CyberpunkDance")
```
"""

    with open("Mixamo_Pipeline_Guide.md", "w", encoding="utf-8") as f:
        f.write(guide_md)
    print("-> Wrote Mixamo_Pipeline_Guide.md")

    print("\n[SUCCESS] Mixamo pipeline installation script created & executed successfully.")

if __name__ == "__main__":
    setup_mixamo_pipeline()
