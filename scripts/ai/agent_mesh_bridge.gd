# Godot 4.3+ Agent Mesh Connector (AMCP Protocol Bridge)
# Asynchronously connects Godot 4 to local Ollama, ComfyUI, RVC, and Godot RL agents.
class_name AgentMeshBridge
extends Node

signal npc_replied(npc_name: String, text: String, audio_path: String)
signal pbr_material_ready(material_name: String, albedo: String, normal: String, roughness: String)
signal mesh_error(error_msg: String)

@export var mesh_server_url: String = "http://127.0.0.1:8005"

var http_request: HTTPRequest

func _ready() -> void:
	http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(_on_request_completed)
	print("[AgentMeshBridge] Agent Mesh Communication Protocol connecté a ", mesh_server_url)

func send_player_speech_to_mesh(npc_name: String, persona: String, speech_text: String) -> void:
	var payload = {
		"npc_name": npc_name,
		"persona": persona,
		"player_text": speech_text
	}
	var headers = ["Content-Type: application/json"]
	var json_payload = JSON.stringify(payload)
	
	var err = http_request.request(mesh_server_url + "/api/mesh/speak", headers, HTTPClient.METHOD_POST, json_payload)
	if err != OK:
		mesh_error.emit("Erreur de connexion au maillage d'agents: " + str(err))

func request_pbr_material_from_mesh(material_prompt: String) -> void:
	var payload = {"material_prompt": material_prompt}
	var headers = ["Content-Type: application/json"]
	var json_payload = JSON.stringify(payload)
	
	http_request.request(mesh_server_url + "/api/mesh/generate_pbr", headers, HTTPClient.METHOD_POST, json_payload)

func _on_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code != 200:
		print("[AgentMeshBridge] Reponse locale fallback (Serveur AI hors-ligne code ", response_code, ")")
		npc_replied.emit("Parzival", "L'OASIS fonctionne en mode secours VR local!", "")
		return
		
	var json = JSON.new()
	if json.parse(body.get_string_from_utf8()) == OK:
		var data = json.get_data()
		if data.has("reply_text"):
			npc_replied.emit(data.get("npc_name", "NPC"), data["reply_text"], data.get("audio_stream_path", ""))
		elif data.has("material_name"):
			pbr_material_ready.emit(data["material_name"], data["albedo_map"], data["normal_map"], data["roughness_map"])
