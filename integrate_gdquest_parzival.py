import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# PARZIVAL GDQUEST MANNEQUIN PLAYER (scenes/player_vr/pc_player.tscn)
# ==============================================================================
GDQUEST_PARZIVAL_PLAYER_TSCN = """[gd_scene load_steps=10 format=3 uid="uid://pc_player_scene"]

[ext_resource type="Script" path="res://scripts/player_vr/third_person_controller.gd" id="1_controller"]
[ext_resource type="PackedScene" uid="uid://scene_navigator_ui" path="res://scenes/ui/scene_navigator.tscn" id="2_navigator"]
[ext_resource type="PackedScene" uid="uid://command_menu_ui" path="res://scenes/ui/command_menu.tscn" id="3_command_menu"]
[ext_resource type="PackedScene" path="res://assets/gdquest_mannequin/godot/assets/3d/mannequiny/mannequiny-0.3.0.glb" id="4_mannequin_glb"]

[sub_resource type="CapsuleShape3D" id="CapsuleShape3D_player"]
radius = 0.35
height = 1.8

[sub_resource type="StandardMaterial3D" id="Mat_VisorGold"]
albedo_color = Color(1.0, 0.8, 0.1, 1)
metallic = 0.95
roughness = 0.1
emission_enabled = true
emission = Color(1.0, 0.8, 0.1, 1)
emission_energy_multiplier = 4.0

[sub_resource type="BoxMesh" id="Mesh_VRVisor"]
material = SubResource("Mat_VisorGold")
size = Vector3(0.32, 0.1, 0.16)

[sub_resource type="StandardMaterial3D" id="Mat_ArcReactorCyan"]
albedo_color = Color(0.0, 0.95, 1.0, 1)
emission_enabled = true
emission = Color(0.0, 0.95, 1.0, 1)
emission_energy_multiplier = 5.0

[sub_resource type="CylinderMesh" id="Mesh_ArcReactor"]
material = SubResource("Mat_ArcReactorCyan")
top_radius = 0.08
bottom_radius = 0.08
height = 0.08

[node name="PCPlayer" type="CharacterBody3D" groups=["player"]]
script = ExtResource("1_controller")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.9, 0)
shape = SubResource("CapsuleShape3D_player")

[node name="MeshPivot" type="Node3D" parent="."]

# Cloned GDQuest 3D Mannequiny Model (Full Skeletal Mesh & Textures)
[node name="MannequinyModel" parent="MeshPivot" instance=ExtResource("4_mannequin_glb")]
transform = Transform3D(-1, 0, -8.74228e-08, 0, 1, 0, 8.74228e-08, 0, -1, 0, 0, 0)

# Parzival Ready Player One Sci-Fi Overlay (VR Visor + Arc Reactor)
[node name="ParzivalVisor" type="MeshInstance3D" parent="MeshPivot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.62, -0.16)
mesh = SubResource("Mesh_VRVisor")

[node name="ParzivalArcReactor" type="MeshInstance3D" parent="MeshPivot"]
transform = Transform3D(1, 0, 0, 0, -4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 1.25, -0.22)
mesh = SubResource("Mesh_ArcReactor")

[node name="SpringArm3D" type="SpringArm3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.9659, 0.2588, 0, -0.2588, 0.9659, 0, 2.2, 0)
spring_length = 3.5

[node name="Camera3D" type="Camera3D" parent="SpringArm3D"]
current = true
near = 0.05

[node name="SceneNavigator" parent="." instance=ExtResource("2_navigator")]

[node name="CommandMenu" parent="." instance=ExtResource("3_command_menu")]
"""

write_file(os.path.join(BASE_DIR, "scenes/player_vr/pc_player.tscn"), GDQUEST_PARZIVAL_PLAYER_TSCN)

print("GDQuest Mannequin 3D GLB model integrated for Parzival player character!")
