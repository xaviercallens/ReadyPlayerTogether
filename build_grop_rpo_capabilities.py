import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# 1. READY PLAYER ME RUNTIME AVATAR LOADER (scripts/ai/rpm_avatar_loader.gd)
# ==============================================================================
RPM_LOADER_GD = """
extends Node

# ==============================================================================
# PROJET OASIS - Ready Player Me (RPM) Runtime Avatar Loader
# (Inspired by Malcolm Nixon's GodotReadyPlayerMeAvatar plugin)
# Downloads and instantiates RPM avatars (.glb) at runtime with skeleton & blendshapes.
# ==============================================================================

signal avatar_loaded(avatar_node: Node3D)

var runtime_loader = preload("res://scripts/ai/runtime_asset_loader.gd").new()
var http_request: HTTPRequest

func _ready() -> void:
	http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(_on_avatar_download_completed)

func load_avatar_from_id(avatar_id: String) -> void:
	var avatar_url = "https://models.readyplayer.me/" + avatar_id + ".glb"
	print("[RPM LOADER] Downloading Ready Player Me avatar from: ", avatar_url)
	http_request.request(avatar_url)

func _on_avatar_download_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code == 200:
		var save_path = "user://rpm_avatar_temp.glb"
		var file = FileAccess.open(save_path, FileAccess.WRITE)
		file.store_buffer(body)
		file.close()
		
		var node = runtime_loader.load_glb_asset(save_path)
		if node:
			print("[RPM LOADER] RPM Avatar successfully loaded into Godot 4!")
			avatar_loaded.emit(node)
	else:
		print("[RPM LOADER] Failed to download RPM avatar. Response code: ", response_code)
"""

write_file(os.path.join(BASE_DIR, "scripts/ai/rpm_avatar_loader.gd"), RPM_LOADER_GD)

# ==============================================================================
# 2. INTERACTIVE VR INVENTORY SYSTEM (scenes/ui/vr_inventory_system.tscn)
# ==============================================================================
INVENTORY_GD = """
extends CanvasLayer

# ==============================================================================
# PROJET OASIS - Interactive VR Artifact Inventory System
# Press 'I' or Menu Button to view gathered Ready Player One Keys & Artifacts
# ==============================================================================

@onready var panel: Control = $Control
@onready var item_list: ItemList = $Control/Panel/VBoxContainer/ItemList
@onready var desc_label: Label = $Control/Panel/VBoxContainer/DescLabel

var artifacts = [
	{"name": "🔑 Copper Key", "desc": "The First Key of Halliday's Easter Egg Hunt. Unlocks the Jade Gate."},
	{"name": "🎲 Zemeckis Cube", "desc": "Reverses time in a 60-meter radius by 50 seconds."},
	{"name": "💣 Holy Hand Grenade", "desc": "Obliterates all enemies within impact range after a 3-second countdown."},
	{"name": "🛹 Cyberpunk Hoverboard", "desc": "Provides anti-gravity flight across OASIS plazas."},
	{"name": "🔮 Orb of Osuvox", "desc": "Creates a level-90 impenetrable forcefield sphere."}
]

func _ready() -> void:
	panel.visible = false
	item_list.item_selected.connect(_on_item_selected)
	_populate_items()

func _populate_items() -> void:
	item_list.clear()
	for item in artifacts:
		item_list.add_item(item["name"])

func toggle_inventory() -> void:
	panel.visible = not panel.visible
	if panel.visible:
		Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
	else:
		Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_I:
			toggle_inventory()

func _on_item_selected(index: int) -> void:
	if index >= 0 and index < artifacts.size():
		desc_label.text = artifacts[index]["desc"]
"""

INVENTORY_TSCN = """
[gd_scene load_steps=2 format=3 uid="uid://vr_inventory_system_ui"]

[ext_resource type="Script" path="res://scripts/ui/vr_inventory_system.gd" id="1_script"]

[node name="VRInventorySystem" type="CanvasLayer"]
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
offset_top = -200.0
offset_right = 300.0
offset_bottom = 200.0
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

[node name="Title" type="Label" parent="Control/Panel/VBoxContainer"]
layout_mode = 2
theme_override_colors/font_color = Color(0.0, 0.9, 1.0, 1)
theme_override_font_sizes/font_size = 22
text = "🎒 OASIS ARTIFACT & KEY INVENTORY (Key: I)"
horizontal_alignment = 1

[node name="ItemList" type="ItemList" parent="Control/Panel/VBoxContainer"]
custom_minimum_size = Vector2(0, 180)
layout_mode = 2
theme_override_font_sizes/font_size = 16

[node name="DescLabel" type="Label" parent="Control/Panel/VBoxContainer"]
layout_mode = 2
theme_override_colors/font_color = Color(0.9, 0.9, 0.9, 1)
theme_override_font_sizes/font_size = 14
text = "Select an artifact above to inspect its RPO lore and powers."
autowrap_mode = 2
"""

write_file(os.path.join(BASE_DIR, "scripts/ui/vr_inventory_system.gd"), INVENTORY_GD)
write_file(os.path.join(BASE_DIR, "scenes/ui/vr_inventory_system.tscn"), INVENTORY_TSCN)

# ==============================================================================
# 3. ATTACH INVENTORY SYSTEM TO PC_PLAYER & VR_PLAYER
# ==============================================================================
PC_PLAYER_TSCN = """
[gd_scene load_steps=13 format=3 uid="uid://pc_player_scene"]

[ext_resource type="Script" path="res://scripts/player_vr/pc_player.gd" id="1_pc_script"]
[ext_resource type="PackedScene" uid="uid://scene_navigator_ui" path="res://scenes/ui/scene_navigator.tscn" id="2_navigator"]
[ext_resource type="PackedScene" uid="uid://command_menu_ui" path="res://scenes/ui/command_menu.tscn" id="3_command_menu"]
[ext_resource type="PackedScene" uid="uid://ai_prompt_tool_ui" path="res://scenes/ui/ai_prompt_tool.tscn" id="4_prompt_tool"]
[ext_resource type="PackedScene" uid="uid://vr_inventory_system_ui" path="res://scenes/ui/vr_inventory_system.tscn" id="5_inventory"]

[sub_resource type="CapsuleShape3D" id="CapsuleShape3D_player"]

[sub_resource type="StandardMaterial3D" id="Mat_MannequinBody"]
albedo_color = Color(0.85, 0.88, 0.95, 1)
metallic = 0.8
roughness = 0.2

[sub_resource type="StandardMaterial3D" id="Mat_Visor"]
albedo_color = Color(0.0, 0.9, 1.0, 1)
emission_enabled = true
emission = Color(0.0, 0.9, 1.0, 1)
emission_energy_multiplier = 4.0

[sub_resource type="CapsuleMesh" id="Mesh_Torso"]
material = SubResource("Mat_MannequinBody")
radius = 0.35
height = 1.05

[sub_resource type="SphereMesh" id="Mesh_Head"]
material = SubResource("Mat_MannequinBody")
radius = 0.22
height = 0.44

[sub_resource type="BoxMesh" id="Mesh_Visor"]
material = SubResource("Mat_Visor")
size = Vector3(0.3, 0.08, 0.12)

[sub_resource type="CylinderMesh" id="Mesh_Limb"]
material = SubResource("Mat_MannequinBody")
top_radius = 0.09
bottom_radius = 0.07
height = 0.85

[node name="PCPlayer" type="CharacterBody3D" groups=["player"]]
script = ExtResource("1_pc_script")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0)
shape = SubResource("CapsuleShape3D_player")

[node name="MannequinMesh" type="Node3D" parent="."]

[node name="Torso" type="MeshInstance3D" parent="MannequinMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.1, 0)
mesh = SubResource("Mesh_Torso")

[node name="Head" type="MeshInstance3D" parent="MannequinMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.72, 0)
mesh = SubResource("Mesh_Head")

[node name="Visor" type="MeshInstance3D" parent="MannequinMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.75, -0.18)
mesh = SubResource("Mesh_Visor")

[node name="LeftLeg" type="MeshInstance3D" parent="MannequinMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.16, 0.42, 0)
mesh = SubResource("Mesh_Limb")

[node name="RightLeg" type="MeshInstance3D" parent="MannequinMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.16, 0.42, 0)
mesh = SubResource("Mesh_Limb")

[node name="Camera3D" type="Camera3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.9659, 0.2588, 0, -0.2588, 0.9659, 0, 2.8, 3.8)
current = true
near = 0.05

[node name="SceneNavigator" parent="." instance=ExtResource("2_navigator")]

[node name="CommandMenu" parent="." instance=ExtResource("3_command_menu")]

[node name="AIPromptTool" parent="." instance=ExtResource("4_prompt_tool")]

[node name="VRInventorySystem" parent="." instance=ExtResource("5_inventory")]
"""

write_file(os.path.join(BASE_DIR, "scenes/player_vr/pc_player.tscn"), PC_PLAYER_TSCN)

print("Godot-Ready-Player-One & RPM Capabilities (RPM Avatar Loader, VR Inventory System) generated successfully!")
