# Godot 4.3+ AI Dialogue Manager
# Routes dialogue through the AMCP Agent Mesh bridge (Ollama or Gemini)
# instead of directly calling OpenAI, keeping the architecture unified.
class_name AIDialogueManager
extends Node

signal dialogue_started(npc_name: String)
signal response_received(npc_name: String, text_response: String)
signal riddle_solved(key_name: String)
signal dialogue_error(error_msg: String)

## The AMCP bridge node to route through. Assign in Inspector or it will be auto-detected.
@export var mesh_bridge: AgentMeshBridge

@export_multiline var system_persona: String = "Tu es le gardien de la Cle de Cuivre de l'OASIS. Tu donnes des reponses courtes, mysterieuses et amicales. Si le joueur resout ton enigme, reponds avec le mot 'SUCCES'."

@export var npc_name: String = "Gardien"

var conversation_history: Array = []

func _ready() -> void:
	# Auto-detect AgentMeshBridge if not assigned
	if mesh_bridge == null:
		mesh_bridge = _find_mesh_bridge()

	if mesh_bridge != null:
		mesh_bridge.npc_replied.connect(_on_mesh_reply)
		mesh_bridge.mesh_error.connect(_on_mesh_error)
		print("[AIDialogueManager] Connected via AMCP bridge.")
	else:
		print("[AIDialogueManager] WARNING: No AgentMeshBridge found. Dialogue will use offline fallback only.")

	conversation_history.append({"role": "system", "content": system_persona})

func _find_mesh_bridge() -> AgentMeshBridge:
	"""Walk up the tree looking for an AgentMeshBridge node."""
	var root := get_tree().current_scene
	if root == null:
		return null
	var bridges := root.find_children("*", "AgentMeshBridge", true, false)
	if bridges.size() > 0:
		return bridges[0] as AgentMeshBridge
	return null

func send_player_speech(player_text: String) -> void:
	if player_text.strip_edges().is_empty():
		return

	print("[AIDialogueManager] Player said: ", player_text)
	conversation_history.append({"role": "user", "content": player_text})
	dialogue_started.emit(npc_name)

	if mesh_bridge != null:
		# Route through AMCP — the server handles Ollama/Gemini routing
		mesh_bridge.send_player_speech_to_mesh(npc_name, system_persona, player_text)
	else:
		# Offline fallback for VR demo without server
		_handle_offline_response()

func _on_mesh_reply(replied_npc: String, text: String, audio_path: String) -> void:
	conversation_history.append({"role": "assistant", "content": text})
	response_received.emit(replied_npc, text)

	# Check for riddle solved keywords
	if "SUCCES" in text.to_upper() or "COPPER" in text.to_upper():
		riddle_solved.emit("Cle de Cuivre")

func _on_mesh_error(error_msg: String) -> void:
	print("[AIDialogueManager] Mesh error: ", error_msg)
	dialogue_error.emit(error_msg)
	# Fall back to offline response
	_handle_offline_response()

func _handle_offline_response() -> void:
	var mock_response := "Bienvenue dans l'OASIS ! En mode demonstration hors-ligne, le gardien vous accorde son passage. SUCCES !"
	conversation_history.append({"role": "assistant", "content": mock_response})
	response_received.emit(npc_name + " (Demo)", mock_response)
	riddle_solved.emit("Cle de Cuivre")
