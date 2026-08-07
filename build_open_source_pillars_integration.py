import os
import sys

def build_open_source_pillars():
    print("=== Building Open-Source Pillars Integration for Projet OASIS ===")
    
    # 1. AI Dialogue Manager (Godot 4.3+ GDScript)
    ai_dialog_gd = """# Godot 4.3+ AI Dialogue Manager (Inspired by krishsharma0413/godot-AI-Dialog)
# Handles asynchronous LLM dialogue (OpenAI/OpenRouter/Gemini) for VR NPCs.
class_name AIDialogueManager
extends Node

signal dialogue_started(npc_name: String)
signal response_received(npc_name: String, text_response: String)
signal riddle_solved(key_name: String)
signal dialogue_error(error_msg: String)

@export var api_url: String = "https://api.openai.com/v1/chat/completions"
@export var api_key: String = ""
@export var default_model: String = "gpt-4o-mini"

@export_multiline var system_persona: String = "Tu es le gardien de la Clé de Cuivre de l'OASIS. Tu donnes des réponses courtes, mystérieuses et amicales. Si le joueur résout ton énigme, réponds avec le mot 'SUCCÈS'."

var conversation_history: Array = []
var http_request: HTTPRequest

func _ready() -> void:
	http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(_on_request_completed)
	
	# Initialiser le persona système
	conversation_history.append({"role": "system", "content": system_persona})
	print("[AIDialogueManager] Initialisé avec persona: ", system_persona)

func send_player_speech(player_text: String) -> void:
	if player_text.strip_edges().is_empty():
		return
		
	print("[AIDialogueManager] Joueur a dit: ", player_text)
	conversation_history.append({"role": "user", "content": player_text})
	dialogue_started.emit("Gardien")
	
	var headers = [
		"Content-Type: application/json",
		"Authorization: Bearer " + api_key
	]
	
	var payload = {
		"model": default_model,
		"messages": conversation_history,
		"max_tokens": 150,
		"temperature": 0.7
	}
	
	var json_payload = JSON.stringify(payload)
	var err = http_request.request(api_url, headers, HTTPClient.METHOD_POST, json_payload)
	if err != OK:
		dialogue_error.emit("Impossible de démarrer la requête HTTP: " + str(err))

func _on_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code != 200:
		var err_text = body.get_string_from_utf8()
		print("[AIDialogueManager] Erreur API (Code ", response_code, "): ", err_text)
		# Réponse de repli locale pour démo VR hors-ligne
		_handle_offline_response()
		return
		
	var json = JSON.new()
	var parse_err = json.parse(body.get_string_from_utf8())
	if parse_err != OK:
		dialogue_error.emit("Erreur de formatage JSON de l'IA")
		return
		
	var data = json.get_data()
	if data.has("choices") and data["choices"].size() > 0:
		var reply_text = data["choices"][0]["message"]["content"]
		conversation_history.append({"role": "assistant", "content": reply_text})
		response_received.emit("Gardien", reply_text)
		
		# Vérifier si l'énigme est résolue
		if "SUCCÈS" in reply_text.upper() or "COPPER" in reply_text.upper():
			riddle_solved.emit("Clé de Cuivre")

func _handle_offline_response() -> void:
	var mock_response = "Bienvenue dans l'OASIS ! En mode démonstration hors-ligne, le gardien vous accorde son passage. SUCCÈS !"
	conversation_history.append({"role": "assistant", "content": mock_response})
	response_received.emit("Gardien (Mode Démo)", mock_response)
	riddle_solved.emit("Clé de Cuivre")
"""
    
    os.makedirs("scripts/ai", exist_ok=True)
    with open("scripts/ai/godot_ai_dialog_manager.gd", "w", encoding="utf-8") as f:
        f.write(ai_dialog_gd)
    print("-> Wrote scripts/ai/godot_ai_dialog_manager.gd")

    # 2. WorkerThreadPool Procedural Generation (Godot 4.3+ GDScript)
    proc_worker_gd = """# Godot 4.3+ Procedural Generation with WorkerThreadPool (Inspired by gdquest-demos)
# Offloads procedural mesh and terrain creation to background threads to prevent VR frame stuttering.
class_name ProceduralWorldWorker
extends Node3D

signal chunk_generated(chunk_position: Vector3, mesh_instance: MeshInstance3D)
signal generation_completed(total_chunks: int)

@export var render_distance: int = 3
@export var chunk_size: float = 20.0
@export var grid_height_scale: float = 5.0

var noise: FastNoiseLite
var generated_chunks: Dictionary = {}
var pending_tasks: Array = []

func _ready() -> void:
	noise = FastNoiseLite.new()
	noise.seed = 1337
	noise.noise_type = FastNoiseLite.TYPE_PERLIN
	noise.frequency = 0.05
	
	print("[ProceduralWorldWorker] Démarrage de la génération arrière-plan VR...")
	generate_world_async()

func generate_world_async() -> void:
	var total = 0
	for x in range(-render_distance, render_distance + 1):
		for z in range(-render_distance, render_distance + 1):
			var chunk_pos = Vector3(x * chunk_size, 0, z * chunk_size)
			total += 1
			# Utiliser WorkerThreadPool de Godot 4 pour ne pas geler l'affichage VR
			var task_id = WorkerThreadPool.add_task(Callable(self, "_build_chunk_thread").bind(chunk_pos))
			pending_tasks.append(task_id)
			
	print("[ProceduralWorldWorker] ", total, " tâches soumises au WorkerThreadPool.")

func _build_chunk_thread(chunk_pos: Vector3) -> void:
	var plane_mesh = PlaneMesh.new()
	plane_mesh.size = Vector2(chunk_size, chunk_size)
	plane_mesh.subdivide_width = 10
	plane_mesh.subdivide_depth = 10
	
	var mesh_inst = MeshInstance3D.new()
	mesh_inst.mesh = plane_mesh
	mesh_inst.position = chunk_pos
	
	# Matériau Synthwave Neon Cyberpunk
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color(0.05, 0.0, 0.15)
	mat.emission_enabled = true
	mat.emission = Color(0.0, 0.8, 1.0)
	mat.emission_energy_multiplier = 0.5
	mesh_inst.material_override = mat
	
	# Publier sur le thread principal
	call_deferred("_on_chunk_completed", chunk_pos, mesh_inst)

func _on_chunk_completed(chunk_pos: Vector3, mesh_inst: MeshInstance3D) -> void:
	add_child(mesh_inst)
	generated_chunks[chunk_pos] = mesh_inst
	chunk_generated.emit(chunk_pos, mesh_inst)
	
	if generated_chunks.size() >= pending_tasks.size():
		generation_completed.emit(generated_chunks.size())
		print("[ProceduralWorldWorker] Génération du monde infini terminée avec succès!")
"""

    os.makedirs("scripts/hub", exist_ok=True)
    with open("scripts/hub/procedural_world_worker.gd", "w", encoding="utf-8") as f:
        f.write(proc_worker_gd)
    print("\n[SUCCESS] Open-source pillars integration script created & executed successfully.")

if __name__ == "__main__":
    build_open_source_pillars()
