extends Node3D

# ==============================================================================
# PROJET OASIS - Central Hub Controller (Halliday's Arcade Lounge)
# Managed by Son (Pilot) & Father (Navigator)
# ==============================================================================

@export var keys_found: int = 0
@export var player_name: str = "Parzival_Jr"

@onready var status_label: Label3D = $CyberGrid/StatusLabel3D

func _ready() -> void:
	print("[OASIS HUB] Welcome to the OASIS Central Hub, " + player_name + "!")
	update_portal_status()

func update_portal_status() -> void:
	if status_label:
		status_label.text = "OASIS HUB - Clés Trouvées: " + str(keys_found) + " / 3\n[Portail 1: Clé de Cuivre OUVERT]"

func _on_portal_copper_body_entered(body: Node3D) -> void:
	if body.name == "VRPlayer" or body.is_in_group("player"):
		print("[OASIS HUB] Entering Copper Key Portal...")
		get_tree().change_scene_to_file("res://scenes/key_copper/copper_key_level.tscn")
