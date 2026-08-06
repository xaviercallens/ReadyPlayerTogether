extends CanvasLayer

# ==============================================================================
# PROJET OASIS - Scene Navigator & Autocomplete Teleporter (Shift + F)
# Free text search across all 12 scenes with live autocomplete filtering.
# ==============================================================================

signal teleport_requested(scene_path: String)

@onready var panel: Control = $Control
@onready var line_edit: LineEdit = $Control/Panel/VBoxContainer/LineEdit
@onready var item_list: ItemList = $Control/Panel/VBoxContainer/ItemList
@onready var status_label: Label = $Control/Panel/VBoxContainer/StatusLabel

const SCENE_REGISTRY = {
	"HUB Central (Cyberpunk Metropolis)": "res://scenes/hub/oasis_hub.tscn",
	"01: The Stacks (Trailer Park)": "res://scenes/demos/scene_01_the_stacks.tscn",
	"02: Halliday's Journal": "res://scenes/demos/scene_02_hallidays_journal.tscn",
	"03: Copper Race (New York)": "res://scenes/demos/scene_03_copper_race.tscn",
	"04: Distracted Globe (Club 0G)": "res://scenes/demos/scene_04_distracted_globe.tscn",
	"05: Retro Arcade (Aech Garage)": "res://scenes/demos/scene_05_arcade_retro.tscn",
	"06: Planet Doom (PvP Lava Zone)": "res://scenes/demos/scene_06_planet_doom.tscn",
	"07: Overlook Hotel (Shining)": "res://scenes/demos/scene_07_overlook_hotel.tscn",
	"08: IOI Citadel (Corporate Sorento)": "res://scenes/demos/scene_08_ioi_citadel.tscn",
	"09: Crystal Castle": "res://scenes/demos/scene_09_crystal_castle.tscn",
	"10: Easter Egg Room": "res://scenes/demos/scene_10_easter_egg.tscn",
	"11: Godot XR Dojo (Combat Arena)": "res://scenes/demos/scene_11_xr_dojo.tscn",
	"12: Library Showroom (Artifacts & Avatars)": "res://scenes/demos/scene_12_library_showroom.tscn"
}

var filtered_scenes: Array = []

func _ready() -> void:
	panel.visible = false
	line_edit.text_changed.connect(_on_text_changed)
	line_edit.text_submitted.connect(_on_text_submitted)
	item_list.item_activated.connect(_on_item_activated)

func toggle_navigator() -> void:
	panel.visible = not panel.visible
	if panel.visible:
		Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
		line_edit.text = ""
		line_edit.grab_focus()
		_update_autocomplete("")
	else:
		Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.shift_pressed and event.keycode == KEY_F:
			toggle_navigator()

func _update_autocomplete(query: String) -> void:
	item_list.clear()
	filtered_scenes.clear()
	
	var clean_query = query.strip_edges().to_lower()
	for title in SCENE_REGISTRY.keys():
		if clean_query.is_empty() or clean_query in title.to_lower():
			item_list.add_item(title)
			filtered_scenes.append(title)
			
	if filtered_scenes.size() > 0:
		status_label.text = "Found %d matching scene(s). Press Enter or Double-Click to Teleport." % filtered_scenes.size()
	else:
		status_label.text = "No scene matching '%s'. Try 'Doom', 'Race', 'Dojo', 'Showroom'..." % query

func _on_text_changed(new_text: String) -> void:
	_update_autocomplete(new_text)

func _on_text_submitted(text: String) -> void:
	if filtered_scenes.size() > 0:
		var target_title = filtered_scenes[0]
		_do_teleport(target_title)

func _on_item_activated(index: int) -> void:
	if index >= 0 and index < filtered_scenes.size():
		var target_title = filtered_scenes[index]
		_do_teleport(target_title)

func _do_teleport(title: String) -> void:
	var path = SCENE_REGISTRY.get(title, "")
	if not path.is_empty():
		print("[SCENE NAVIGATOR] Teleporting to: ", title)
		panel.visible = false
		get_tree().change_scene_to_file(path)