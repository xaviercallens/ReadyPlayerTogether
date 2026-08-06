extends Node3D

# ==============================================================================
# PROJET OASIS - Phase 0 Ready Player Me Avatar Loader (Universal GLTF Bridge)
# Compatible with Godot 4, Unity, and Unreal Engine RPM pipelines
# ==============================================================================

@export var avatar_url: str = "https://models.readyplayer.me/64bfa15f0e72c63d7e93a001.glb"
@export var local_avatar_path: str = "res://assets/avatars/default_avatar.glb"

func _ready() -> void:
	print("[RPM LOADER] Initializing Ready Player Me Phase 0 Loader...")
	load_local_gltf_avatar()

func load_local_gltf_avatar() -> void:
	if FileAccess.file_exists(local_avatar_path):
		var gltf_doc = GLTFDocument.new()
		var gltf_state = GLTFState.new()
		var error = gltf_doc.append_from_file(local_avatar_path, gltf_state)
		if error == OK:
			var avatar_node = gltf_doc.generate_scene(gltf_state)
			add_child(avatar_node)
			print("[RPM LOADER] Avatar GLTF successfully loaded into scene!")
		else:
			print("[RPM LOADER] Error loading avatar GLTF file: ", error)
	else:
		print("[RPM LOADER] Local avatar not found at " + local_avatar_path + ". Ready for RPM API download.")
