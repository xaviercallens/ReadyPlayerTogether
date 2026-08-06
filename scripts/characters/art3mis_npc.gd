extends CharacterBody3D

@onready var key_mesh: MeshInstance3D = $KeyMesh
@onready var dialogue_label: Label3D = $DialogueLabel
@onready var body_mesh: Node3D = $BodyMesh

var anim_controller: RPMAnimator
var time_passed: float = 0.0

func _ready() -> void:
	$InteractionArea.body_entered.connect(_on_body_entered)
	$InteractionArea.body_exited.connect(_on_body_exited)
	dialogue_label.text = "ART3MIS: 'La Clé de Jade t'attend...'"
	
	anim_controller = RPMAnimator.new()
	anim_controller.target_avatar_node = body_mesh
	add_child(anim_controller)

func _process(delta: float) -> void:
	time_passed += delta
	if key_mesh:
		key_mesh.rotation.y += delta * 2.5
		key_mesh.position.y = 2.4 + sin(time_passed * 3.5) * 0.1

func _on_body_entered(body: Node3D) -> void:
	if body.is_in_group("player"):
		dialogue_label.text = "ART3MIS: 'Salut Gunter! La Clé de Jade est cachée dans le portail 05!'"
		if anim_controller:
			anim_controller.set_state(RPMAnimator.AnimState.WAVE)

func _on_body_exited(body: Node3D) -> void:
	if body.is_in_group("player"):
		dialogue_label.text = "ART3MIS: 'La Clé de Jade t'attend...'"
		if anim_controller:
			anim_controller.set_state(RPMAnimator.AnimState.IDLE)