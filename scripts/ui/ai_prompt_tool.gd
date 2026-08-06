extends CanvasLayer

# ==============================================================================
# PROJET OASIS - Interactive In-Game AI Prompt Tool
# Allows the 10-year-old son to type any asset prompt (e.g. 'cyberpunk hoverboard')
# Sends HTTP POST to FastAPI ML Foundry (http://127.0.0.1:8000/api/generate_asset)
# Dynamically loads and spawns the resulting .glb model right in front of the player!
# ==============================================================================

@onready var panel: Control = $Control
@onready var prompt_input: LineEdit = $Control/Panel/VBoxContainer/LineEdit
@onready var status_label: Label = $Control/Panel/VBoxContainer/StatusLabel
@onready var http_request: HTTPRequest = $HTTPRequest

var runtime_loader = preload("res://scripts/ai/runtime_asset_loader.gd").new()

func _ready() -> void:
	panel.visible = false
	http_request.request_completed.connect(_on_request_completed)

func toggle_tool() -> void:
	panel.visible = not panel.visible
	if panel.visible:
		Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
		prompt_input.text = ""
		prompt_input.grab_focus()
	else:
		Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if (event.ctrl_pressed and event.keycode == KEY_A) or (event.shift_pressed and event.keycode == KEY_A):
			toggle_tool()

func _on_submit_pressed() -> void:
	var text_prompt = prompt_input.text.strip_edges()
	if text_prompt.is_empty():
		status_label.text = "Please enter a valid asset prompt!"
		return
		
	status_label.text = "Sending prompt to ML Foundry Backend (RTX 2070)..."
	print("[AI PROMPT TOOL] Requesting generation for: ", text_prompt)
	
	var url = "http://127.0.0.1:8000/api/generate_asset"
	var headers = ["Content-Type: application/json"]
	var body = JSON.stringify({"prompt": text_prompt, "category": "prop"})
	
	var err = http_request.request(url, headers, HTTPClient.METHOD_POST, body)
	if err != OK:
		status_label.text = "HTTP Request Error: " + str(err)

func _on_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code == 200:
		var json = JSON.parse_string(body.get_string_from_utf8())
		if json and json.has("asset_res_path"):
			var res_path = json["asset_res_path"]
			status_label.text = "Asset Ready! Spawning: " + res_path
			print("[AI PROMPT TOOL] Spawning GLTF asset: ", res_path)
			_spawn_asset_in_front_of_player(res_path)
			panel.visible = false
			Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
	else:
		status_label.text = "Server error code: " + str(response_code)

func _spawn_asset_in_front_of_player(res_path: String) -> void:
	var spawned_node = runtime_loader.load_glb_asset(res_path)
	if spawned_node:
		var player = get_tree().get_nodes_in_group("player")[0] if get_tree().get_nodes_in_group("player").size() > 0 else null
		var parent_scene = get_tree().current_scene
		parent_scene.add_child(spawned_node)
		if player:
			spawned_node.global_position = player.global_position - player.global_transform.basis.z * 3.0 + Vector3(0, 0.5, 0)
		else:
			spawned_node.global_position = Vector3(0, 1, -3)