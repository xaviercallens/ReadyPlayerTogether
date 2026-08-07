# Matrix-Game Arcade Portal WebSocket Client (The Dreamer)
# Streams playable video onto a 3D Mesh (Arcade Screen or Portal) in VR.
# Input is throttled to match the server's 25 FPS to avoid flooding.
class_name ArcadePortalClient
extends MeshInstance3D

@export var websocket_url: String = "ws://127.0.0.1:8006/ws/dream_portal"

var socket := WebSocketPeer.new()
var image := Image.new()
var image_texture := ImageTexture.new()

# Input throttling: only send at 25 FPS, and only when changed
var _last_input: String = ""
var _send_interval: float = 1.0 / 25.0  # 25 FPS
var _time_since_send: float = 0.0

func _ready() -> void:
	# Apply dynamic texture as material on the mesh (e.g., arcade screen)
	var mat := StandardMaterial3D.new()
	mat.albedo_texture = image_texture
	mat.emission_enabled = true
	mat.emission_texture = image_texture
	mat.cull_mode = BaseMaterial3D.CULL_DISABLED
	set_surface_override_material(0, mat)

	var err := socket.connect_to_url(websocket_url)
	if err == OK:
		print("[ArcadePortal] Connected to Matrix-Game on ", websocket_url)
	else:
		print("[ArcadePortal] WebSocket connection failed.")

func _process(delta: float) -> void:
	socket.poll()
	var state := socket.get_ready_state()

	if state == WebSocketPeer.STATE_OPEN:
		# Read incoming video frames
		while socket.get_available_packet_count() > 0:
			var packet := socket.get_packet()
			_update_portal_texture(packet)

		# Throttled input sending (25 FPS max, only on change)
		_time_since_send += delta
		if _time_since_send >= _send_interval:
			_time_since_send = 0.0
			_send_player_inputs()

	elif state == WebSocketPeer.STATE_CLOSED:
		pass # Could implement reconnect logic here

func _update_portal_texture(jpeg_bytes: PackedByteArray) -> void:
	var err := image.load_jpg_from_buffer(jpeg_bytes)
	if err == OK:
		if image_texture.get_size() == Vector2.ZERO:
			image_texture.set_image(image)
		else:
			image_texture.update(image)

func _send_player_inputs() -> void:
	var input_str := ""
	if Input.is_action_pressed("move_forward"): input_str += "W"
	if Input.is_action_pressed("move_backward"): input_str += "S"
	if Input.is_action_pressed("move_left"): input_str += "A"
	if Input.is_action_pressed("move_right"): input_str += "D"

	# Only send if input changed (avoid redundant packets)
	if input_str != _last_input:
		_last_input = input_str
		if input_str != "":
			socket.put_packet(input_str.to_utf8_buffer())
