# Godot 4.3+ AI Dialogue Manager (Inspired by krishsharma0413/godot-AI-Dialog)
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
