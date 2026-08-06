extends Node

# ==============================================================================
# PROJET OASIS - Master Data Bridge GDScript Client
# Connects Godot 4 VR & PC UI to the FastAPI Data Bridge Server (http://127.0.0.1:8000)
# Handles 3D Meshes (.glb), PBR Textures (.png), and Skyboxes (.hdr)
# ==============================================================================

signal mesh_ready(res_path: String)
signal pbr_ready(albedo_path: String, normal_path: String, roughness_path: String)
signal skybox_ready(hdr_path: String)

@export var bridge_server_url: String = "http://127.0.0.1:8000"
var http_node: HTTPRequest
var runtime_loader = preload("res://scripts/ai/runtime_asset_loader.gd").new()

func _ready() -> void:
	http_node = HTTPRequest.new()
	add_child(http_node)
	http_node.request_completed.connect(_on_bridge_request_completed)

func request_mesh_generation(prompt: String) -> void:
	print("[DATA BRIDGE] Requesting 3D Mesh: ", prompt)
	var url = bridge_server_url + "/api/bridge/mesh"
	var headers = ["Content-Type: application/json"]
	var body = JSON.stringify({"prompt": prompt, "category": "prop"})
	http_node.request(url, headers, HTTPClient.METHOD_POST, body)

func request_pbr_maps(asset_name: String) -> void:
	print("[DATA BRIDGE] Requesting PBR Maps for: ", asset_name)
	var url = bridge_server_url + "/api/bridge/pbr"
	var headers = ["Content-Type: application/json"]
	var body = JSON.stringify({"asset_name": asset_name})
	http_node.request(url, headers, HTTPClient.METHOD_POST, body)

func request_skybox_generation(prompt: String) -> void:
	print("[DATA BRIDGE] Requesting 360° Skybox HDR: ", prompt)
	var url = bridge_server_url + "/api/bridge/skybox"
	var headers = ["Content-Type: application/json"]
	var body = JSON.stringify({"prompt": prompt})
	http_node.request(url, headers, HTTPClient.METHOD_POST, body)

func _on_bridge_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code == 200:
		var json = JSON.parse_string(body.get_string_from_utf8())
		if json and json.has("asset_type"):
			var asset_type = json["asset_type"]
			if asset_type == "mesh":
				var res_path = json.get("res_path", "")
				print("[DATA BRIDGE] 3D Mesh Ready -> ", res_path)
				mesh_ready.emit(res_path)
			elif asset_type == "pbr_textures":
				pbr_ready.emit(json.get("albedo_path", ""), json.get("normal_path", ""), json.get("roughness_path", ""))
			elif asset_type == "hdr_skybox":
				skybox_ready.emit(json.get("hdr_path", ""))
	else:
		print("[DATA BRIDGE] Server returned response code: ", response_code)