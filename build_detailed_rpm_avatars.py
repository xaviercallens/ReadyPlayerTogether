import os

BASE_DIR = r"C:\Users\Utilisateur\.gemini\antigravity\scratch\project_oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# 1. PARZIVAL DETAILED READY PLAYER ME HUMANOID (.tscn)
# ==============================================================================
PARZIVAL_DETAILED_TSCN = """
[gd_scene load_steps=12 format=3 uid="uid://parzival_npc_scene"]

[ext_resource type="Script" path="res://scripts/characters/parzival_npc.gd" id="1_script"]

[sub_resource type="StandardMaterial3D" id="Mat_Skin"]
albedo_color = Color(0.92, 0.75, 0.65, 1)

[sub_resource type="StandardMaterial3D" id="Mat_Jacket"]
albedo_color = Color(0.1, 0.25, 0.55, 1)
roughness = 0.5

[sub_resource type="StandardMaterial3D" id="Mat_Pants"]
albedo_color = Color(0.12, 0.12, 0.18, 1)

[sub_resource type="StandardMaterial3D" id="Mat_Visor"]
albedo_color = Color(0.0, 1.0, 0.9, 1)
emission_enabled = true
emission = Color(0.0, 1.0, 0.9, 1)
emission_energy_multiplier = 4.0

[sub_resource type="StandardMaterial3D" id="Mat_Key"]
albedo_color = Color(1.0, 0.8, 0.2, 1)
metallic = 0.9
roughness = 0.1
emission_enabled = true
emission = Color(1.0, 0.8, 0.2, 1)
emission_energy_multiplier = 3.0

[sub_resource type="CapsuleMesh" id="Mesh_Torso"]
material = SubResource("Mat_Jacket")
radius = 0.32
height = 0.9

[sub_resource type="SphereMesh" id="Mesh_Head"]
material = SubResource("Mat_Skin")
radius = 0.22
height = 0.44

[sub_resource type="BoxMesh" id="Mesh_Visor"]
material = SubResource("Mat_Visor")
size = Vector3(0.4, 0.12, 0.15)

[sub_resource type="CylinderMesh" id="Mesh_Limb"]
material = SubResource("Mat_Pants")
top_radius = 0.08
bottom_radius = 0.07
height = 0.8

[sub_resource type="CylinderShape3D" id="Shape_Interact"]
height = 3.0
radius = 4.0

[node name="ParzivalNPC" type="CharacterBody3D"]
script = ExtResource("1_script")

[node name="BodyMesh" type="Node3D" parent="."]

[node name="Torso" type="MeshInstance3D" parent="BodyMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.05, 0)
mesh = SubResource("Mesh_Torso")

[node name="Head" type="MeshInstance3D" parent="BodyMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.68, 0)
mesh = SubResource("Mesh_Head")

[node name="Visor" type="MeshInstance3D" parent="BodyMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.7, -0.18)
mesh = SubResource("Mesh_Visor")

[node name="LeftLeg" type="MeshInstance3D" parent="BodyMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.15, 0.4, 0)
mesh = SubResource("Mesh_Limb")

[node name="RightLeg" type="MeshInstance3D" parent="BodyMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.15, 0.4, 0)
mesh = SubResource("Mesh_Limb")

[node name="KeyMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.3, 0)
mesh = SubResource("Mesh_Visor")

[node name="NameTag" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.1, 0)
pixel_size = 0.015
text = "PARZIVAL (RPM Avatar)"
font_size = 36
outline_size = 8

[node name="DialogueLabel" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.7, 0)
pixel_size = 0.015
text = "PARZIVAL: 'Trouve la Clé de Cuivre!'"
font_size = 42
outline_size = 10

[node name="InteractionArea" type="Area3D" parent="."]

[node name="CollisionShape3D" type="CollisionShape3D" parent="InteractionArea"]
shape = SubResource("Shape_Interact")
"""

# ==============================================================================
# 2. ART3MIS DETAILED READY PLAYER ME HUMANOID (.tscn)
# ==============================================================================
ART3MIS_DETAILED_TSCN = """
[gd_scene load_steps=12 format=3 uid="uid://art3mis_npc_scene"]

[ext_resource type="Script" path="res://scripts/characters/art3mis_npc.gd" id="1_script"]

[sub_resource type="StandardMaterial3D" id="Mat_Skin"]
albedo_color = Color(0.95, 0.8, 0.7, 1)

[sub_resource type="StandardMaterial3D" id="Mat_Jacket"]
albedo_color = Color(0.85, 0.1, 0.45, 1)
roughness = 0.3

[sub_resource type="StandardMaterial3D" id="Mat_Hair"]
albedo_color = Color(0.9, 0.05, 0.2, 1)

[sub_resource type="StandardMaterial3D" id="Mat_Visor"]
albedo_color = Color(1.0, 0.0, 0.6, 1)
emission_enabled = true
emission = Color(1.0, 0.0, 0.6, 1)
emission_energy_multiplier = 4.0

[sub_resource type="CapsuleMesh" id="Mesh_Torso"]
material = SubResource("Mat_Jacket")
radius = 0.28
height = 0.85

[sub_resource type="SphereMesh" id="Mesh_Head"]
material = SubResource("Mat_Skin")
radius = 0.2,
height = 0.4

[sub_resource type="SphereMesh" id="Mesh_Hair"]
material = SubResource("Mat_Hair")
radius = 0.23,
height = 0.42

[sub_resource type="BoxMesh" id="Mesh_Visor"]
material = SubResource("Mat_Visor")
size = Vector3(0.38, 0.1, 0.14)

[sub_resource type="CylinderMesh" id="Mesh_Limb"]
material = SubResource("Mat_Jacket")
top_radius = 0.07
bottom_radius = 0.06
height = 0.8

[sub_resource type="CylinderShape3D" id="Shape_Interact"]
height = 3.0
radius = 4.0

[node name="Art3misNPC" type="CharacterBody3D"]
script = ExtResource("1_script")

[node name="BodyMesh" type="Node3D" parent="."]

[node name="Torso" type="MeshInstance3D" parent="BodyMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.0, 0)
mesh = SubResource("Mesh_Torso")

[node name="Hair" type="MeshInstance3D" parent="BodyMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.63, 0.02)
mesh = SubResource("Mesh_Hair")

[node name="Head" type="MeshInstance3D" parent="BodyMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.6, 0)
mesh = SubResource("Mesh_Head")

[node name="Visor" type="MeshInstance3D" parent="BodyMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.62, -0.16)
mesh = SubResource("Mesh_Visor")

[node name="LeftLeg" type="MeshInstance3D" parent="BodyMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.14, 0.4, 0)
mesh = SubResource("Mesh_Limb")

[node name="RightLeg" type="MeshInstance3D" parent="BodyMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.14, 0.4, 0)
mesh = SubResource("Mesh_Limb")

[node name="KeyMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.3, 0)
mesh = SubResource("Mesh_Visor")

[node name="NameTag" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.1, 0)
pixel_size = 0.015
text = "ART3MIS (RPM Avatar)"
font_size = 36
outline_size = 8

[node name="DialogueLabel" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.7, 0)
pixel_size = 0.015
text = "ART3MIS: 'La Clé de Jade t'attend...'"
font_size = 42
outline_size = 10

[node name="InteractionArea" type="Area3D" parent="."]

[node name="CollisionShape3D" type="CollisionShape3D" parent="InteractionArea"]
shape = SubResource("Shape_Interact")
"""

# ==============================================================================
# 3. AECH DETAILED READY PLAYER ME MECH (.tscn)
# ==============================================================================
AECH_DETAILED_TSCN = """
[gd_scene load_steps=11 format=3 uid="uid://aech_npc_scene"]

[ext_resource type="Script" path="res://scripts/characters/aech_npc.gd" id="1_script"]

[sub_resource type="StandardMaterial3D" id="Mat_Armor"]
albedo_color = Color(0.2, 0.45, 0.8, 1)
metallic = 0.8
roughness = 0.2

[sub_resource type="StandardMaterial3D" id="Mat_Glow"]
albedo_color = Color(0.0, 0.8, 1.0, 1)
emission_enabled = true
emission = Color(0.0, 0.8, 1.0, 1)
emission_energy_multiplier = 4.0

[sub_resource type="BoxMesh" id="Mesh_Torso"]
material = SubResource("Mat_Armor")
size = Vector3(0.9, 1.1, 0.6)

[sub_resource type="BoxMesh" id="Mesh_Shoulder"]
material = SubResource("Mat_Glow")
size = Vector3(0.4, 0.3, 0.4)

[sub_resource type="SphereMesh" id="Mesh_Head"]
material = SubResource("Mat_Armor")
radius = 0.26
height = 0.52

[sub_resource type="BoxMesh" id="Mesh_Visor"]
material = SubResource("Mat_Glow")
size = Vector3(0.5, 0.15, 0.15)

[sub_resource type="CylinderMesh" id="Mesh_Limb"]
material = SubResource("Mat_Armor")
top_radius = 0.12
bottom_radius = 0.1
height = 0.9

[sub_resource type="CylinderShape3D" id="Shape_Interact"]
height = 3.0
radius = 4.5

[node name="AechNPC" type="CharacterBody3D"]
script = ExtResource("1_script")

[node name="BodyMesh" type="Node3D" parent="."]

[node name="Torso" type="MeshInstance3D" parent="BodyMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.15, 0)
mesh = SubResource("Mesh_Torso")

[node name="LeftShoulder" type="MeshInstance3D" parent="BodyMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.65, 1.5, 0)
mesh = SubResource("Mesh_Shoulder")

[node name="RightShoulder" type="MeshInstance3D" parent="BodyMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.65, 1.5, 0)
mesh = SubResource("Mesh_Shoulder")

[node name="Head" type="MeshInstance3D" parent="BodyMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.85, 0)
mesh = SubResource("Mesh_Head")

[node name="Visor" type="MeshInstance3D" parent="BodyMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.88, -0.22)
mesh = SubResource("Mesh_Visor")

[node name="LeftLeg" type="MeshInstance3D" parent="BodyMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.28, 0.45, 0)
mesh = SubResource("Mesh_Limb")

[node name="RightLeg" type="MeshInstance3D" parent="BodyMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.28, 0.45, 0)
mesh = SubResource("Mesh_Limb")

[node name="NameTag" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.5, 0)
pixel_size = 0.015
text = "AECH (Master Mech RPM)"
font_size = 36
outline_size = 8

[node name="DialogueLabel" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3.1, 0)
pixel_size = 0.015
text = "AECH: 'Bienvenue au Garage!'"
font_size = 42
outline_size = 10

[node name="InteractionArea" type="Area3D" parent="."]

[node name="CollisionShape3D" type="CollisionShape3D" parent="InteractionArea"]
shape = SubResource("Shape_Interact")
"""

write_file(os.path.join(BASE_DIR, "scenes/characters/parzival_npc.tscn"), PARZIVAL_DETAILED_TSCN)
write_file(os.path.join(BASE_DIR, "scenes/characters/art3mis_npc.tscn"), ART3MIS_DETAILED_TSCN)
write_file(os.path.join(BASE_DIR, "scenes/characters/aech_npc.tscn"), AECH_DETAILED_TSCN)

print("Detailed Ready Player Me humanoid avatar models built successfully!")
