import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# 1. SCENE NAVIGATOR SCRIPT (scripts/ui/scene_navigator.gd)
# ==============================================================================
NAVIGATOR_GD = """
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
"""

write_file(os.path.join(BASE_DIR, "scripts/ui/scene_navigator.gd"), NAVIGATOR_GD)

# ==============================================================================
# 2. SCENE NAVIGATOR UI SCENE (scenes/ui/scene_navigator.tscn)
# ==============================================================================
NAVIGATOR_TSCN = """
[gd_scene load_steps=2 format=3 uid="uid://scene_navigator_ui"]

[ext_resource type="Script" path="res://scripts/ui/scene_navigator.gd" id="1_script"]

[node name="SceneNavigator" type="CanvasLayer"]
process_mode = 3
script = ExtResource("1_script")

[node name="Control" type="Control" parent="."]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2

[node name="Panel" type="Panel" parent="Control"]
layout_mode = 1
anchors_preset = 8
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = -300.0
offset_top = -220.0
offset_right = 300.0
offset_bottom = 220.0
grow_horizontal = 2
grow_vertical = 2

[node name="VBoxContainer" type="VBoxContainer" parent="Control/Panel"]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
offset_left = 15.0
offset_top = 15.0
offset_right = -15.0
offset_bottom = -15.0
grow_horizontal = 2
grow_vertical = 2
theme_override_constants/separation = 10

[node name="TitleLabel" type="Label" parent="Control/Panel/VBoxContainer"]
layout_mode = 2
theme_override_font_sizes/font_size = 22
text = "🌀 OASIS SCENE NAVIGATOR (Shift + F)"
horizontal_alignment = 1

[node name="LineEdit" type="LineEdit" parent="Control/Panel/VBoxContainer"]
layout_mode = 2
theme_override_font_sizes/font_size = 18
placeholder_text = "Type scene name (e.g. Doom, Race, Dojo, Showroom)..."

[node name="ItemList" type="ItemList" parent="Control/Panel/VBoxContainer"]
layout_mode = 2
size_flags_vertical = 3
theme_override_font_sizes/font_size = 16

[node name="StatusLabel" type="Label" parent="Control/Panel/VBoxContainer"]
layout_mode = 2
theme_override_font_sizes/font_size = 14
text = "Press Enter or Double-Click to Teleport instantly."
horizontal_alignment = 1
"""

write_file(os.path.join(BASE_DIR, "scenes/ui/scene_navigator.tscn"), NAVIGATOR_TSCN)

# ==============================================================================
# 3. ATTACH SCENE NAVIGATOR TO PC PLAYER (pc_player.tscn & pc_player.gd)
# ==============================================================================
PC_PLAYER_TSCN = """
[gd_scene load_steps=4 format=3 uid="uid://pc_player_scene"]

[ext_resource type="Script" path="res://scripts/player_vr/pc_player.gd" id="1_pc_script"]
[ext_resource type="PackedScene" uid="uid://scene_navigator_ui" path="res://scenes/ui/scene_navigator.tscn" id="2_navigator"]

[sub_resource type="CapsuleShape3D" id="CapsuleShape3D_player"]

[node name="PCPlayer" type="CharacterBody3D" groups=["player"]]
script = ExtResource("1_pc_script")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0)
shape = SubResource("CapsuleShape3D_player")

[node name="Camera3D" type="Camera3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.6, 0)
current = true

[node name="SceneNavigator" parent="." instance=ExtResource("2_navigator")]
"""

write_file(os.path.join(BASE_DIR, "scenes/player_vr/pc_player.tscn"), PC_PLAYER_TSCN)

print("OASIS Scene Navigator UI & Autocomplete Teleporter (Shift+F) generated successfully!")
