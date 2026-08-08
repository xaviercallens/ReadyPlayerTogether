extends CharacterBody3D

# ==============================================================================
# PROJET OASIS - Parzival NPC (GDQuest 3D Mannequin Avatar)
# ==============================================================================

@onready var key_mesh: Node3D = get_node_or_null("KeyMesh")
@onready var dialogue_label: Label3D = get_node_or_null("DialogueLabel")
@onready var anim_player: AnimationPlayer = get_node_or_null("MeshPivot/MannequinyModel/AnimationPlayer")

var time_passed: float = 0.0
var is_player_near: bool = false

func _ready() -> void:
	if has_node("InteractionArea"):
		$InteractionArea.body_entered.connect(_on_body_entered)
		$InteractionArea.body_exited.connect(_on_body_exited)
	if dialogue_label != null:
		dialogue_label.text = "PARZIVAL: 'Trouve la Clé de Cuivre dans le Portail 03!'"
	if anim_player != null and anim_player.has_animation("idle"):
		anim_player.play("idle")

func _process(delta: float) -> void:
	time_passed += delta
	if key_mesh != null:
		key_mesh.rotation.y += delta * 2.0
		key_mesh.position.y = 2.4 + sin(time_passed * 3.0) * 0.1

func _on_body_entered(body: Node3D) -> void:
	if body != null and body.is_in_group("player"):
		is_player_near = true
		if dialogue_label != null:
			dialogue_label.text = "PARZIVAL: 'Bienvenue Gunter! Le Mannequin GDQuest est prêt!'"
		if anim_player != null:
			if anim_player.has_animation("fight_idle"):
				anim_player.play("fight_idle")

func _on_body_exited(body: Node3D) -> void:
	if body != null and body.is_in_group("player"):
		is_player_near = false
		if dialogue_label != null:
			dialogue_label.text = "PARZIVAL: 'Trouve la Clé de Cuivre!'"
		if anim_player != null:
			if anim_player.has_animation("idle"):
				anim_player.play("idle")
