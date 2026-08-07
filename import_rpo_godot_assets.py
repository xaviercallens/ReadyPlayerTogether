import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# 1. DELOREAN TIME MACHINE SCENE (scenes/vehicles/delorean_car.tscn)
# ==============================================================================
DELOREAN_GD = """
extends CharacterBody3D

@export var speed: float = 0.0
var time_passed: float = 0.0

func _process(delta: float) -> void:
	time_passed += delta
	# Flux Capacitor pulse animation
	$FluxCapacitor.light_energy = 2.0 + sin(time_passed * 10.0) * 1.5
	$RearThruster.light_energy = 3.0 + sin(time_passed * 8.0) * 1.0
"""

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
"""

write_file(os.path.join(BASE_DIR, "scripts/vehicles/delorean_car.gd"), DELOREAN_GD)
write_file(os.path.join(BASE_DIR, "scenes/vehicles/delorean_car.tscn"), DELOREAN_TSCN)

# ==============================================================================
# 2. RPO MANNEQUIN MALE SCENE (scenes/characters/rpo_mannequin_male.tscn)
# ==============================================================================
MANNEQUIN_TSCN = """
[gd_scene load_steps=6 format=3 uid="uid://rpo_mannequin_male_scene"]

[sub_resource type="StandardMaterial3D" id="Mat_Mannequin"]
albedo_color = Color(0.85, 0.88, 0.92, 1)
metallic = 0.4
roughness = 0.2

[sub_resource type="CapsuleMesh" id="Mesh_Torso"]
material = SubResource("Mat_Mannequin")
radius = 0.35
height = 1.0

[sub_resource type="SphereMesh" id="Mesh_Head"]
material = SubResource("Mat_Mannequin")
radius = 0.22
height = 0.44

[sub_resource type="CylinderMesh" id="Mesh_Limb"]
material = SubResource("Mat_Mannequin")
top_radius = 0.09
bottom_radius = 0.07
height = 0.85

[node name="RPOMannequinMale" type="Node3D"]

[node name="Torso" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.1, 0)
mesh = SubResource("Mesh_Torso")

[node name="Head" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.72, 0)
mesh = SubResource("Mesh_Head")

[node name="LeftLeg" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.16, 0.42, 0)
mesh = SubResource("Mesh_Limb")

[node name="RightLeg" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.16, 0.42, 0)
mesh = SubResource("Mesh_Limb")

[node name="Label3D" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.1, 0)
billboard = 1
pixel_size = 0.015
text = "RPO MANNEQUIN AVATAR"
font_size = 32
outline_size = 6
"""

write_file(os.path.join(BASE_DIR, "scenes/characters/rpo_mannequin_male.tscn"), MANNEQUIN_TSCN)

# ==============================================================================
# 3. ENHANCE COPPER RACE DEMO WITH DELOREAN (scene_03_copper_race.tscn)
# ==============================================================================
COPPER_RACE_TSCN = """
[gd_scene load_steps=7 format=3 uid="uid://demo_03_copper_race"]

[ext_resource type="PackedScene" uid="uid://pc_player_scene" path="res://scenes/player_vr/pc_player.tscn" id="1_player"]
[ext_resource type="Script" path="res://scripts/demos/demo_return.gd" id="2_return_script"]
[ext_resource type="PackedScene" uid="uid://delorean_car_scene" path="res://scenes/vehicles/delorean_car.tscn" id="3_delorean"]

[sub_resource type="Environment" id="Environment_race"]
background_mode = 1
background_color = Color(0.05, 0.05, 0.25, 1)
glow_enabled = true
glow_intensity = 2.5
glow_bloom = 0.6
glow_blend_mode = 0
volumetric_fog_enabled = true
volumetric_fog_density = 0.015
volumetric_fog_albedo = Color(0.0, 1.0, 0.9, 1)
ssr_enabled = true

[sub_resource type="StandardMaterial3D" id="Mat_Asphalt"]
albedo_color = Color(0.08, 0.08, 0.12, 1)
metallic = 0.8
roughness = 0.2

[sub_resource type="PlaneMesh" id="Plane_Track"]
material = SubResource("Mat_Asphalt")
size = Vector2(40, 200)

[node name="CopperRaceNewYork" type="Node3D"]
script = ExtResource("2_return_script")

[node name="WorldEnvironment" type="WorldEnvironment" parent="."]
environment = SubResource("Environment_race")

[node name="DirectionalLight3D" type="DirectionalLight3D" parent="."]
transform = Transform3D(0.866025, -0.353553, 0.353553, 0, 0.707107, 0.707107, -0.5, -0.612372, 0.612372, 0, 15, 0)
light_color = Color(0.2, 0.9, 1.0, 1)
shadow_enabled = true

[node name="Track" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, -80)
mesh = SubResource("Plane_Track")

[node name="DeLoreanTimeMachine" parent="." instance=ExtResource("3_delorean")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, -8)

[node name="Label3D" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4.0, -12)
billboard = 1
pixel_size = 0.02
text = "THE COPPER KEY RACE - NEW YORK TRACK
[Featuring Parzival's DeLorean Time Machine]
Press H or Gamepad Start to Return to HUB"
font_size = 54
outline_size = 12

[node name="PCPlayer" parent="." instance=ExtResource("1_player")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 2)
"""

write_file(os.path.join(BASE_DIR, "scenes/demos/scene_03_copper_race.tscn"), COPPER_RACE_TSCN)

print("Imported RPO Godot assets (DeLorean, Mannequin, Track) integrated successfully!")
