import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# 1. THIRD-PERSON CAMERA IN PC_PLAYER (scenes/player_vr/pc_player.tscn)
# Positioned behind & above the player: (0, 2.8, 3.8) tilted down 15 deg.
# ==============================================================================
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
transform = Transform3D(1, 0, 0, 0, 0.9659, 0.2588, 0, -0.2588, 0.9659, 0, 2.8, 3.8)
current = true
near = 0.05

[node name="SceneNavigator" parent="." instance=ExtResource("2_navigator")]

[node name="CommandMenu" parent="." instance=ExtResource("3_command_menu")]
"""

write_file(os.path.join(BASE_DIR, "scenes/player_vr/pc_player.tscn"), PC_PLAYER_TSCN)

# ==============================================================================
# 2. UPDATE LAUNCHERS FOR DESKTOP MODE NO VR (Launch_Oasis.bat & Launch_Oasis.ps1)
# ==============================================================================
BAT_CONTENT = """@echo off
echo Starting Projet OASIS (Desktop Mode - No VR)...
"C:\\Users\\Utilisateur\\AppData\\Local\\Microsoft\\WinGet\\Packages\\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\\Godot_v4.7.1-stable_win64.exe" --path "D:\\xdev\\Oasis"
"""

PS1_CONTENT = """Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " Launching Projet OASIS (Desktop Mode)..." -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
& "C:\\Users\\Utilisateur\\AppData\\Local\\Microsoft\\WinGet\\Packages\\GodotEngine.GodotEngine_Microsoft.Winget.Source_8wekyb3d8bbwe\\Godot_v4.7.1-stable_win64.exe" --path "D:\\xdev\\Oasis"
"""

write_file(os.path.join(BASE_DIR, "Launch_Oasis.bat"), BAT_CONTENT)
write_file(os.path.join(BASE_DIR, "Launch_Oasis.ps1"), PS1_CONTENT)

print("Camera third-person view & desktop launcher scripts updated successfully!")
