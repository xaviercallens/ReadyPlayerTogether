import os
import math

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# LIGHTENED & SPATIALLY BALANCED HUB SCENE (oasis_hub.tscn)
# ==============================================================================
HUB_HEADER = """
[gd_scene load_steps=12 format=3 uid="uid://oasis_hub_cyberpunk"]

[ext_resource type="Script" path="res://scripts/hub/oasis_hub.gd" id="1_hub_script"]
[ext_resource type="PackedScene" uid="uid://pc_player_scene" path="res://scenes/player_vr/pc_player.tscn" id="2_player"]
[ext_resource type="PackedScene" uid="uid://parzival_npc_scene" path="res://scenes/characters/parzival_npc.tscn" id="3_parzival"]
[ext_resource type="PackedScene" uid="uid://art3mis_npc_scene" path="res://scenes/characters/art3mis_npc.tscn" id="4_art3mis"]
[ext_resource type="PackedScene" uid="uid://aech_npc_scene" path="res://scenes/characters/aech_npc.tscn" id="5_aech"]

[sub_resource type="Environment" id="Environment_cyberpunk"]
background_mode = 1
background_color = Color(0.04, 0.03, 0.08, 1)
glow_enabled = true
glow_intensity = 1.8
glow_bloom = 0.3
glow_blend_mode = 0
volumetric_fog_enabled = true
volumetric_fog_density = 0.006
volumetric_fog_albedo = Color(0.1, 0.6, 0.9, 1)
ssr_enabled = true

[sub_resource type="StandardMaterial3D" id="Mat_Floor"]
albedo_color = Color(0.08, 0.08, 0.12, 1)
metallic = 0.7
roughness = 0.25

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
light_color = Color(0.6, 0.85, 1.0, 1)
light_energy = 1.2
shadow_enabled = true

[node name="CentralPlatform" type="StaticBody3D" parent="."]

[node name="MeshInstance3D" type="MeshInstance3D" parent="CentralPlatform"]
mesh = SubResource("Mesh_Floor")

[node name="CollisionShape3D" type="CollisionShape3D" parent="CentralPlatform"]
shape = SubResource("Shape_Floor")

[node name="PCPlayer" parent="." instance=ExtResource("2_player")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.8, 0)

[node name="ParzivalNPC" parent="." instance=ExtResource("3_parzival")]
transform = Transform3D(0.7, 0, 0, 0, 0.7, 0, 0, 0, 0.7, 4.0, 0.2, -4.5)

[node name="Art3misNPC" parent="." instance=ExtResource("4_art3mis")]
transform = Transform3D(0.7, 0, 0, 0, 0.7, 0, 0, 0, 0.7, -4.0, 0.2, -4.5)

[node name="AechNPC" parent="." instance=ExtResource("5_aech")]
transform = Transform3D(0.7, 0, 0, 0, 0.7, 0, 0, 0, 0.7, 0.0, 0.2, -7.5)

[node name="HubTitle" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 5.5, -9)
billboard = 1
pixel_size = 0.018
text = "WELCOME TO THE OASIS
[Keys 1-9, 0] Teleport Instantly | [Gamepad / Mouse] Look"
font_size = 56
outline_size = 12

[node name="Portals" type="Node3D" parent="."]
"""

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
print("Hub lightened, characters scaled down (0.7x), and spatially distributed!")
