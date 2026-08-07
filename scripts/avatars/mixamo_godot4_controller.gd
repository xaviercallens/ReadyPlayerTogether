# Godot 4.3+ Mixamo & Ready Player Me Humanoid Retargeter & AnimationTree Controller
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
