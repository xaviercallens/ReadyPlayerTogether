extends CharacterBody3D

# ==============================================================================
# PROJET OASIS - Parzival (Ready Player One Gunter NPC)
# Interacts with the player, floating key animation, Gemini AI dialogue trigger.
# ==============================================================================

@onready var key_mesh: MeshInstance3D = $KeyMesh
@onready var dialogue_label: Label3D = $DialogueLabel
@onready var body_mesh: MeshInstance3D = $BodyMesh

var anim_controller: RPMAnimator
var time_passed: float = 0.0
var is_player_near: bool = false

func _ready() -> void:
	$InteractionArea.body_entered.connect(_on_body_entered)
	$InteractionArea.body_exited.connect(_on_body_exited)
	dialogue_label.text = "PARZIVAL: 'Trouve la Clé de Cuivre!'"
	
	# Instantiate RPM Animation Library controller
	anim_controller = RPMAnimator.new()
	anim_controller.target_avatar_node = body_mesh
	add_child(anim_controller)

func _process(delta: float) -> void:
	# Floating & rotation animation for the Copper Key above Parzival's head
	time_passed += delta
	if key_mesh:
		key_mesh.rotation.y += delta * 2.0
		key_mesh.position.y = 2.4 + sin(time_passed * 3.0) * 0.1

func _on_body_entered(body: Node3D) -> void:
	if body.is_in_group("player"):
		is_player_near = true
		dialogue_label.text = "PARZIVAL: 'Bienvenue Gunter! Traverse le portail 03 pour la course!'"
		if anim_controller:
			anim_controller.set_state(RPMAnimator.AnimState.WAVE)

func _on_body_exited(body: Node3D) -> void:
	if body.is_in_group("player"):
		is_player_near = false
		dialogue_label.text = "PARZIVAL: 'Trouve la Clé de Cuivre!'"
		if anim_controller:
			anim_controller.set_state(RPMAnimator.AnimState.IDLE)