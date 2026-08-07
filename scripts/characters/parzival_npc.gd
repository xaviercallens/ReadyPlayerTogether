extends CharacterBody3D

# ==============================================================================
# PROJET OASIS - Parzival (Ready Player One Gunter NPC)
# ==============================================================================

@onready var key_mesh: Node3D = get_node_or_null("KeyMesh")
@onready var dialogue_label: Label3D = get_node_or_null("DialogueLabel")
@onready var body_mesh: Node3D = get_node_or_null("BodyMesh")

var anim_controller: RPMAnimator
var mixamo_controller: MixamoGodot4Controller
var time_passed: float = 0.0
var is_player_near: bool = false

func _ready() -> void:
	if has_node("InteractionArea"):
		$InteractionArea.body_entered.connect(_on_body_entered)
		$InteractionArea.body_exited.connect(_on_body_exited)
	if dialogue_label != null:
		dialogue_label.text = "PARZIVAL: 'Trouve la Clé de Cuivre!'"
	
	if body_mesh != null:
		anim_controller = RPMAnimator.new()
		anim_controller.target_avatar_node = body_mesh
		add_child(anim_controller)
		
		# Intégration de la pipeline Mixamo ➔ Godot 4
		mixamo_controller = MixamoGodot4Controller.new()
		add_child(mixamo_controller)

func _process(delta: float) -> void:
	time_passed += delta
	if key_mesh != null:
		key_mesh.rotation.y += delta * 2.0
		key_mesh.position.y = 2.4 + sin(time_passed * 3.0) * 0.1

func _on_body_entered(body: Node3D) -> void:
	if body != null and body.is_in_group("player"):
		is_player_near = true
		if dialogue_label != null:
			dialogue_label.text = "PARZIVAL: 'Bienvenue Gunter! Traverse le portail 03 pour la course!'"
		if anim_controller != null:
			anim_controller.set_state(RPMAnimator.AnimState.WAVE)
		if mixamo_controller != null:
			mixamo_controller.play_action("WaveGreeting")

func _on_body_exited(body: Node3D) -> void:
	if body != null and body.is_in_group("player"):
		is_player_near = false
		if dialogue_label != null:
			dialogue_label.text = "PARZIVAL: 'Trouve la Clé de Cuivre!'"
		if anim_controller != null:
			anim_controller.set_state(RPMAnimator.AnimState.IDLE)
		if mixamo_controller != null:
			mixamo_controller.play_action("Idle")