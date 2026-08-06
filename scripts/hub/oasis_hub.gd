extends Node3D

const DEMO_SCENES = [
	"res://scenes/demos/scene_01_the_stacks.tscn",
	"res://scenes/demos/scene_02_hallidays_journal.tscn",
	"res://scenes/demos/scene_03_copper_race.tscn",
	"res://scenes/demos/scene_04_distracted_globe.tscn",
	"res://scenes/demos/scene_05_arcade_retro.tscn",
	"res://scenes/demos/scene_06_planet_doom.tscn",
	"res://scenes/demos/scene_07_overlook_hotel.tscn",
	"res://scenes/demos/scene_08_ioi_citadel.tscn",
	"res://scenes/demos/scene_09_crystal_castle.tscn",
	"res://scenes/demos/scene_10_easter_egg.tscn",
	"res://scenes/demos/scene_11_xr_dojo.tscn",
	"res://scenes/demos/scene_12_library_showroom.tscn"
]

func _ready() -> void:
	print("[OASIS HUB] Active. Press 1-9, 0 for Demos | Press L for Library Showroom!")
	_connect_portals()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_L:
			_teleport_to_demo(12)
			return
		match event.keycode:
			KEY_1: _teleport_to_demo(1)
			KEY_2: _teleport_to_demo(2)
			KEY_3: _teleport_to_demo(3)
			KEY_4: _teleport_to_demo(4)
			KEY_5: _teleport_to_demo(5)
			KEY_6: _teleport_to_demo(6)
			KEY_7: _teleport_to_demo(7)
			KEY_8: _teleport_to_demo(8)
			KEY_9: _teleport_to_demo(9)
			KEY_0: _teleport_to_demo(10)

func _connect_portals() -> void:
	for i in range(1, 11):
		var portal_name = "Portal_%02d" % i
		var portal_node = get_node_or_null("Portals/" + portal_name)
		if portal_node:
			portal_node.body_entered.connect(_on_portal_entered.bind(i))

func _on_portal_entered(body: Node3D, demo_index: int) -> void:
	if body.is_in_group("player"):
		_teleport_to_demo(demo_index)

func _teleport_to_demo(demo_index: int) -> void:
	if demo_index >= 1 and demo_index <= DEMO_SCENES.size():
		print("[OASIS HUB] Teleporting to Scene %02d..." % demo_index)
		get_tree().change_scene_to_file(DEMO_SCENES[demo_index - 1])