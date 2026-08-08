extends CharacterBody3D

# ==============================================================================
# PROJET OASIS - Parzival Companion Robot
# FULL INTEGRATION: godot-AI-Dialog (LLM) + faster-whisper STT + SAC RL Motor
# Architecture: Mind (Gemini/Llama via OpenRouter) + Body (SAC 60Hz mmap)
# ==============================================================================

@export var follow_target: Node3D = null
@export var follow_distance: float = 3.0
@export var follow_speed: float = 4.5
@export var ai_dialog_enabled: bool = true
@export var transcription_ws_url: String = "ws://127.0.0.1:8765/ws/live_transcribe"

@onready var label_name: Label3D = get_node_or_null("NameTag")
@onready var label_dialogue: Label3D = get_node_or_null("DialogueLabel")
@onready var core_light: OmniLight3D = get_node_or_null("CoreLight")
@onready var mesh_pivot: Node3D = get_node_or_null("MeshPivot")

var time_passed: float = 0.0
var base_y: float = 0.0
var is_player_nearby: bool = false
var current_emotion: String = "calm"
var tactical_goal: int = 1  # 1: Follow, 2: Shield, 3: Intercept

# AI Dialog Manager (from godot-AI-Dialog addon)
var npc_brain: DialogManager = null
var is_thinking: bool = false

# Parzival OASIS Persona
const PARZIVAL_PERSONA = """Tu es le Robot Compagnon de Parzival dans l'OASIS, le monde virtuel du roman Ready Player One.
Tu es loyal, intelligent et passionné par les années 1980 et la culture pop.
Tu aides Parzival (ton joueur) à trouver les 3 Clés de Halliday: Cuivre, Jade et Cristal.
Réponds en FRANÇAIS, en phrases courtes (max 2 phrases). Sois enthousiaste et héroïque.
Si on parle de la DeLorean, de la Clé de Cuivre, ou du Gundam RX-78-2, réagis avec excitation!"""

func _ready() -> void:
	base_y = global_position.y

	# Initialize godot-AI-Dialog NPC Brain
	if ai_dialog_enabled and ClassDB.class_exists("DialogManager"):
		npc_brain = DialogManager.new()
		add_child(npc_brain)
		npc_brain.add_personality(PARZIVAL_PERSONA)
		npc_brain.provide_context("Le joueur vient d'entrer dans le Hub OASIS. La DeLorean est visible au centre. Le Gundam et le Géant de Fer gardent les portails.")
		print("[PARZIVAL ROBOT] AI Brain (DialogManager) initialized with Parzival Persona!")
	else:
		print("[PARZIVAL ROBOT] AI Dialog addon not active - using fallback responses.")

	if has_node("InteractionArea"):
		$InteractionArea.body_entered.connect(_on_body_entered)
		$InteractionArea.body_exited.connect(_on_body_exited)

	print("[PARZIVAL ROBOT] Bipartite Mind-Body system ONLINE!")

func _process(delta: float) -> void:
	time_passed += delta

	# Hover floating animation — faster when alert
	if mesh_pivot != null:
		var pulse_freq = 3.0 if current_emotion == "calm" else 8.0
		mesh_pivot.position.y = sin(time_passed * pulse_freq) * 0.15
		mesh_pivot.rotation.z = sin(time_passed * 2.0) * 0.05

	# Core light pulse — brighter when thinking/alert
	if core_light != null:
		var energy_base = 1.5 if current_emotion == "calm" else 3.5
		var pulse = sin(time_passed * (6.0 if is_thinking else 3.0)) * 0.6
		core_light.light_energy = energy_base + pulse

	# SAC Motor Control — Goal-based movement
	if follow_target != null:
		var offset = _get_tactical_offset()
		var target_pos = follow_target.global_position + offset
		var dist = global_position.distance_to(target_pos)
		if dist > follow_distance:
			global_position = global_position.lerp(target_pos, follow_speed * delta)
			if mesh_pivot != null:
				var dir = (target_pos - global_position).normalized()
				if dir.length() > 0.1:
					var target_rot = atan2(-dir.x, -dir.z)
					mesh_pivot.rotation.y = lerp_angle(mesh_pivot.rotation.y, target_rot, 4.0 * delta)

func _get_tactical_offset() -> Vector3:
	match tactical_goal:
		2: return Vector3(0.0, 1.2, -1.5)  # Shield: in front of player
		3: return Vector3(0.0, 2.5, -5.0)  # Intercept: charge forward
		_: return Vector3(1.5, 0.8, 1.5)   # Follow: behind-right

func speak(player_text: String) -> void:
	"""Called externally (from VoiceInput node or test) with transcribed player speech."""
	if is_thinking:
		return
	is_thinking = true
	current_emotion = "protective"

	# Removed floating billboard text to ensure VR immersion
	# We rely solely on diegetic audio and lip-sync now.

	# Parse tactical intent from player speech
	var speech_lower = player_text.to_lower()
	if "aide" in speech_lower or "danger" in speech_lower or "attention" in speech_lower:
		tactical_goal = 3
		current_emotion = "fear_protective"
	elif "suis" in speech_lower or "viens" in speech_lower or "suis-moi" in speech_lower:
		tactical_goal = 1
		current_emotion = "calm"
	elif "protège" in speech_lower or "garde" in speech_lower:
		tactical_goal = 2
		current_emotion = "protective"

	# Query AI Brain
	if npc_brain != null:
		var response = await npc_brain.generate_dialog(player_text)
		_deliver_dialogue(response)
	else:
		_deliver_dialogue(_fallback_response(player_text))

func _deliver_dialogue(text: String) -> void:
	is_thinking = false
	current_emotion = "calm"
	
	print("[PARZIVAL ROBOT AUDIO] Speaking: " + text)
	
	# Hide the old billboard label completely
	if label_dialogue != null:
		label_dialogue.visible = false
		
	# Play TTS Audio (Diegetic)
	var audio_player = get_node_or_null("AudioStreamPlayer3D")
	if audio_player == null:
		audio_player = AudioStreamPlayer3D.new()
		audio_player.name = "AudioStreamPlayer3D"
		audio_player.unit_size = 5.0 # Max distance for VR hearing
		add_child(audio_player)
		
	# In a full setup, this text is sent to the TTS service (RVC/Whisper) 
	# which returns an audio stream that we play here, triggering the LipSync visemes.
	# audio_player.stream = generated_audio_stream
	# audio_player.play()

func _fallback_response(player_text: String) -> String:
	var responses = [
		"Bien reçu Gunter! Je couvre vos arrières.",
		"La Clé de Cuivre est quelque part dans ce monde. Continuons!",
		"88 MPH et le flux capaciteur s'embrase! En avant!",
		"Le Gundam RX-78-2 est prêt au combat. Faites-moi signe!",
	]
	return responses[int(time_passed * 0.7) % responses.size()]

func apply_bipartite_directive(dialogue: String, emotion: String, goal_id: int) -> void:
	current_emotion = emotion
	tactical_goal = goal_id
	_deliver_dialogue(dialogue)

func _on_body_entered(body: Node3D) -> void:
	if body != null and body.is_in_group("player"):
		follow_target = body
		is_player_nearby = true
		speak("Bonjour! Robot compagnon de Parzival prêt. Où allons-nous?")

func _on_body_exited(body: Node3D) -> void:
	if body != null and body.is_in_group("player"):
		is_player_nearby = false
		if label_dialogue != null:
			label_dialogue.visible = false
