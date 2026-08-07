import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# 1. HIGH DETAIL DELOREAN TIME MACHINE (scenes/vehicles/delorean_car.tscn)
# ==============================================================================
DELOREAN_TSCN = """
[gd_scene load_steps=18 format=3 uid="uid://delorean_car_scene"]

[ext_resource type="Script" path="res://scripts/vehicles/delorean_car.gd" id="1_script"]

[sub_resource type="StandardMaterial3D" id="Mat_StainlessSteel"]
albedo_color = Color(0.75, 0.78, 0.82, 1)
metallic = 0.95
roughness = 0.15

[sub_resource type="StandardMaterial3D" id="Mat_DarkChassis"]
albedo_color = Color(0.12, 0.12, 0.15, 1)
metallic = 0.8
roughness = 0.3

[sub_resource type="StandardMaterial3D" id="Mat_Glass"]
albedo_color = Color(0.05, 0.1, 0.18, 0.85)
metallic = 0.9
roughness = 0.05

[sub_resource type="StandardMaterial3D" id="Mat_TireRubber"]
albedo_color = Color(0.08, 0.08, 0.1, 1)
roughness = 0.85

[sub_resource type="StandardMaterial3D" id="Mat_RimChrome"]
albedo_color = Color(0.9, 0.9, 0.95, 1)
metallic = 1.0
roughness = 0.1

[sub_resource type="StandardMaterial3D" id="Mat_NeonCyan"]
albedo_color = Color(0.0, 0.95, 1.0, 1)
emission_enabled = true
emission = Color(0.0, 0.95, 1.0, 1)
emission_energy_multiplier = 5.0

[sub_resource type="StandardMaterial3D" id="Mat_RedTailLight"]
albedo_color = Color(1.0, 0.1, 0.1, 1)
emission_enabled = true
emission = Color(1.0, 0.1, 0.1, 1)
emission_energy_multiplier = 4.0

[sub_resource type="StandardMaterial3D" id="Mat_Headlight"]
albedo_color = Color(0.95, 0.98, 1.0, 1)
emission_enabled = true
emission = Color(0.95, 0.98, 1.0, 1)
emission_energy_multiplier = 6.0

# Meshes
[sub_resource type="BoxMesh" id="Mesh_LowerBody"]
material = SubResource("Mat_StainlessSteel")
size = Vector3(2.1, 0.5, 4.4)

[sub_resource type="PrismMesh" id="Mesh_WedgeHood"]
material = SubResource("Mat_StainlessSteel")
size = Vector3(2.08, 0.45, 1.8)

[sub_resource type="BoxMesh" id="Mesh_RoofCabin"]
material = SubResource("Mat_Glass")
size = Vector3(1.85, 0.55, 1.6)

[sub_resource type="BoxMesh" id="Mesh_FrontBumper"]
material = SubResource("Mat_DarkChassis")
size = Vector3(2.12, 0.35, 0.4)

[sub_resource type="BoxMesh" id="Mesh_RearDeck"]
material = SubResource("Mat_DarkChassis")
size = Vector3(1.95, 0.4, 1.2)

[sub_resource type="CylinderMesh" id="Mesh_FluxThruster"]
material = SubResource("Mat_NeonCyan")
top_radius = 0.2
bottom_radius = 0.25
height = 0.6

[sub_resource type="CylinderMesh" id="Mesh_WheelTire"]
material = SubResource("Mat_TireRubber")
top_radius = 0.42
bottom_radius = 0.42
height = 0.32

[sub_resource type="CylinderMesh" id="Mesh_WheelRim"]
material = SubResource("Mat_RimChrome")
top_radius = 0.28
bottom_radius = 0.28
height = 0.33

[node name="DeLoreanTimeMachine" type="CharacterBody3D"]
script = ExtResource("1_script")

[node name="BodyLower" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.45, 0)
mesh = SubResource("Mesh_LowerBody")

[node name="WedgeHood" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, -4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 0.68, -1.3)
mesh = SubResource("Mesh_WedgeHood")

[node name="RoofCabin" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.95, 0.1)
mesh = SubResource("Mesh_RoofCabin")

[node name="FrontBumper" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.38, -2.15)
mesh = SubResource("Mesh_FrontBumper")

[node name="RearDeck" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.8, 1.4)
mesh = SubResource("Mesh_RearDeck")

# Twin Rear Flux Thrusters
[node name="FluxThrusterLeft" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, -4.37114e-08, -1, 0, 1, -4.37114e-08, -0.6, 0.85, 2.05)
mesh = SubResource("Mesh_FluxThruster")

[node name="FluxThrusterRight" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, -4.37114e-08, -1, 0, 1, -4.37114e-08, 0.6, 0.85, 2.05)
mesh = SubResource("Mesh_FluxThruster")

# Headlights & Taillights
[node name="HeadlightLeft" type="OmniLight3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.7, 0.45, -2.3)
light_color = Color(0.95, 0.98, 1.0, 1)
light_energy = 5.0
omni_range = 8.0

[node name="HeadlightRight" type="OmniLight3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.7, 0.45, -2.3)
light_color = Color(0.95, 0.98, 1.0, 1)
light_energy = 5.0
omni_range = 8.0

[node name="RearTaillight" type="OmniLight3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.7, 2.25)
light_color = Color(1.0, 0.1, 0.1, 1)
light_energy = 4.0
omni_range = 5.0

# 4 Detailed Wheels (Tire + Chrome Rim)
[node name="WheelFL" type="Node3D" parent="."]
transform = Transform3D(-4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 0, 0, 1, -1.1, 0.42, -1.4)

[node name="Tire" type="MeshInstance3D" parent="WheelFL"]
mesh = SubResource("Mesh_WheelTire")

[node name="Rim" type="MeshInstance3D" parent="WheelFL"]
mesh = SubResource("Mesh_WheelRim")

[node name="WheelFR" type="Node3D" parent="."]
transform = Transform3D(-4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 0, 0, 1, 1.1, 0.42, -1.4)

[node name="Tire" type="MeshInstance3D" parent="WheelFR"]
mesh = SubResource("Mesh_WheelTire")

[node name="Rim" type="MeshInstance3D" parent="WheelFR"]
mesh = SubResource("Mesh_WheelRim")

[node name="WheelRL" type="Node3D" parent="."]
transform = Transform3D(-4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 0, 0, 1, -1.1, 0.42, 1.4)

[node name="Tire" type="MeshInstance3D" parent="WheelRL"]
mesh = SubResource("Mesh_WheelTire")

[node name="Rim" type="MeshInstance3D" parent="WheelRL"]
mesh = SubResource("Mesh_WheelRim")

[node name="WheelRR" type="Node3D" parent="."]
transform = Transform3D(-4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 0, 0, 1, 1.1, 0.42, 1.4)

[node name="Tire" type="MeshInstance3D" parent="WheelRR"]
mesh = SubResource("Mesh_WheelTire")

[node name="Rim" type="MeshInstance3D" parent="WheelRR"]
mesh = SubResource("Mesh_WheelRim")

[node name="FluxCapacitor" type="OmniLight3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.1, 0)
light_color = Color(0.0, 0.95, 1.0, 1)
light_energy = 4.0
omni_range = 5.0

[node name="Label3D" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.2, 0)
billboard = 1
pixel_size = 0.015
text = "PARZIVAL'S HIGH-DETAIL DELOREAN TIME MACHINE
'88 MPH Into the OASIS!'"
font_size = 36
outline_size = 8
"""

# ==============================================================================
# 2. HIGH DETAIL PLAYABLE PARZIVAL AVATAR (scenes/player_vr/pc_player.tscn)
# ==============================================================================
PARZIVAL_PLAYER_TSCN = """
[gd_scene load_steps=18 format=3 uid="uid://pc_player_scene"]

[ext_resource type="Script" path="res://scripts/player_vr/third_person_controller.gd" id="1_controller"]
[ext_resource type="PackedScene" uid="uid://scene_navigator_ui" path="res://scenes/ui/scene_navigator.tscn" id="2_navigator"]
[ext_resource type="PackedScene" uid="uid://command_menu_ui" path="res://scenes/ui/command_menu.tscn" id="3_command_menu"]

[sub_resource type="CapsuleShape3D" id="CapsuleShape3D_player"]

[sub_resource type="StandardMaterial3D" id="Mat_ArmorSuit"]
albedo_color = Color(0.12, 0.16, 0.24, 1)
metallic = 0.85
roughness = 0.2

[sub_resource type="StandardMaterial3D" id="Mat_PlatingGold"]
albedo_color = Color(0.95, 0.75, 0.2, 1)
metallic = 0.95
roughness = 0.15

[sub_resource type="StandardMaterial3D" id="Mat_GlowCyan"]
albedo_color = Color(0.0, 0.95, 1.0, 1)
emission_enabled = true
emission = Color(0.0, 0.95, 1.0, 1)
emission_energy_multiplier = 5.0

[sub_resource type="StandardMaterial3D" id="Mat_SkinFace"]
albedo_color = Color(0.9, 0.75, 0.65, 1)

[sub_resource type="StandardMaterial3D" id="Mat_HairParzival"]
albedo_color = Color(0.8, 0.7, 0.3, 1)

# Body Meshes
[sub_resource type="CapsuleMesh" id="Mesh_Torso"]
material = SubResource("Mat_ArmorSuit")
radius = 0.32
height = 0.95

[sub_resource type="BoxMesh" id="Mesh_ChestPlate"]
material = SubResource("Mat_PlatingGold")
size = Vector3(0.55, 0.4, 0.2)

[sub_resource type="CylinderMesh" id="Mesh_ArcReactor"]
material = SubResource("Mat_GlowCyan")
top_radius = 0.08
bottom_radius = 0.08
height = 0.1

[sub_resource type="BoxMesh" id="Mesh_ShoulderPad"]
material = SubResource("Mat_ArmorSuit")
size = Vector3(0.35, 0.2, 0.3)

[sub_resource type="SphereMesh" id="Mesh_Head"]
material = SubResource("Mat_SkinFace")
radius = 0.22
height = 0.44

[sub_resource type="BoxMesh" id="Mesh_VRVisor"]
material = SubResource("Mat_GlowCyan")
size = Vector3(0.38, 0.11, 0.16)

[sub_resource type="CylinderMesh" id="Mesh_LimbLeg"]
material = SubResource("Mat_ArmorSuit")
top_radius = 0.09
bottom_radius = 0.07
height = 0.85

[sub_resource type="BoxMesh" id="Mesh_Boot"]
material = SubResource("Mat_PlatingGold")
size = Vector3(0.18, 0.15, 0.32)

[node name="PCPlayer" type="CharacterBody3D" groups=["player"]]
script = ExtResource("1_controller")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0)
shape = SubResource("CapsuleShape3D_player")

[node name="MeshPivot" type="Node3D" parent="."]

# Articulated Humanoid Avatar Frame
[node name="Torso" type="MeshInstance3D" parent="MeshPivot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.1, 0)
mesh = SubResource("Mesh_Torso")

[node name="ChestArmor" type="MeshInstance3D" parent="MeshPivot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.22, -0.15)
mesh = SubResource("Mesh_ChestPlate")

[node name="ArcReactor" type="MeshInstance3D" parent="MeshPivot"]
transform = Transform3D(1, 0, 0, 0, -4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 1.25, -0.26)
mesh = SubResource("Mesh_ArcReactor")

[node name="ShoulderLeft" type="MeshInstance3D" parent="MeshPivot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.42, 1.35, 0)
mesh = SubResource("Mesh_ShoulderPad")

[node name="ShoulderRight" type="MeshInstance3D" parent="MeshPivot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.42, 1.35, 0)
mesh = SubResource("Mesh_ShoulderPad")

[node name="Head" type="MeshInstance3D" parent="MeshPivot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.72, 0)
mesh = SubResource("Mesh_Head")

[node name="VRVisor" type="MeshInstance3D" parent="MeshPivot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.75, -0.18)
mesh = SubResource("Mesh_VRVisor")

[node name="LeftLeg" type="MeshInstance3D" parent="MeshPivot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.16, 0.42, 0)
mesh = SubResource("Mesh_LimbLeg")

[node name="RightLeg" type="MeshInstance3D" parent="MeshPivot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.16, 0.42, 0)
mesh = SubResource("Mesh_LimbLeg")

[node name="LeftBoot" type="MeshInstance3D" parent="MeshPivot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.16, 0.08, -0.05)
mesh = SubResource("Mesh_Boot")

[node name="RightBoot" type="MeshInstance3D" parent="MeshPivot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.16, 0.08, -0.05)
mesh = SubResource("Mesh_Boot")

[node name="SpringArm3D" type="SpringArm3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.9659, 0.2588, 0, -0.2588, 0.9659, 0, 2.2, 0)
spring_length = 3.5

[node name="Camera3D" type="Camera3D" parent="SpringArm3D"]
current = true
near = 0.05

[node name="SceneNavigator" parent="." instance=ExtResource("2_navigator")]

[node name="CommandMenu" parent="." instance=ExtResource("3_command_menu")]
"""

# ==============================================================================
# 3. HIGH DETAIL GUNDAM RX-78-2 MECH (scenes/characters/gundam_mech.tscn)
# ==============================================================================
GUNDAM_MECH_TSCN = """
[gd_scene load_steps=18 format=3 uid="uid://gundam_mech_scene"]

[ext_resource type="Script" path="res://scripts/characters/gundam_mech.gd" id="1_script"]

[sub_resource type="StandardMaterial3D" id="Mat_WhiteArmor"]
albedo_color = Color(0.92, 0.94, 0.98, 1)
metallic = 0.85
roughness = 0.2

[sub_resource type="StandardMaterial3D" id="Mat_BlueChest"]
albedo_color = Color(0.08, 0.25, 0.75, 1)
metallic = 0.85
roughness = 0.2

[sub_resource type="StandardMaterial3D" id="Mat_RedTrim"]
albedo_color = Color(0.85, 0.1, 0.15, 1)
metallic = 0.85
roughness = 0.2

[sub_resource type="StandardMaterial3D" id="Mat_YellowCrest"]
albedo_color = Color(1.0, 0.85, 0.1, 1)
emission_enabled = true
emission = Color(1.0, 0.85, 0.1, 1)
emission_energy_multiplier = 4.0

[sub_resource type="StandardMaterial3D" id="Mat_GreenEyes"]
albedo_color = Color(0.0, 1.0, 0.4, 1)
emission_enabled = true
emission = Color(0.0, 1.0, 0.4, 1)
emission_energy_multiplier = 6.0

# Geometry
[sub_resource type="BoxMesh" id="Mesh_Chest"]
material = SubResource("Mat_BlueChest")
size = Vector3(2.4, 2.6, 1.6)

[sub_resource type="BoxMesh" id="Mesh_WaistRed"]
material = SubResource("Mat_RedTrim")
size = Vector3(2.2, 0.8, 1.5)

[sub_resource type="BoxMesh" id="Mesh_ShoulderWhite"]
material = SubResource("Mat_WhiteArmor")
size = Vector3(1.2, 1.1, 1.3)

[sub_resource type="BoxMesh" id="Mesh_ArmWhite"]
material = SubResource("Mat_WhiteArmor")
size = Vector3(0.75, 2.4, 0.75)

[sub_resource type="BoxMesh" id="Mesh_LegWhite"]
material = SubResource("Mat_WhiteArmor")
size = Vector3(0.85, 3.2, 0.95)

[sub_resource type="SphereMesh" id="Mesh_Helmet"]
material = SubResource("Mat_WhiteArmor")
radius = 0.65
height = 1.3

[sub_resource type="PrismMesh" id="Mesh_VFin"]
material = SubResource("Mat_YellowCrest")
size = Vector3(1.8, 0.7, 0.15)

[sub_resource type="BoxMesh" id="Mesh_VisorEyes"]
material = SubResource("Mat_GreenEyes")
size = Vector3(0.9, 0.22, 0.25)

[sub_resource type="BoxMesh" id="Mesh_ShieldRed"]
material = SubResource("Mat_RedTrim")
size = Vector3(1.8, 3.8, 0.3)

[node name="GundamRX78Mech" type="CharacterBody3D"]
script = ExtResource("1_script")

[node name="Chest" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4.2, 0)
mesh = SubResource("Mesh_Chest")

[node name="Waist" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.5, 0)
mesh = SubResource("Mesh_WaistRed")

[node name="ShoulderLeft" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -1.8, 4.8, 0)
mesh = SubResource("Mesh_ShoulderWhite")

[node name="ShoulderRight" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 1.8, 4.8, 0)
mesh = SubResource("Mesh_ShoulderWhite")

[node name="ArmLeft" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -1.8, 3.2, 0)
mesh = SubResource("Mesh_ArmWhite")

[node name="ArmRight" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 1.8, 3.2, 0)
mesh = SubResource("Mesh_ArmWhite")

[node name="LegLeft" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.65, 1.2, 0)
mesh = SubResource("Mesh_LegWhite")

[node name="LegRight" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.65, 1.2, 0)
mesh = SubResource("Mesh_LegWhite")

[node name="Helmet" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 6.1, 0)
mesh = SubResource("Mesh_Helmet")

[node name="VFinCrest" type="MeshInstance3D" parent="Helmet"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.55, -0.55)
mesh = SubResource("Mesh_VFin")

[node name="VisorEyes" type="MeshInstance3D" parent="Helmet"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.05, -0.58)
mesh = SubResource("Mesh_VisorEyes")

[node name="Shield" type="MeshInstance3D" parent="."]
transform = Transform3D(0.965926, 0, 0.258819, 0, 1, 0, -0.258819, 0, 0.965926, -2.4, 3.5, 0.4)
mesh = SubResource("Mesh_ShieldRed")

[node name="EyeLight" type="OmniLight3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 6.15, -0.8)
light_color = Color(0.0, 1.0, 0.4, 1)
light_energy = 5.0
omni_range = 6.0

[node name="Label3D" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 7.5, 0)
billboard = 1
pixel_size = 0.02
text = "GUNDAM RX-78-2 BATTLE MECH AVATAR
'Ready Player One Climax Battle Mech!'"
font_size = 48
outline_size = 12
"""

# Save High Detail Models
write_file(os.path.join(BASE_DIR, "scenes/vehicles/delorean_car.tscn"), DELOREAN_TSCN)
write_file(os.path.join(BASE_DIR, "scenes/player_vr/pc_player.tscn"), PARZIVAL_PLAYER_TSCN)
write_file(os.path.join(BASE_DIR, "scenes/characters/gundam_mech.tscn"), GUNDAM_MECH_TSCN)

print("High-detail 3D models generated for DeLorean, Parzival, and Gundam RX-78!")
