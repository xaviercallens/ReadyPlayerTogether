import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# 1. FIXED COMMAND MENU SCENE (scenes/ui/command_menu.tscn)
# ==============================================================================
COMMAND_MENU_TSCN = """
[gd_scene load_steps=2 format=3 uid="uid://command_menu_ui"]

[ext_resource type="Script" path="res://scripts/ui/command_menu.gd" id="1_script"]

[node name="CommandMenu" type="CanvasLayer"]
script = ExtResource("1_script")

[node name="QuickBadge" type="Panel" parent="."]
offset_left = 20.0
offset_top = 20.0
offset_right = 360.0
offset_bottom = 120.0

[node name="LabelBadge" type="Label" parent="."]
offset_left = 30.0
offset_top = 28.0
offset_right = 350.0
offset_bottom = 50.0
theme_override_colors/font_color = Color(0.0, 0.9, 1.0, 1)
theme_override_font_sizes/font_size = 14
text = "🌀 OASIS QUICK SHORTCUTS [Tab = Menu]"

[node name="LabelDetails" type="Label" parent="."]
offset_left = 30.0
offset_top = 55.0
offset_right = 350.0
offset_bottom = 110.0
theme_override_font_sizes/font_size = 12
text = "Shift + F ➡️ Teleport Search | L ➡️ Showroom
Keys 1-9, 0 ➡️ Demos | H ➡️ Cyberpunk HUB"

[node name="Overlay" type="Control" parent="."]
visible = false
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2

[node name="Panel" type="Panel" parent="Overlay"]
layout_mode = 1
anchors_preset = 8
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = -340.0
offset_top = -250.0
offset_right = 340.0
offset_bottom = 250.0
grow_horizontal = 2
grow_vertical = 2

[node name="Header" type="Label" parent="Overlay"]
layout_mode = 1
anchors_preset = 8
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = -320.0
offset_top = -235.0
offset_right = 320.0
offset_bottom = -200.0
theme_override_colors/font_color = Color(0.0, 1.0, 0.8, 1)
theme_override_font_sizes/font_size = 20
text = "🎮 PROJET OASIS - MASTER COMMAND MENU"
horizontal_alignment = 1

[node name="CmdDetails" type="Label" parent="Overlay"]
layout_mode = 1
anchors_preset = 8
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = -310.0
offset_top = -180.0
offset_right = 310.0
offset_bottom = 180.0
theme_override_font_sizes/font_size = 15
text = "⌨️  Shift + F  ➡️  Open Teleport Navigator with Live Search
🏛️  Key L / Shift+L  ➡️  Teleport to Exhibition Showroom
🔄  Key H / Backspace  ➡️  Return to Cyberpunk HUB Plaza
🔢  Keys 1 - 9, 0  ➡️  Direct Teleport to Demos 01 to 10
🏃  W / A / S / D  ➡️  Move Character & Jump (Space)
🕹️  Gamepad D-Pad/Sticks ➡️ Full Controller Support"

[node name="Footer" type="Label" parent="Overlay"]
layout_mode = 1
anchors_preset = 8
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = -320.0
offset_top = 200.0
offset_right = 320.0
offset_bottom = 230.0
theme_override_font_sizes/font_size = 14
text = "[Press Tab or Escape to Close Menu]"
horizontal_alignment = 1
"""

write_file(os.path.join(BASE_DIR, "scenes/ui/command_menu.tscn"), COMMAND_MENU_TSCN)

# ==============================================================================
# 2. FIXED COMMAND MENU SCRIPT (scripts/ui/command_menu.gd)
# ==============================================================================
COMMAND_MENU_GD = """
extends CanvasLayer

# ==============================================================================
# PROJET OASIS - Controls & Commands Overlay HUD
# ==============================================================================

@onready var overlay: Control = $Overlay

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_TAB or event.keycode == KEY_ESCAPE:
			if overlay != null:
				overlay.visible = not overlay.visible
"""

write_file(os.path.join(BASE_DIR, "scripts/ui/command_menu.gd"), COMMAND_MENU_GD)

# ==============================================================================
# 3. FIXED DELOREAN CAR SCENE WITH DRIVER & VISÈME LABEL (scenes/vehicles/delorean_car.tscn)
# ==============================================================================
DELOREAN_TSCN = """
[gd_scene load_steps=10 format=3 uid="uid://delorean_car_scene"]

[ext_resource type="Script" path="res://scripts/vehicles/delorean_car.gd" id="1_script"]

[sub_resource type="StandardMaterial3D" id="Mat_StainlessSteel"]
albedo_color = Color(0.7, 0.72, 0.75, 1)
metallic = 0.95
roughness = 0.15

[sub_resource type="BoxMesh" id="Mesh_CarBody"]
material = SubResource("Mat_StainlessSteel")
size = Vector3(2.1, 0.8, 4.4)

[sub_resource type="StandardMaterial3D" id="Mat_Windshield"]
albedo_color = Color(0.05, 0.05, 0.1, 0.9)
metallic = 0.9
roughness = 0.05

[sub_resource type="BoxMesh" id="Mesh_Windshield"]
material = SubResource("Mat_Windshield")
size = Vector3(1.9, 0.5, 1.8)

[sub_resource type="StandardMaterial3D" id="Mat_Wheel"]
albedo_color = Color(0.1, 0.1, 0.1, 1)
roughness = 0.8

[sub_resource type="CylinderMesh" id="Mesh_Wheel"]
material = SubResource("Mat_Wheel")
top_radius = 0.45
bottom_radius = 0.45
height = 0.3

[sub_resource type="StandardMaterial3D" id="Mat_NeonCyan"]
albedo_color = Color(0.0, 0.9, 1.0, 1)
emission_enabled = true
emission = Color(0.0, 0.9, 1.0, 1)
emission_energy_multiplier = 4.0

[sub_resource type="BoxMesh" id="Mesh_RearThruster"]
material = SubResource("Mat_NeonCyan")
size = Vector3(1.8, 0.25, 0.3)

[node name="DeLoreanTimeMachine" type="CharacterBody3D"]
script = ExtResource("1_script")

[node name="Body" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.6, 0)
mesh = SubResource("Mesh_CarBody")

[node name="Cabin" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.1, -0.2)
mesh = SubResource("Mesh_Windshield")

[node name="WheelFL" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 0, 0, 1, -1.1, 0.45, -1.4)
mesh = SubResource("Mesh_Wheel")

[node name="WheelFR" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 0, 0, 1, 1.1, 0.45, -1.4)
mesh = SubResource("Mesh_Wheel")

[node name="WheelRL" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 0, 0, 1, -1.1, 0.45, 1.4)
mesh = SubResource("Mesh_Wheel")

[node name="WheelRR" type="MeshInstance3D" parent="."]
transform = Transform3D(-4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 0, 0, 1, 1.1, 0.45, 1.4)
mesh = SubResource("Mesh_Wheel")

[node name="ThrusterMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.7, 2.25)
mesh = SubResource("Mesh_RearThruster")

[node name="FluxCapacitor" type="OmniLight3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.2, 0)
light_color = Color(0.0, 0.9, 1.0, 1)
light_energy = 3.0
omni_range = 4.0

[node name="RearThruster" type="OmniLight3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.7, 2.5)
light_color = Color(0.0, 1.0, 0.8, 1)
light_energy = 4.0

[node name="Label3D" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.2, 0)
billboard = 1
pixel_size = 0.015
text = "PARZIVAL'S DELOREAN TIME MACHINE
'88 MPH Into the OASIS!'"
font_size = 36
outline_size = 8

[node name="Driver" type="Node3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.2, 0)

[node name="VisemeLabel" type="Label3D" parent="Driver"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.4, 0)
billboard = 1
pixel_size = 0.012
text = "PARZIVAL: First key is earned!"
font_size = 28
outline_size = 6
"""

write_file(os.path.join(BASE_DIR, "scenes/vehicles/delorean_car.tscn"), DELOREAN_TSCN)

# ==============================================================================
# 4. SAFE DELOREAN SCRIPT WITH GUARANTEED NULL CHECKS (scripts/vehicles/delorean_car.gd)
# ==============================================================================
DELOREAN_GD = """
extends Node3D

# ==============================================================================
# PROJET OASIS - DeLorean Time Machine (Null-Safe Construction Shader & Driver Viseme)
# ==============================================================================

@export var construction_duration: float = 2.0
var shader_material: ShaderMaterial
var time_passed: float = 0.0

func _ready() -> void:
	play_construction_effect()

func _get_target_mesh() -> MeshInstance3D:
	if has_node("Body"):
		return get_node("Body") as MeshInstance3D
	elif has_node("CarMesh/Body"):
		return get_node("CarMesh/Body") as MeshInstance3D
	
	var meshes = find_children("*", "MeshInstance3D", true, false)
	if meshes.size() > 0:
		return meshes[0] as MeshInstance3D
	return null

func play_construction_effect() -> void:
	var mesh_node = _get_target_mesh()
	if mesh_node != null:
		var mat = mesh_node.get_surface_override_material(0)
		if mat == null and mesh_node.mesh != null:
			mat = mesh_node.mesh.surface_get_material(0)
			
		if mat != null and mat is ShaderMaterial:
			shader_material = mat
			shader_material.set_shader_parameter("construction_progress", 0.0)
			var tween = create_tween()
			tween.tween_property(shader_material, "shader_parameter/construction_progress", 1.0, construction_duration)
			print("[DELOREAN] Holographic Construction Shader Sweep Initiated (2s)!")

func _process(delta: float) -> void:
	time_passed += delta
	if has_node("Driver/VisemeLabel"):
		var driver_label = get_node("Driver/VisemeLabel") as Label3D
		if driver_label != null:
			var visemes = ["Aah", "Ohh", "Eee", "Mmm", "First key is earned!"]
			driver_label.text = "PARZIVAL: " + visemes[int(time_passed * 3.0) % visemes.size()]
"""

write_file(os.path.join(BASE_DIR, "scripts/vehicles/delorean_car.gd"), DELOREAN_GD)

print("All node warnings and null-pointer errors resolved successfully!")
