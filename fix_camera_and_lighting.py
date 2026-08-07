import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# 1. FIX PC_PLAYER CAMERA & MANNEQUIN MESH (scenes/player_vr/pc_player.tscn)
# ==============================================================================
# Offset Camera forward to prevent mesh interior clipping (near = 0.05)
PC_PLAYER_TSCN = """
[gd_scene load_steps=11 format=3 uid="uid://pc_player_scene"]

[ext_resource type="Script" path="res://scripts/player_vr/pc_player.gd" id="1_pc_script"]
[ext_resource type="PackedScene" uid="uid://scene_navigator_ui" path="res://scenes/ui/scene_navigator.tscn" id="2_navigator"]
[ext_resource type="PackedScene" uid="uid://command_menu_ui" path="res://scenes/ui/command_menu.tscn" id="3_command_menu"]

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
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.7, -0.3)
current = true
near = 0.05

[node name="SceneNavigator" parent="." instance=ExtResource("2_navigator")]

[node name="CommandMenu" parent="." instance=ExtResource("3_command_menu")]
"""

write_file(os.path.join(BASE_DIR, "scenes/player_vr/pc_player.tscn"), PC_PLAYER_TSCN)

# ==============================================================================
# 2. ENHANCE ENVIRONMENT & AMBIENT LIGHTING IN HUB (scenes/hub/oasis_hub.tscn)
# ==============================================================================
HUB_HEADER = """
[gd_scene load_steps=16 format=3 uid="uid://oasis_hub_cyberpunk"]

[ext_resource type="Script" path="res://scripts/hub/oasis_hub.gd" id="1_hub_script"]
[ext_resource type="PackedScene" uid="uid://pc_player_scene" path="res://scenes/player_vr/pc_player.tscn" id="2_player"]
[ext_resource type="PackedScene" uid="uid://parzival_npc_scene" path="res://scenes/characters/parzival_npc.tscn" id="3_parzival"]
[ext_resource type="PackedScene" uid="uid://art3mis_npc_scene" path="res://scenes/characters/art3mis_npc.tscn" id="4_art3mis"]
[ext_resource type="PackedScene" uid="uid://aech_npc_scene" path="res://scenes/characters/aech_npc.tscn" id="5_aech"]
[ext_resource type="PackedScene" uid="uid://zemeckis_cube_scene" path="res://scenes/artifacts/zemeckis_cube.tscn" id="6_zemeckis"]
[ext_resource type="PackedScene" uid="uid://holy_hand_grenade_scene" path="res://scenes/artifacts/holy_hand_grenade.tscn" id="7_grenade"]
[ext_resource type="PackedScene" uid="uid://iron_giant_companion_scene" path="res://scenes/characters/iron_giant_companion.tscn" id="8_giant"]
[ext_resource type="PackedScene" uid="uid://delorean_car_scene" path="res://scenes/vehicles/delorean_car.tscn" id="9_delorean"]

[sub_resource type="Environment" id="Environment_cyberpunk"]
background_mode = 1
background_color = Color(0.08, 0.06, 0.15, 1)
ambient_light_source = 2
ambient_light_color = Color(0.4, 0.45, 0.6, 1)
ambient_light_energy = 1.5
glow_enabled = true
glow_intensity = 1.5
glow_bloom = 0.2
glow_blend_mode = 0
volumetric_fog_enabled = false
ssr_enabled = true

[sub_resource type="StandardMaterial3D" id="Mat_Floor"]
albedo_color = Color(0.12, 0.12, 0.18, 1)
metallic = 0.6
roughness = 0.3

[sub_resource type="CylinderMesh" id="Mesh_Floor"]
material = SubResource("Mat_Floor")
top_radius = 18.0
bottom_radius = 18.0
height = 0.4

[sub_resource type="StandardMaterial3D" id="Mat_Portal"]
albedo_color = Color(0.0, 0.9, 0.8, 1)
emission_enabled = true
emission = Color(0.0, 0.9, 0.8, 1)
emission_energy_multiplier = 3.0

[sub_resource type="TorusMesh" id="Mesh_Portal"]
material = SubResource("Mat_Portal")
inner_radius = 1.6
outer_radius = 2.0

[sub_resource type="CylinderShape3D" id="Shape_Portal"]
height = 3.0
radius = 2.0

[sub_resource type="BoxShape3D" id="Shape_Floor"]
size = Vector3(36, 0.4, 36)

[node name="OasisHub" type="Node3D"]
script = ExtResource("1_hub_script")

[node name="WorldEnvironment" type="WorldEnvironment" parent="."]
environment = SubResource("Environment_cyberpunk")

[node name="DirectionalLight3D" type="DirectionalLight3D" parent="."]
transform = Transform3D(0.866025, -0.353553, 0.353553, 0, 0.707107, 0.707107, -0.5, -0.612372, 0.612372, 0, 15, 0)
light_color = Color(0.8, 0.9, 1.0, 1)
light_energy = 2.0
shadow_enabled = true

[node name="CentralPlatform" type="StaticBody3D" parent="."]

[node name="MeshInstance3D" type="MeshInstance3D" parent="CentralPlatform"]
mesh = SubResource("Mesh_Floor")

[node name="CollisionShape3D" type="CollisionShape3D" parent="CentralPlatform"]
shape = SubResource("Shape_Floor")

# Playable Player Spawn
[node name="PCPlayer" parent="." instance=ExtResource("2_player")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.8, 4.0)

# Central DeLorean Time Machine
[node name="CentralDeLorean" parent="." instance=ExtResource("9_delorean")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.2, -1.0)

[node name="ParzivalNPC" parent="." instance=ExtResource("3_parzival")]
transform = Transform3D(0.7, 0, 0, 0, 0.7, 0, 0, 0, 0.7, 4.5, 0.2, -4.5)

[node name="Art3misNPC" parent="." instance=ExtResource("4_art3mis")]
transform = Transform3D(0.7, 0, 0, 0, 0.7, 0, 0, 0, 0.7, -4.5, 0.2, -4.5)

[node name="AechNPC" parent="." instance=ExtResource("5_aech")]
transform = Transform3D(0.7, 0, 0, 0, 0.7, 0, 0, 0, 0.7, 0.0, 0.2, -7.5)

[node name="ZemeckisCube" parent="." instance=ExtResource("6_zemeckis")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 2.5, 0.2, -2.5)

[node name="HolyHandGrenade" parent="." instance=ExtResource("7_grenade")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -2.5, 0.2, -2.5)

[node name="IronGiantCompanion" parent="." instance=ExtResource("8_giant")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -8.0, 0.0, -10.0)

[node name="HubTitle" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 6.0, -10)
billboard = 1
pixel_size = 0.018
text = "WELCOME TO THE OASIS
[Keys 1-9, 0] Teleport Demos | [Shift+F] Search | [Tab] Command Menu"
font_size = 56
outline_size = 12

[node name="Portals" type="Node3D" parent="."]
"""

import math

portal_names = [
	"01: The Stacks [1]", "02: Halliday's Journal [2]", "03: Copper Race [3]",
	"04: Distracted Globe [4]", "05: Retro Arcade [5]", "06: Planet Doom [6]",
	"07: Overlook Hotel [7]", "08: IOI Citadel [8]", "09: Crystal Castle [9]", "10: Easter Egg [0]"
]

portals_tscn = ""
for i in range(1, 11):
	angle = (i - 1) * (2 * math.pi / 10)
	radius = 13.0
	x = math.cos(angle) * radius
	z = math.sin(angle) * radius
	rot_y = -angle + math.pi/2
	
	portals_tscn += f"""
[node name="Portal_{i:02d}" type="Area3D" parent="Portals"]
transform = Transform3D({math.cos(rot_y):.4f}, 0, {math.sin(rot_y):.4f}, 0, 1, 0, {-math.sin(rot_y):.4f}, 0, {math.cos(rot_y):.4f}, {x:.2f}, 1.8, {z:.2f})

[node name="MeshInstance3D" type="MeshInstance3D" parent="Portals/Portal_{i:02d}"]
transform = Transform3D(1, 0, 0, 0, -4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 0, 0)
mesh = SubResource("Mesh_Portal")

[node name="CollisionShape3D" type="CollisionShape3D" parent="Portals/Portal_{i:02d}"]
shape = SubResource("Shape_Portal")

[node name="Label3D" type="Label3D" parent="Portals/Portal_{i:02d}"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.3, 0)
billboard = 1
pixel_size = 0.014
text = "{portal_names[i-1]}"
font_size = 42
outline_size = 8
"""

write_file(os.path.join(BASE_DIR, "scenes/hub/oasis_hub.tscn"), HUB_HEADER + portals_tscn)

print("Camera offset and ambient lighting enhanced for immediate visibility!")
