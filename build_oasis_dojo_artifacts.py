import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# 1. ZEMECKIS CUBE ARTIFACT (Time Reverser)
# ==============================================================================
ZEMECKIS_GD = """
extends Area3D

@export var rotation_speed: float = 2.0
var time_passed: float = 0.0

func _process(delta: float) -> void:
	time_passed += delta
	rotation.y += delta * rotation_speed
	position.y = 1.2 + sin(time_passed * 3.0) * 0.1

func _on_body_entered(body: Node3D) -> void:
	if body.is_in_group("player"):
		print("[ARTIFACT] Zemeckis Cube Activated! Reversing Time 60 seconds...")
"""

ZEMECKIS_TSCN = """
[gd_scene load_steps=5 format=3 uid="uid://zemeckis_cube_scene"]

[ext_resource type="Script" path="res://scripts/artifacts/zemeckis_cube.gd" id="1_script"]

[sub_resource type="StandardMaterial3D" id="Mat_Rubik"]
albedo_color = Color(0.0, 0.8, 1.0, 1)
metallic = 0.8
roughness = 0.2
emission_enabled = true
emission = Color(0.0, 0.8, 1.0, 1)
emission_energy_multiplier = 3.0

[sub_resource type="BoxMesh" id="Mesh_Cube"]
material = SubResource("Mat_Rubik")
size = Vector3(0.4, 0.4, 0.4)

[sub_resource type="SphereShape3D" id="Shape_Interact"]
radius = 1.5

[node name="ZemeckisCube" type="Area3D"]
script = ExtResource("1_script")

[node name="MeshInstance3D" type="MeshInstance3D" parent="."]
mesh = SubResource("Mesh_Cube")

[node name="Label3D" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.6, 0)
billboard = 1
pixel_size = 0.012
text = "ARTIFACT: Zemeckis Cube"
font_size = 32
outline_size = 6

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
shape = SubResource("Shape_Interact")
"""

# ==============================================================================
# 2. HOLY HAND GRENADE OF ANTIOCH
# ==============================================================================
GRENADE_GD = """
extends Area3D

var time_passed: float = 0.0

func _process(delta: float) -> void:
	time_passed += delta
	rotation.y += delta * 1.5
	position.y = 1.2 + sin(time_passed * 2.5) * 0.08

func _on_body_entered(body: Node3D) -> void:
	if body.is_in_group("player"):
		print("[ARTIFACT] Holy Hand Grenade acquired! Massive AOE Blast Ready!")
"""

GRENADE_TSCN = """
[gd_scene load_steps=5 format=3 uid="uid://holy_hand_grenade_scene"]

[ext_resource type="Script" path="res://scripts/artifacts/holy_hand_grenade.gd" id="1_script"]

[sub_resource type="StandardMaterial3D" id="Mat_GoldCross"]
albedo_color = Color(1.0, 0.85, 0.1, 1)
metallic = 0.95
roughness = 0.1
emission_enabled = true
emission = Color(1.0, 0.85, 0.1, 1)
emission_energy_multiplier = 2.5

[sub_resource type="SphereMesh" id="Mesh_Grenade"]
material = SubResource("Mat_GoldCross")
radius = 0.25
height = 0.5

[sub_resource type="SphereShape3D" id="Shape_Interact"]
radius = 1.5

[node name="HolyHandGrenade" type="Area3D"]
script = ExtResource("1_script")

[node name="MeshInstance3D" type="MeshInstance3D" parent="."]
mesh = SubResource("Mesh_Grenade")

[node name="Label3D" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.6, 0)
billboard = 1
pixel_size = 0.012
text = "ARTIFACT: Holy Hand Grenade"
font_size = 32
outline_size = 6

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
shape = SubResource("Shape_Interact")
"""

# ==============================================================================
# 3. IRON GIANT MECH COMPANION (Aech's Masterpiece)
# ==============================================================================
GIANT_GD = """
extends CharacterBody3D

@onready var label: Label3D = $Label3D
var time_passed: float = 0.0

func _process(delta: float) -> void:
	time_passed += delta
	# Subtle breathing animation for the giant mech
	$MechBody.position.y = 4.0 + sin(time_passed * 1.5) * 0.1
"""

GIANT_TSCN = """
[gd_scene load_steps=7 format=3 uid="uid://iron_giant_companion_scene"]

[ext_resource type="Script" path="res://scripts/characters/iron_giant_companion.gd" id="1_script"]

[sub_resource type="StandardMaterial3D" id="Mat_Steel"]
albedo_color = Color(0.3, 0.35, 0.4, 1)
metallic = 0.9
roughness = 0.3

[sub_resource type="StandardMaterial3D" id="Mat_Eyes"]
albedo_color = Color(1.0, 0.9, 0.2, 1)
emission_enabled = true
emission = Color(1.0, 0.9, 0.2, 1)
emission_energy_multiplier = 5.0

[sub_resource type="BoxMesh" id="Mesh_GiantTorso"]
material = SubResource("Mat_Steel")
size = Vector3(3.5, 4.5, 2.5)

[sub_resource type="SphereMesh" id="Mesh_GiantHead"]
material = SubResource("Mat_Steel")
radius = 1.2
height = 2.4

[sub_resource type="BoxMesh" id="Mesh_Eyes"]
material = SubResource("Mat_Eyes")
size = Vector3(1.6, 0.4, 0.3)

[node name="IronGiantCompanion" type="CharacterBody3D"]
script = ExtResource("1_script")

[node name="MechBody" type="Node3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4.0, 0)

[node name="Torso" type="MeshInstance3D" parent="MechBody"]
mesh = SubResource("Mesh_GiantTorso")

[node name="Head" type="MeshInstance3D" parent="MechBody"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3.2, 0)
mesh = SubResource("Mesh_GiantHead")

[node name="Eyes" type="MeshInstance3D" parent="MechBody"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3.3, -1.1)
mesh = SubResource("Mesh_Eyes")

[node name="Label3D" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 9.5, 0)
billboard = 1
pixel_size = 0.02
text = "AECH'S IRON GIANT MECH
'I Am Not A Gun!'"
font_size = 48
outline_size = 12
"""

# ==============================================================================
# 4. GODOT XR DOJO TRAINING ARENA DEMO SCENE (scene_11_xr_dojo.tscn)
# ==============================================================================
DOJO_TSCN = """
[gd_scene load_steps=7 format=3 uid="uid://demo_11_xr_dojo"]

[ext_resource type="PackedScene" uid="uid://pc_player_scene" path="res://scenes/player_vr/pc_player.tscn" id="1_player"]
[ext_resource type="Script" path="res://scripts/demos/demo_return.gd" id="2_return_script"]

[sub_resource type="Environment" id="Environment_dojo"]
background_mode = 1
background_color = Color(0.05, 0.05, 0.1, 1)
glow_enabled = true
glow_intensity = 2.0
glow_bloom = 0.5
glow_blend_mode = 0
volumetric_fog_enabled = true
volumetric_fog_density = 0.008
volumetric_fog_albedo = Color(0.8, 0.2, 1.0, 1)
ssr_enabled = true

[sub_resource type="StandardMaterial3D" id="Mat_DojoFloor"]
albedo_color = Color(0.12, 0.1, 0.18, 1)
metallic = 0.8
roughness = 0.2

[sub_resource type="PlaneMesh" id="Plane_Dojo"]
material = SubResource("Mat_DojoFloor")
size = Vector3(50, 50)

[sub_resource type="StandardMaterial3D" id="Mat_Target"]
albedo_color = Color(1.0, 0.2, 0.4, 1)
emission_enabled = true
emission = Color(1.0, 0.2, 0.4, 1)
emission_energy_multiplier = 3.0

[sub_resource type="CylinderMesh" id="Mesh_Target"]
material = SubResource("Mat_Target")
top_radius = 1.0
bottom_radius = 1.0
height = 0.2

[node name="GodotXRDojoArena" type="Node3D"]
script = ExtResource("2_return_script")

[node name="WorldEnvironment" type="WorldEnvironment" parent="."]
environment = SubResource("Environment_dojo")

[node name="DirectionalLight3D" type="DirectionalLight3D" parent="."]
transform = Transform3D(0.866025, -0.353553, 0.353553, 0, 0.707107, 0.707107, -0.5, -0.612372, 0.612372, 0, 10, 0)
light_color = Color(0.9, 0.4, 1.0, 1)
shadow_enabled = true

[node name="Floor" type="MeshInstance3D" parent="."]
mesh = SubResource("Plane_Dojo")

[node name="Label3D" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4.0, -8)
billboard = 1
pixel_size = 0.02
text = "GODOT XR DOJO - COMBAT TRAINING ARENA
[Target Practice & VR Physics Playground]
Press H or Gamepad Start to Return to HUB"
font_size = 54
outline_size = 12

[node name="Target1" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, -4.37114e-08, -1, 0, 1, -4.37114e-08, -4, 2, -6)
mesh = SubResource("Mesh_Target")

[node name="Target2" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, -4.37114e-08, -1, 0, 1, -4.37114e-08, 4, 2, -6)
mesh = SubResource("Mesh_Target")

[node name="PCPlayer" parent="." instance=ExtResource("1_player")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 2)
"""

write_file(os.path.join(BASE_DIR, "scripts/artifacts/zemeckis_cube.gd"), ZEMECKIS_GD)
write_file(os.path.join(BASE_DIR, "scenes/artifacts/zemeckis_cube.tscn"), ZEMECKIS_TSCN)

write_file(os.path.join(BASE_DIR, "scripts/artifacts/holy_hand_grenade.gd"), GRENADE_GD)
write_file(os.path.join(BASE_DIR, "scenes/artifacts/holy_hand_grenade.tscn"), GRENADE_TSCN)

write_file(os.path.join(BASE_DIR, "scripts/characters/iron_giant_companion.gd"), GIANT_GD)
write_file(os.path.join(BASE_DIR, "scenes/characters/iron_giant_companion.tscn"), GIANT_TSCN)

write_file(os.path.join(BASE_DIR, "scenes/demos/scene_11_xr_dojo.tscn"), DOJO_TSCN)

print("RPO & Godot XR Dojo Artifacts, Iron Giant Mech, and Training Arena generated successfully!")
