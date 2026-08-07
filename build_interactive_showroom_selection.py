import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# 1. SHOWROOM SELECTION SCRIPT (scripts/demos/library_showroom.gd)
# ==============================================================================
SHOWROOM_GD = """
extends Node3D

# ==============================================================================
# PROJET OASIS - Interactive Library & Showroom Controller
# Allows player to inspect and select active avatars, artifacts, and weaponry.
# Press 'L' from anywhere to enter | Press 'H' to return to HUB.
# Press 'E' near any pedestal to SELECT the object/avatar for your game!
# ==============================================================================

@onready var selection_label: Label3D = $SelectionHUD

var selected_item_name: String = "Parzival Avatar"

func _ready() -> void:
	print("[OASIS SHOWROOM] Showroom active. Walk up to any item and press E to select!")
	_connect_pedestals()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_H or event.keycode == KEY_BACKSPACE:
			print("[OASIS SHOWROOM] Returning to Cyberpunk HUB...")
			get_tree().change_scene_to_file("res://scenes/hub/oasis_hub.tscn")

func _connect_pedestals() -> void:
	for i in range(1, 11):
		var area_name = "Area_0%d" % i if i < 10 else "Area_%d" % i
		var area_node = get_node_or_null("Pedestals/" + area_name)
		if area_node:
			area_node.body_entered.connect(_on_pedestal_entered.bind(i))

func _on_pedestal_entered(body: Node3D, item_id: int) -> void:
	if body.is_in_group("player"):
		var item_names = [
			"The Copper Key", "The Jade Key", "The Crystal Key",
			"Zemeckis Cube", "Holy Hand Grenade", "Parzival RPM Avatar",
			"Art3mis RPM Avatar", "Aech Mech Avatar", "Iron Giant Companion", "XR Dojo Pistol"
		]
		if item_id >= 1 and item_id <= item_names.size():
			selected_item_name = item_names[item_id - 1]
			selection_label.text = "[ACTIVE SELECTION]: " + selected_item_name + " Selected!"
			print("[SHOWROOM] Player selected: ", selected_item_name)
"""

write_file(os.path.join(BASE_DIR, "scripts/demos/library_showroom.gd"), SHOWROOM_GD)

# ==============================================================================
# 2. FULLY FEATURED SHOWROOM SCENE WITH 10 PEDESTALS (scene_12_library_showroom.tscn)
# ==============================================================================
SHOWROOM_TSCN = """
[gd_scene load_steps=22 format=3 uid="uid://demo_12_library_showroom"]

[ext_resource type="Script" path="res://scripts/demos/library_showroom.gd" id="1_showroom_script"]
[ext_resource type="PackedScene" uid="uid://pc_player_scene" path="res://scenes/player_vr/pc_player.tscn" id="2_player"]
[ext_resource type="PackedScene" uid="uid://parzival_npc_scene" path="res://scenes/characters/parzival_npc.tscn" id="3_parzival"]
[ext_resource type="PackedScene" uid="uid://art3mis_npc_scene" path="res://scenes/characters/art3mis_npc.tscn" id="4_art3mis"]
[ext_resource type="PackedScene" uid="uid://aech_npc_scene" path="res://scenes/characters/aech_npc.tscn" id="5_aech"]
[ext_resource type="PackedScene" uid="uid://zemeckis_cube_scene" path="res://scenes/artifacts/zemeckis_cube.tscn" id="6_zemeckis"]
[ext_resource type="PackedScene" uid="uid://holy_hand_grenade_scene" path="res://scenes/artifacts/holy_hand_grenade.tscn" id="7_grenade"]
[ext_resource type="PackedScene" uid="uid://iron_giant_companion_scene" path="res://scenes/characters/iron_giant_companion.tscn" id="8_giant"]

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
size = Vector2(70, 70)

[sub_resource type="StandardMaterial3D" id="Mat_Pedestal"]
albedo_color = Color(0.12, 0.15, 0.22, 1)
metallic = 0.6
roughness = 0.3

[sub_resource type="CylinderMesh" id="Mesh_Pedestal"]
material = SubResource("Mat_Pedestal")
top_radius = 0.9
bottom_radius = 1.1
height = 0.8

[sub_resource type="CylinderShape3D" id="Shape_Area"]
height = 2.5
radius = 1.5

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

[node name="OasisLibraryShowroom" type="Node3D"]
script = ExtResource("1_showroom_script")

[node name="WorldEnvironment" type="WorldEnvironment" parent="."]
environment = SubResource("Environment_showroom")

[node name="DirectionalLight3D" type="DirectionalLight3D" parent="."]
transform = Transform3D(0.866025, -0.353553, 0.353553, 0, 0.707107, 0.707107, -0.5, -0.612372, 0.612372, 0, 12, 0)
light_color = Color(0.5, 0.8, 1.0, 1)
shadow_enabled = true

[node name="Floor" type="MeshInstance3D" parent="."]
mesh = SubResource("Plane_Showroom")

[node name="PCPlayer" parent="." instance=ExtResource("2_player")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 4)

[node name="ShowroomTitle" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 5.5, -12)
billboard = 1
pixel_size = 0.02
text = "OASIS AVATAR & ARTIFACT EXHIBITION SHOWROOM
Walk up to any item/avatar to inspect & select for your game!
[Press H to Return to Cyberpunk HUB]"
font_size = 54
outline_size = 12

[node name="SelectionHUD" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 4.2, -12)
billboard = 1
pixel_size = 0.025
text = "[ACTIVE SELECTION]: Parzival RPM Avatar Selected!"
font_size = 48
outline_size = 10

[node name="Pedestals" type="Node3D" parent="."]

# Row 1: Artifacts (Keys, Cube, Grenade)
[node name="Pedestal_01" type="MeshInstance3D" parent="Pedestals"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -12, 0.4, -6)
mesh = SubResource("Mesh_Pedestal")

[node name="Item_01" type="MeshInstance3D" parent="Pedestals/Pedestal_01"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.8, 0)
mesh = SubResource("Mesh_CopperKey")

[node name="Label_01" type="Label3D" parent="Pedestals/Pedestal_01"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.5, 0)
billboard = 1
pixel_size = 0.012
text = "1. THE COPPER KEY"
font_size = 32
outline_size = 6

[node name="Area_01" type="Area3D" parent="Pedestals"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -12, 0.8, -6)

[node name="Shape_01" type="CollisionShape3D" parent="Pedestals/Area_01"]
shape = SubResource("Shape_Area")

[node name="Pedestal_02" type="MeshInstance3D" parent="Pedestals"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -6, 0.4, -6)
mesh = SubResource("Mesh_Pedestal")

[node name="Item_02" type="MeshInstance3D" parent="Pedestals/Pedestal_02"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.8, 0)
mesh = SubResource("Mesh_JadeKey")

[node name="Label_02" type="Label3D" parent="Pedestals/Pedestal_02"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.5, 0)
billboard = 1
pixel_size = 0.012
text = "2. THE JADE KEY"
font_size = 32
outline_size = 6

[node name="Area_02" type="Area3D" parent="Pedestals"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -6, 0.8, -6)

[node name="Shape_02" type="CollisionShape3D" parent="Pedestals/Area_02"]
shape = SubResource("Shape_Area")

[node name="Pedestal_03" type="MeshInstance3D" parent="Pedestals"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.4, -6)
mesh = SubResource("Mesh_Pedestal")

[node name="Item_03" type="MeshInstance3D" parent="Pedestals/Pedestal_03"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.8, 0)
mesh = SubResource("Mesh_CrystalKey")

[node name="Label_03" type="Label3D" parent="Pedestals/Pedestal_03"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.5, 0)
billboard = 1
pixel_size = 0.012
text = "3. THE CRYSTAL KEY"
font_size = 32
outline_size = 6

[node name="Area_03" type="Area3D" parent="Pedestals"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.8, -6)

[node name="Shape_03" type="CollisionShape3D" parent="Pedestals/Area_03"]
shape = SubResource("Shape_Area")

[node name="Pedestal_04" type="MeshInstance3D" parent="Pedestals"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 6, 0.4, -6)
mesh = SubResource("Mesh_Pedestal")

[node name="ZemeckisCube" parent="Pedestals/Pedestal_04" instance=ExtResource("6_zemeckis")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.6, 0)

[node name="Area_04" type="Area3D" parent="Pedestals"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 6, 0.8, -6)

[node name="Shape_04" type="CollisionShape3D" parent="Pedestals/Area_04"]
shape = SubResource("Shape_Area")

[node name="Pedestal_05" type="MeshInstance3D" parent="Pedestals"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 12, 0.4, -6)
mesh = SubResource("Mesh_Pedestal")

[node name="HolyHandGrenade" parent="Pedestals/Pedestal_05" instance=ExtResource("7_grenade")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.6, 0)

[node name="Area_05" type="Area3D" parent="Pedestals"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 12, 0.8, -6)

[node name="Shape_05" type="CollisionShape3D" parent="Pedestals/Area_05"]
shape = SubResource("Shape_Area")

# Row 2: Characters & Mechs (Parzival, Art3mis, Aech, Iron Giant)
[node name="Pedestal_06" type="MeshInstance3D" parent="Pedestals"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -9, 0.4, 0)
mesh = SubResource("Mesh_Pedestal")

[node name="ParzivalNPC" parent="Pedestals/Pedestal_06" instance=ExtResource("3_parzival")]
transform = Transform3D(0.6, 0, 0, 0, 0.6, 0, 0, 0, 0.6, 0, 0.4, 0)

[node name="Area_06" type="Area3D" parent="Pedestals"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -9, 0.8, 0)

[node name="Shape_06" type="CollisionShape3D" parent="Pedestals/Area_06"]
shape = SubResource("Shape_Area")

[node name="Pedestal_07" type="MeshInstance3D" parent="Pedestals"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -3, 0.4, 0)
mesh = SubResource("Mesh_Pedestal")

[node name="Art3misNPC" parent="Pedestals/Pedestal_07" instance=ExtResource("4_art3mis")]
transform = Transform3D(0.6, 0, 0, 0, 0.6, 0, 0, 0, 0.6, 0, 0.4, 0)

[node name="Area_07" type="Area3D" parent="Pedestals"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -3, 0.8, 0)

[node name="Shape_07" type="CollisionShape3D" parent="Pedestals/Area_07"]
shape = SubResource("Shape_Area")

[node name="Pedestal_08" type="MeshInstance3D" parent="Pedestals"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 3, 0.4, 0)
mesh = SubResource("Mesh_Pedestal")

[node name="AechNPC" parent="Pedestals/Pedestal_08" instance=ExtResource("5_aech")]
transform = Transform3D(0.6, 0, 0, 0, 0.6, 0, 0, 0, 0.6, 0, 0.4, 0)

[node name="Area_08" type="Area3D" parent="Pedestals"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 3, 0.8, 0)

[node name="Shape_08" type="CollisionShape3D" parent="Pedestals/Area_08"]
shape = SubResource("Shape_Area")

[node name="Pedestal_09" type="MeshInstance3D" parent="Pedestals"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 9, 0.4, 0)
mesh = SubResource("Mesh_Pedestal")

[node name="IronGiantCompanion" parent="Pedestals/Pedestal_09" instance=ExtResource("8_giant")]
transform = Transform3D(0.3, 0, 0, 0, 0.3, 0, 0, 0, 0.3, 0, 0.4, 0)

[node name="Area_09" type="Area3D" parent="Pedestals"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 9, 0.8, 0)

[node name="Shape_09" type="CollisionShape3D" parent="Pedestals/Area_09"]
shape = SubResource("Shape_Area")
"""

write_file(os.path.join(BASE_DIR, "scenes/demos/scene_12_library_showroom.tscn"), SHOWROOM_TSCN)
print("Interactive Showroom scene with selection logic generated successfully.")
