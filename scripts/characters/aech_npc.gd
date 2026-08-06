extends CharacterBody3D

@onready var dialogue_label: Label3D = $DialogueLabel
@onready var body_mesh: Node3D = $BodyMesh

var anim_controller: RPMAnimator
var time_passed: float = 0.0

func _ready() -> void:
	$InteractionArea.body_entered.connect(_on_body_entered)
	$InteractionArea.body_exited.connect(_on_body_exited)
	dialogue_label.text = "AECH: 'Bienvenue au Garage!'"
	
	anim_controller = RPMAnimator.new()
	anim_controller.target_avatar_node = body_mesh
	add_child(anim_controller)

func _on_body_entered(body: Node3D) -> void:
	if body.is_in_group("player"):
		dialogue_label.text = "AECH: 'Hey Gunter! Besoin de réparer ton Iron Giant ou ta DeLorean?'"
		if anim_controller:
			anim_controller.set_state(RPMAnimator.AnimState.WAVE)

func _on_body_exited(body: Node3D) -> void:
	if body.is_in_group("player"):
		dialogue_label.text = "AECH: 'Bienvenue au Garage!'"
		if anim_controller:
			anim_controller.set_state(RPMAnimator.AnimState.IDLE)