# Godot 4.3+ Agent Mesh Connector (AMCP Protocol Bridge)
# Connects Godot 4 to the unified OASIS server with request pooling and session memory.
class_name AgentMeshBridge
extends Node

signal npc_replied(npc_name: String, text: String, audio_path: String)
signal pbr_material_ready(material_name: String, albedo: String, normal: String, roughness: String)
signal mesh_error(error_msg: String)

@export var mesh_server_url: String = "http://127.0.0.1:8005"

# HTTPRequest pool to allow concurrent requests
var _request_pool: Array[HTTPRequest] = []
var _pool_size: int = 4
var _session_id: String = ""

func _ready() -> void:
	# Generate a unique session ID for conversation memory
	_session_id = str(randi()) + "_" + str(Time.get_ticks_msec())

	# Create a pool of HTTPRequest nodes
	for i in range(_pool_size):
		var req := HTTPRequest.new()
		req.name = "HTTPReq_" + str(i)
		add_child(req)
		req.request_completed.connect(_on_request_completed)
		_request_pool.append(req)

	print("[AgentMeshBridge] AMCP connected to ", mesh_server_url, " (session: ", _session_id, ")")

func _get_available_request() -> HTTPRequest:
	"""Get an idle HTTPRequest from the pool, or null if all busy."""
	for req in _request_pool:
		if req.get_http_client_status() == HTTPClient.STATUS_DISCONNECTED or \
		   req.get_http_client_status() == HTTPClient.STATUS_CONNECTED:
			return req
	return null

func send_player_speech_to_mesh(npc_name: String, persona: String, speech_text: String) -> void:
	var req := _get_available_request()
	if req == null:
		mesh_error.emit("All HTTP request slots busy. Try again.")
		return

	var payload := {
		"npc_name": npc_name,
		"persona": persona,
		"player_text": speech_text,
		"session_id": _session_id,
	}
	var headers := ["Content-Type: application/json"]
	var json_payload := JSON.stringify(payload)

	var err := req.request(mesh_server_url + "/api/mesh/speak", headers, HTTPClient.METHOD_POST, json_payload)
	if err != OK:
		mesh_error.emit("Connection error to agent mesh: " + str(err))

func request_pbr_material_from_mesh(material_prompt: String) -> void:
	var req := _get_available_request()
	if req == null:
		mesh_error.emit("All HTTP request slots busy. Try again.")
		return

	var payload := {"material_prompt": material_prompt}
	var headers := ["Content-Type: application/json"]
	var json_payload := JSON.stringify(payload)

	req.request(mesh_server_url + "/api/mesh/generate_pbr", headers, HTTPClient.METHOD_POST, json_payload)

func _on_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code != 200:
		print("[AgentMeshBridge] Server response code ", response_code, " — using VR fallback.")
		npc_replied.emit("Parzival", "L'OASIS fonctionne en mode secours VR local!", "")
		return

	var json := JSON.new()
	if json.parse(body.get_string_from_utf8()) == OK:
		var data: Dictionary = json.get_data()
		if data.has("reply_text"):
			npc_replied.emit(data.get("npc_name", "NPC"), data["reply_text"], data.get("audio_stream_path", ""))
		elif data.has("material_name"):
			pbr_material_ready.emit(data["material_name"], data["albedo_map"], data["normal_map"], data["roughness_map"])
