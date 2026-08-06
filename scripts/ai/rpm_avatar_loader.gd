extends Node

# ==============================================================================
# PROJET OASIS - Ready Player Me (RPM) Runtime Avatar Loader
# (Inspired by Malcolm Nixon's GodotReadyPlayerMeAvatar plugin)
# Downloads and instantiates RPM avatars (.glb) at runtime with skeleton & blendshapes.
# ==============================================================================

signal avatar_loaded(avatar_node: Node3D)

var runtime_loader = preload("res://scripts/ai/runtime_asset_loader.gd").new()
var http_request: HTTPRequest

func _ready() -> void:
	http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(_on_avatar_download_completed)

func load_avatar_from_id(avatar_id: String) -> void:
	var avatar_url = "https://models.readyplayer.me/" + avatar_id + ".glb"
	print("[RPM LOADER] Downloading Ready Player Me avatar from: ", avatar_url)
	http_request.request(avatar_url)

func _on_avatar_download_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code == 200:
		var save_path = "user://rpm_avatar_temp.glb"
		var file = FileAccess.open(save_path, FileAccess.WRITE)
		file.store_buffer(body)
		file.close()
		
		var node = runtime_loader.load_glb_asset(save_path)
		if node:
			print("[RPM LOADER] RPM Avatar successfully loaded into Godot 4!")
			avatar_loaded.emit(node)
	else:
		print("[RPM LOADER] Failed to download RPM avatar. Response code: ", response_code)