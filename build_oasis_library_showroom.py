import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# CLEANED LIBRARY SHOWROOM SCENE (scene_12_library_showroom.tscn)
# ==============================================================================
SHOWROOM_TSCN = """
[gd_scene load_steps=18 format=3 uid="uid://demo_12_library_showroom"]

[ext_resource type="PackedScene" uid="uid://pc_player_scene" path="res://scenes/player_vr/pc_player.tscn" id="1_player"]
[ext_resource type="Script" path="res://scripts/demos/demo_return.gd" id="2_return_script"]

[sub_resource type="Environment" id="Environment_showroom"]
background_mode = 1
background_color = Color(0.03, 0.02, 0.06, 1)
glow_enabled = true
glow_intensity = 2.0
glow_bloom = 0.5
glow_blend_mode = 0
volumetric_fog_enabled = true
volumetric_fog_density = 0.005
volumetric_fog_albedo = Color(0.2, 0.7, 1.0, 1)
ssr_enabled = true

[sub_resource type="StandardMaterial3D" id="Mat_ShowroomFloor"]
albedo_color = Color(0.06, 0.06, 0.1, 1)
metallic = 0.85
roughness = 0.15

[sub_resource type="PlaneMesh" id="Plane_Showroom"]
material = SubResource("Mat_ShowroomFloor")
size = Vector2(60, 60)

[sub_resource type="StandardMaterial3D" id="Mat_Pedestal"]
albedo_color = Color(0.12, 0.15, 0.22, 1)
metallic = 0.6
roughness = 0.3

[sub_resource type="CylinderMesh" id="Mesh_Pedestal"]
material = SubResource("Mat_Pedestal")
top_radius = 0.8
bottom_radius = 1.0
height = 0.8

[sub_resource type="StandardMaterial3D" id="Mat_CopperKey"]
albedo_color = Color(1.0, 0.6, 0.1, 1)
metallic = 0.9
emission_enabled = true
emission = Color(1.0, 0.6, 0.1, 1)
emission_energy_multiplier = 3.0

[sub_resource type="BoxMesh" id="Mesh_CopperKey"]
material = SubResource("Mat_CopperKey")
size = Vector3(0.35, 0.35, 0.35)

[sub_resource type="StandardMaterial3D" id="Mat_JadeKey"]
albedo_color = Color(0.1, 0.9, 0.4, 1)
metallic = 0.8
emission_enabled = true
emission = Color(0.1, 0.9, 0.4, 1)
emission_energy_multiplier = 3.0

[sub_resource type="BoxMesh" id="Mesh_JadeKey"]
material = SubResource("Mat_JadeKey")
size = Vector3(0.35, 0.35, 0.35)

[sub_resource type="StandardMaterial3D" id="Mat_CrystalKey"]
albedo_color = Color(0.8, 0.9, 1.0, 1)
metallic = 0.9
emission_enabled = true
emission = Color(0.8, 0.9, 1.0, 1)
emission_energy_multiplier = 4.0

[sub_resource type="SphereMesh" id="Mesh_CrystalKey"]
material = SubResource("Mat_CrystalKey")
radius = 0.22
height = 0.44

[sub_resource type="StandardMaterial3D" id="Mat_Zemeckis"]
albedo_color = Color(0.0, 0.8, 1.0, 1)
metallic = 0.8
emission_enabled = true
emission = Color(0.0, 0.8, 1.0, 1)
emission_energy_multiplier = 3.0

[sub_resource type="BoxMesh" id="Mesh_Zemeckis"]
material = SubResource("Mat_Zemeckis")
size = Vector3(0.4, 0.4, 0.4)

[sub_resource type="StandardMaterial3D" id="Mat_Grenade"]
albedo_color = Color(1.0, 0.85, 0.1, 1)
metallic = 0.9
emission_enabled = true
emission = Color(1.0, 0.85, 0.1, 1)
emission_energy_multiplier = 3.0

[sub_resource type="SphereMesh" id="Mesh_Grenade"]
material = SubResource("Mat_Grenade")
radius = 0.22
height = 0.44

[node name="OasisLibraryShowroom" type="Node3D"]
script = ExtResource("2_return_script")

[node name="WorldEnvironment" type="WorldEnvironment" parent="."]
environment = SubResource("Environment_showroom")

[node name="DirectionalLight3D" type="DirectionalLight3D" parent="."]
transform = Transform3D(0.866025, -0.353553, 0.353553, 0, 0.707107, 0.707107, -0.5, -0.612372, 0.612372, 0, 12, 0)
light_color = Color(0.5, 0.8, 1.0, 1)
shadow_enabled = true

[node name="Floor" type="MeshInstance3D" parent="."]
mesh = SubResource("Plane_Showroom")

[node name="PCPlayer" parent="." instance=ExtResource("1_player")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 2)

[node name="ShowroomTitle" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 5.0, -10)
billboard = 1
pixel_size = 0.02
text = "THE OASIS ARTIFACT & AVATAR LIBRARY SHOWROOM
[Press L from anywhere to Open | Press H to Return to HUB]"
font_size = 56
outline_size = 12

# Pedestal 1: Copper Key
[node name="Pedestal_01" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -8, 0.4, -6)
mesh = SubResource("Mesh_Pedestal")

[node name="Item_CopperKey" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -8, 1.2, -6)
mesh = SubResource("Mesh_CopperKey")

[node name="Label_01" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -8, 1.8, -6)
billboard = 1
pixel_size = 0.012
text = "1. THE COPPER KEY
'Three Hidden Keys open Three Secret Gates'"
font_size = 32
outline_size = 6

# Pedestal 2: Jade Key
[node name="Pedestal_02" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -4, 0.4, -6)
mesh = SubResource("Mesh_Pedestal")

[node name="Item_JadeKey" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -4, 1.2, -6)
mesh = SubResource("Mesh_JadeKey")

[node name="Label_02" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -4, 1.8, -6)
billboard = 1
pixel_size = 0.012
text = "2. THE JADE KEY
'A Whistle & A Maze of Emeralds'"
font_size = 32
outline_size = 6

# Pedestal 3: Crystal Key
[node name="Pedestal_03" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.4, -6)
mesh = SubResource("Mesh_Pedestal")

[node name="Item_CrystalKey" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.2, -6)
mesh = SubResource("Mesh_CrystalKey")

[node name="Label_03" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.8, -6)
billboard = 1
pixel_size = 0.012
text = "3. THE CRYSTAL KEY
'Charity, Faith, and Hope'"
font_size = 32
outline_size = 6

# Pedestal 4: Zemeckis Cube
[node name="Pedestal_04" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 4, 0.4, -6)
mesh = SubResource("Mesh_Pedestal")

[node name="Item_Zemeckis" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 4, 1.2, -6)
mesh = SubResource("Mesh_Zemeckis")

[node name="Label_04" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 4, 1.8, -6)
billboard = 1
pixel_size = 0.012
text = "4. ZEMECKIS CUBE
'Reverses Time 60 Seconds'"
font_size = 32
outline_size = 6

# Pedestal 5: Holy Hand Grenade
[node name="Pedestal_05" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 8, 0.4, -6)
mesh = SubResource("Mesh_Pedestal")

[node name="Item_Grenade" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 8, 1.2, -6)
mesh = SubResource("Mesh_Grenade")

[node name="Label_05" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 8, 1.8, -6)
billboard = 1
pixel_size = 0.012
text = "5. HOLY HAND GRENADE
'Consult the Book of Armaments'"
font_size = 32
outline_size = 6
"""

write_file(os.path.join(BASE_DIR, "scenes/demos/scene_12_library_showroom.tscn"), SHOWROOM_TSCN)
print("Cleaned scene_12_library_showroom.tscn generated!")
