extends Node3D

# ==============================================================================
# PROJET OASIS - Cyberpunk Hub Central Controller
# Manages portal teleportation to the 10 Ready Player One demo scenes.
# ==============================================================================

@export var default_avatar_url: String = "https://models.readyplayer.me/64bfa15f0e72c63d7e3934a6.glb"

func _ready() -> void:
	print("[OASIS HUB] Cyberpunk Hub initialized. RTX 2070 Shaders Active.")
	_connect_portals()

func _connect_portals() -> void:
	for i in range(1, 11):
		var portal_name = "Portal_%02d" % i
		var portal_node = get_node_or_null("Portals/" + portal_name)
		if portal_node:
			portal_node.body_entered.connect(_on_portal_entered.bind(i))

func _on_portal_entered(body: Node3D, demo_index: int) -> void:
	if body.is_in_group("player"):
		print("[OASIS HUB] Player entered Portal %02d! Teleporting..." % demo_index)
		var scene_paths = [
			"res://scenes/demos/scene_01_the_stacks.tscn",
			"res://scenes/demos/scene_02_hallidays_journal.tscn",
			"res://scenes/demos/scene_03_copper_race.tscn",
			"res://scenes/demos/scene_04_distracted_globe.tscn",
			"res://scenes/demos/scene_05_arcade_retro.tscn",
			"res://scenes/demos/scene_06_planet_doom.tscn",
			"res://scenes/demos/scene_07_overlook_hotel.tscn",
			"res://scenes/demos/scene_08_ioi_citadel.tscn",
			"res://scenes/demos/scene_09_crystal_castle.tscn",
			"res://scenes/demos/scene_10_easter_egg.tscn"
		]
		if demo_index >= 1 and demo_index <= scene_paths.size():
			get_tree().change_scene_to_file(scene_paths[demo_index - 1])