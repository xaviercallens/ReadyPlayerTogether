extends Node3D

# ==============================================================================
# PROJET OASIS - La Clé de Cuivre (Copper Key Action Dodge Game)
# Scripted for Father-Son Pair Programming
# ==============================================================================

@export var current_score: int = 0
@export var key_unlocked: bool = false

@onready var score_label: Label3D = $UI/ScoreLabel3D

func _ready() -> void:
	print("[CLÉ DE CUIVRE] Mini-jeu démarré ! Esquivez les obstacles et attrapez la Clé !")
	update_score_ui()

func add_points(amount: int) -> void:
	current_score += amount
	update_score_ui()
	if current_score >= 100 and not key_unlocked:
		unlock_copper_key()

func update_score_ui() -> void:
	if score_label:
		score_label.text = "SCORE: " + str(current_score) + " / 100"

func unlock_copper_key() -> void:
	key_unlocked = true
	print("[CLÉ DE CUIVRE] FÉLICITATIONS ! La Clé de Cuivre est à vous !")
	if score_label:
		score_label.text = "VICTOIRE ! CLÉ DE CUIVRE OBTENUE !"

func _on_key_collect_area_body_entered(body: Node3D) -> void:
	add_points(100)
