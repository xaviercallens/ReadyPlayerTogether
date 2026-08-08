import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# MASTER READY PLAYER ONE MOVIE SPIRIT HUB SCENE (scenes/hub/oasis_master_rpo_movie.tscn)
# Clean .tscn template without inline # comment lines to guarantee 100% node parsing
# ==============================================================================
MASTER_HUB_TSCN = """[gd_scene load_steps=20 format=3 uid="uid://master_rpo_movie_hub"]

[ext_resource type="PackedScene" uid="uid://pc_player_scene" path="res://scenes/player_vr/pc_player.tscn" id="1_player"]
[ext_resource type="PackedScene" uid="uid://delorean_car_scene" path="res://scenes/vehicles/delorean_car.tscn" id="2_delorean"]
[ext_resource type="PackedScene" path="res://assets/oasis_batch/3d_iron_giant_assignment.glb" id="3_iron_giant"]
[ext_resource type="PackedScene" path="res://assets/oasis_batch/transformers_bumblebee.glb" id="4_bumblebee"]
[ext_resource type="PackedScene" path="res://assets/oasis_batch/free_cyberpunk_hovercar.glb" id="5_hovercar"]
[ext_resource type="PackedScene" path="res://assets/oasis_batch/GodotRobot3rdPersonShooterFinal.glb" id="6_godot_robot"]
[ext_resource type="PackedScene" uid="uid://hoverboard_artifact_scene" path="res://scenes/artifacts/hoverboard.tscn" id="7_hoverboard"]
[ext_resource type="PackedScene" uid="uid://orb_osuvox_artifact_scene" path="res://scenes/artifacts/orb_osuvox.tscn" id="8_osuvox"]
[ext_resource type="PackedScene" uid="uid://zemeckis_cube_scene" path="res://scenes/artifacts/zemeckis_cube.tscn" id="9_zemeckis"]
[ext_resource type="PackedScene" uid="uid://holy_hand_grenade_scene" path="res://scenes/artifacts/holy_hand_grenade.tscn" id="10_grenade"]
[ext_resource type="PackedScene" uid="uid://virtual_portal_screen_scene" path="res://scenes/ui/virtual_portal_screen.tscn" id="11_portal"]

[sub_resource type="ProceduralSkyMaterial" id="Sky_RPO"]
sky_top_color = Color(0.05, 0.15, 0.35, 1)
sky_horizon_color = Color(0.2, 0.7, 1.0, 1)
ground_bottom_color = Color(0.05, 0.15, 0.35, 1)
ground_horizon_color = Color(0.2, 0.7, 1.0, 1)

[sub_resource type="Sky" id="Sky_Mesh"]
sky_material = SubResource("Sky_RPO")

[sub_resource type="Environment" id="Env_RPO"]
background_mode = 2
sky = SubResource("Sky_Mesh")
ambient_light_color = Color(0.3, 0.75, 1.0, 1)
ambient_light_energy = 1.5
glow_enabled = true
glow_intensity = 1.2
glow_bloom = 0.2
glow_blend_mode = 0
fog_enabled = false
volumetric_fog_enabled = false
ssr_enabled = true
ssao_enabled = true

[sub_resource type="StandardMaterial3D" id="Mat_PlazaFloor"]
albedo_color = Color(0.08, 0.1, 0.15, 1)
metallic = 0.95
roughness = 0.15

[sub_resource type="CylinderMesh" id="Mesh_Plaza"]
material = SubResource("Mat_PlazaFloor")
top_radius = 50.0
bottom_radius = 50.0
height = 0.6

[sub_resource type="CylinderShape3D" id="Shape_PlazaFloor"]
height = 1.0
radius = 50.0

[sub_resource type="StandardMaterial3D" id="Mat_NeonRing"]
albedo_color = Color(0.0, 0.9, 1.0, 1)
emission_enabled = true
emission = Color(0.0, 0.9, 1.0, 1)
emission_energy_multiplier = 4.0

[sub_resource type="TorusMesh" id="Mesh_Ring"]
material = SubResource("Mat_NeonRing")
inner_radius = 48.5
outer_radius = 49.5

[node name="OasisMasterRPOMovieHub" type="Node3D"]

[node name="WorldEnvironment" type="WorldEnvironment" parent="."]
environment = SubResource("Env_RPO")

[node name="SunLight" type="DirectionalLight3D" parent="."]
transform = Transform3D(0.866025, -0.353553, 0.353553, 0, 0.707107, 0.707107, -0.5, -0.612372, 0.612372, 0, 25, 0)
light_color = Color(0.0, 0.9, 1.0, 1)
light_energy = 1.8
shadow_enabled = true

[node name="GroundPlaza" type="StaticBody3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, -0.3, 0)

[node name="PlazaCollision" type="CollisionShape3D" parent="GroundPlaza"]
shape = SubResource("Shape_PlazaFloor")

[node name="PlazaFloorMesh" type="MeshInstance3D" parent="GroundPlaza"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.2, 0)
mesh = SubResource("Mesh_Plaza")

[node name="NeonRing" type="MeshInstance3D" parent="GroundPlaza"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.52, 0)
mesh = SubResource("Mesh_Ring")

[node name="SafetyGroundBox" type="CSGBox3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, -1.0, 0)
use_collision = true
size = Vector3(150, 1, 150)

[node name="PCPlayer" parent="." instance=ExtResource("1_player")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.5, 10)

[node name="DeLoreanTimeMachine" parent="." instance=ExtResource("2_delorean")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.2, -1.0)

[node name="IronGiantTitan" parent="." instance=ExtResource("3_iron_giant")]
transform = Transform3D(4.33, 0, -2.5, 0, 5.0, 0, 2.5, 0, 4.33, -14, 0.2, -8)

[node name="BumblebeeTitan" parent="." instance=ExtResource("4_bumblebee")]
transform = Transform3D(4.33, 0, 2.5, 0, 5.0, 0, -2.5, 0, 4.33, 14, 0.2, -8)

[node name="CyberpunkHovercar" parent="." instance=ExtResource("5_hovercar")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3.5, -8)

[node name="GodotRobotShooter" parent="." instance=ExtResource("6_godot_robot")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -9, 0.2, 2)

[node name="IronGiantLabel" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -14, 18.0, -8)
billboard = 1
pixel_size = 0.018
text = "IRON GIANT (Titan Colossus x50)
'I Am Not A Gun!'"
font_size = 48
outline_size = 12

[node name="BumblebeeLabel" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 14, 18.0, -8)
billboard = 1
pixel_size = 0.018
text = "TRANSFORMERS BUMBLEBEE (Titan Mech x50)"
font_size = 48
outline_size = 12

[node name="HovercarLabel" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 5.2, -8)
billboard = 1
pixel_size = 0.015
text = "CYBERPUNK HOVERCAR (Sky Vehicle)"
font_size = 36
outline_size = 8

[node name="GodotRobotLabel" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -9, 2.5, 2)
billboard = 1
pixel_size = 0.015
text = "GODOT 4 BATTLE ROBOT"
font_size = 36
outline_size = 8

[node name="CyberpunkHoverboard" parent="." instance=ExtResource("7_hoverboard")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -4.5, 0.2, 2.0)

[node name="OrbOfOsuvox" parent="." instance=ExtResource("8_osuvox")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 4.5, 0.2, 2.0)

[node name="ZemeckisCube" parent="." instance=ExtResource("9_zemeckis")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -7.0, 1.2, 0.0)

[node name="HolyHandGrenade" parent="." instance=ExtResource("10_grenade")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 7.0, 1.2, 0.0)

[node name="VirtualPortalScreen" parent="." instance=ExtResource("11_portal")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.2, -18.0)

[node name="MasterTitle" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 7.5, -12)
billboard = 1
pixel_size = 0.02
text = "WELCOME TO THE OASIS - READY PLAYER ONE MOVIE EXPERIENCE
[Press F: Spawn DeLorean | Press Ctrl+A: AI Generator | Press I: Inventory | Press Shift+F: Teleport]"
font_size = 52
outline_size = 12
"""

write_file(os.path.join(BASE_DIR, "scenes/hub/oasis_master_rpo_movie.tscn"), MASTER_HUB_TSCN)

print("Master Ready Player One Movie Spirit Hub Scene updated cleanly!")
