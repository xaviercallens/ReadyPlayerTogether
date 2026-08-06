extends Node3D
class_name RPMAvatarLoader

# ==============================================================================
# PROJET OASIS - Ready Player Me Universal Avatar Loader
# Downloads GLB/GLTF avatars at runtime and attaches them to the player rig.
# ==============================================================================

signal avatar_loaded(avatar_node: Node3D)
signal avatar_failed(error_message: String)

@export var avatar_url: String = "https://models.readyplayer.me/64bfa15f0e72c63d7e3934a6.glb"
@export var auto_load_on_start: bool = true

var http_request: HTTPRequest

func _ready() -> void:
	http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(_on_avatar_download_completed)
	
	if auto_load_on_start and not avatar_url.is_empty():
		load_avatar_from_url(avatar_url)

func load_avatar_from_url(url: String) -> void:
	print("[RPM Loader] Fetching avatar model from: ", url)
	var err = http_request.request(url)
	if err != OK:
		print("[RPM Loader] Error initiating HTTP request: ", err)
		avatar_failed.emit("HTTP Request Failed")

func _on_avatar_download_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if result != HTTPRequest.RESULT_SUCCESS or response_code != 200:
		print("[RPM Loader] Failed to download RPM avatar. HTTP Code: ", response_code)
		avatar_failed.emit("Download Failed")
		return
		
	print("[RPM Loader] Avatar GLB downloaded (%d bytes). Parsing GLTF..." % body.size())
	
	var gltf_doc = GLTFDocument.new()
	var gltf_state = GLTFState.new()
	
	var err = gltf_doc.append_from_buffer(body, "", gltf_state)
	if err == OK:
		var avatar_scene = gltf_doc.generate_scene(gltf_state)
		if avatar_scene:
			# Remove previous avatar instances
			for child in get_children():
				if child != http_request:
					child.queue_free()
			
			add_child(avatar_scene)
			avatar_scene.name = "RPMAvatarModel"
			avatar_scene.transform.basis = Basis.from_scale(Vector3(1, 1, 1))
			print("[RPM Loader] Ready Player Me Avatar successfully attached to player!")
			avatar_loaded.emit(avatar_scene)
	else:
		print("[RPM Loader] Error parsing GLTF buffer: ", err)
		avatar_failed.emit("GLTF Parsing Error")