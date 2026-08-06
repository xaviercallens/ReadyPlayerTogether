import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# 1. CYBERPUNK HOVERBOARD ARTIFACT (scenes/artifacts/hoverboard.tscn)
# ==============================================================================
HOVERBOARD_GD = """
extends Area3D

@export var levitation_speed: float = 3.0
var time_passed: float = 0.0

func _process(delta: float) -> void:
	time_passed += delta
	rotation.y += delta * levitation_speed
	position.y = 1.0 + sin(time_passed * 4.0) * 0.12
	$ThrusterLight.light_energy = 3.0 + sin(time_passed * 10.0) * 1.5

func _on_body_entered(body: Node3D) -> void:
	if body.is_in_group("player"):
		print("[ARTIFACT] Cyberpunk Hoverboard Equipped! Anti-Gravity Flight Active!")
"""

HOVERBOARD_TSCN = """
[gd_scene load_steps=7 format=3 uid="uid://hoverboard_artifact_scene"]

[ext_resource type="Script" path="res://scripts/artifacts/hoverboard.gd" id="1_script"]

[sub_resource type="StandardMaterial3D" id="Mat_CarbonFiber"]
albedo_color = Color(0.1, 0.12, 0.18, 1)
metallic = 0.95
roughness = 0.1

[sub_resource type="BoxMesh" id="Mesh_Board"]
material = SubResource("Mat_CarbonFiber")
size = Vector3(0.6, 0.08, 1.8)

[sub_resource type="StandardMaterial3D" id="Mat_NeonMagenta"]
albedo_color = Color(1.0, 0.0, 0.8, 1)
emission_enabled = true
emission = Color(1.0, 0.0, 0.8, 1)
emission_energy_multiplier = 5.0

[sub_resource type="BoxMesh" id="Mesh_Thruster"]
material = SubResource("Mat_NeonMagenta")
size = Vector3(0.5, 0.05, 0.3)

[sub_resource type="SphereShape3D" id="Shape_Interact"]
radius = 1.5

[node name="CyberpunkHoverboard" type="Area3D"]
script = ExtResource("1_script")

[node name="BoardMesh" type="MeshInstance3D" parent="."]
mesh = SubResource("Mesh_Board")

[node name="ThrusterMesh" type="MeshInstance3D" parent="BoardMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, -0.05, 0.7)
mesh = SubResource("Mesh_Thruster")

[node name="ThrusterLight" type="OmniLight3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, -0.2, 0.7)
light_color = Color(1.0, 0.0, 0.8, 1)
light_energy = 4.0

[node name="Label3D" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.6, 0)
billboard = 1
pixel_size = 0.012
text = "ARTIFACT: Cyberpunk Hoverboard"
font_size = 32
outline_size = 6

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
shape = SubResource("Shape_Interact")
"""

write_file(os.path.join(BASE_DIR, "scripts/artifacts/hoverboard.gd"), HOVERBOARD_GD)
write_file(os.path.join(BASE_DIR, "scenes/artifacts/hoverboard.tscn"), HOVERBOARD_TSCN)

# ==============================================================================
# 2. ORB OF OSUVOX ARTIFACT (scenes/artifacts/orb_osuvox.tscn)
# ==============================================================================
OSUVOX_GD = """
extends Area3D

var time_passed: float = 0.0

func _process(delta: float) -> void:
	time_passed += delta
	rotation.y += delta * 2.0
	position.y = 1.2 + sin(time_passed * 3.0) * 0.1
	$ShieldMesh.scale = Vector3.ONE * (1.0 + sin(time_passed * 5.0) * 0.05)
"""

OSUVOX_TSCN = """
[gd_scene load_steps=7 format=3 uid="uid://orb_osuvox_artifact_scene"]

[ext_resource type="Script" path="res://scripts/artifacts/orb_osuvox.gd" id="1_script"]

[sub_resource type="StandardMaterial3D" id="Mat_OrbCore"]
albedo_color = Color(0.9, 0.1, 0.2, 1)
metallic = 0.9
emission_enabled = true
emission = Color(0.9, 0.1, 0.2, 1)
emission_energy_multiplier = 4.0

[sub_resource type="SphereMesh" id="Mesh_Core"]
material = SubResource("Mat_OrbCore")
radius = 0.25
height = 0.5

[sub_resource type="StandardMaterial3D" id="Mat_Forcefield"]
transparency = 1
albedo_color = Color(0.9, 0.2, 0.4, 0.4)
metallic = 0.8
roughness = 0.1

[sub_resource type="SphereMesh" id="Mesh_Shield"]
material = SubResource("Mat_Forcefield")
radius = 0.45
height = 0.9

[sub_resource type="SphereShape3D" id="Shape_Interact"]
radius = 1.5

[node name="OrbOfOsuvox" type="Area3D"]
script = ExtResource("1_script")

[node name="CoreMesh" type="MeshInstance3D" parent="."]
mesh = SubResource("Mesh_Core")

[node name="ShieldMesh" type="MeshInstance3D" parent="."]
mesh = SubResource("Mesh_Shield")

[node name="Label3D" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.7, 0)
billboard = 1
pixel_size = 0.012
text = "ARTIFACT: Orb of Osuvox Forcefield"
font_size = 32
outline_size = 6

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
shape = SubResource("Shape_Interact")
"""

write_file(os.path.join(BASE_DIR, "scripts/artifacts/orb_osuvox.gd"), OSUVOX_GD)
write_file(os.path.join(BASE_DIR, "scenes/artifacts/orb_osuvox.tscn"), OSUVOX_TSCN)

# ==============================================================================
# 3. GUNDAM RX-78 BATTLE MECH AVATAR (scenes/characters/gundam_mech.tscn)
# ==============================================================================
GUNDAM_GD = """
extends CharacterBody3D

var time_passed: float = 0.0

func _process(delta: float) -> void:
	time_passed += delta
	# Gundam eye reactor pulse
	$EyeLight.light_energy = 4.0 + sin(time_passed * 6.0) * 1.5
"""

GUNDAM_TSCN = """
[gd_scene load_steps=8 format=3 uid="uid://gundam_mech_scene"]

[ext_resource type="Script" path="res://scripts/characters/gundam_mech.gd" id="1_script"]

[sub_resource type="StandardMaterial3D" id="Mat_GundamWhite"]
albedo_color = Color(0.9, 0.92, 0.96, 1)
metallic = 0.8
roughness = 0.2

[sub_resource type="StandardMaterial3D" id="Mat_GundamBlue"]
albedo_color = Color(0.1, 0.3, 0.8, 1)
metallic = 0.8
roughness = 0.2

[sub_resource type="StandardMaterial3D" id="Mat_EyesYellow"]
albedo_color = Color(1.0, 0.9, 0.1, 1)
emission_enabled = true
emission = Color(1.0, 0.9, 0.1, 1)
emission_energy_multiplier = 5.0

[sub_resource type="BoxMesh" id="Mesh_Chest"]
material = SubResource("Mat_GundamBlue")
size = Vector3(2.2, 2.8, 1.6)

[sub_resource type="BoxMesh" id="Mesh_Head"]
material = SubResource("Mat_GundamWhite")
size = Vector3(1.2, 1.2, 1.2)

[sub_resource type="BoxMesh" id="Mesh_Eyes"]
material = SubResource("Mat_EyesYellow")
size = Vector3(0.9, 0.25, 0.2)

[node name="GundamRX78Mech" type="CharacterBody3D"]
script = ExtResource("1_script")

[node name="Chest" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3.0, 0)
mesh = SubResource("Mesh_Chest")

[node name="Head" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 5.0, 0)
mesh = SubResource("Mesh_Head")

[node name="Eyes" type="MeshInstance3D" parent="Head"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.1, -0.62)
mesh = SubResource("Mesh_Eyes")

[node name="EyeLight" type="OmniLight3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 5.1, -0.8)
light_color = Color(1.0, 0.9, 0.1, 1)
light_energy = 4.0

[node name="Label3D" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 6.5, 0)
billboard = 1
pixel_size = 0.02
text = "GUNDAM RX-78-2 BATTLE MECH AVATAR
'Ready Player One Climax Battle Mech!'"
font_size = 48
outline_size = 12
"""

write_file(os.path.join(BASE_DIR, "scripts/characters/gundam_mech.gd"), GUNDAM_GD)
write_file(os.path.join(BASE_DIR, "scenes/characters/gundam_mech.tscn"), GUNDAM_TSCN)

print("Better ML Characters & Artifacts (Hoverboard, Orb of Osuvox, Gundam Mech) generated successfully!")
