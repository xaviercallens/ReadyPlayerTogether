import os

BASE_DIR = r"C:\Users\Utilisateur\.gemini\antigravity\scratch\project_oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# 1. PARZIVAL NPC SCRIPT
PARZIVAL_GD = """
extends CharacterBody3D

# ==============================================================================
# PROJET OASIS - Parzival (Ready Player One Gunter NPC)
# Interacts with the player, floating key animation, Gemini AI dialogue trigger.
# ==============================================================================

@onready var key_mesh: MeshInstance3D = $KeyMesh
@onready var dialogue_label: Label3D = $DialogueLabel

var time_passed: float = 0.0
var is_player_near: bool = false

func _ready() -> void:
	$InteractionArea.body_entered.connect(_on_body_entered)
	$InteractionArea.body_exited.connect(_on_body_exited)
	dialogue_label.text = "PARZIVAL: 'Trouve la Clé de Cuivre!'"

func _process(delta: float) -> void:
	# Floating & rotation animation for the Copper Key above Parzival's head
	time_passed += delta
	if key_mesh:
		key_mesh.rotation.y += delta * 2.0
		key_mesh.position.y = 2.4 + sin(time_passed * 3.0) * 0.1

func _on_body_entered(body: Node3D) -> void:
	if body.is_in_group("player"):
		is_player_near = true
		dialogue_label.text = "PARZIVAL: 'Bienvenue Gunter! Traverse le portail 03 pour la course!'"

func _on_body_exited(body: Node3D) -> void:
	if body.is_in_group("player"):
		is_player_near = false
		dialogue_label.text = "PARZIVAL: 'Trouve la Clé de Cuivre!'"
"""

# 2. PARZIVAL NPC SCENE (.tscn)
PARZIVAL_TSCN = """
[gd_scene load_steps=9 format=3 uid="uid://parzival_npc_scene"]

[ext_resource type="Script" path="res://scripts/characters/parzival_npc.gd" id="1_script"]

[sub_resource type="StandardMaterial3D" id="Mat_ParzivalBody"]
albedo_color = Color(0.15, 0.3, 0.6, 1)
roughness = 0.4

[sub_resource type="CapsuleMesh" id="Mesh_Body"]
material = SubResource("Mat_ParzivalBody")
radius = 0.4
height = 1.8

[sub_resource type="StandardMaterial3D" id="Mat_Visor"]
albedo_color = Color(0.0, 1.0, 0.8, 1)
emission_enabled = true
emission = Color(0.0, 1.0, 0.8, 1)
emission_energy_multiplier = 3.0

[sub_resource type="BoxMesh" id="Mesh_Visor"]
material = SubResource("Mat_Visor")
size = Vector3(0.5, 0.15, 0.2)

[sub_resource type="StandardMaterial3D" id="Mat_Key"]
albedo_color = Color(1.0, 0.7, 0.1, 1)
metallic = 0.9
roughness = 0.1
emission_enabled = true
emission = Color(1.0, 0.7, 0.1, 1)
emission_energy_multiplier = 2.0

[sub_resource type="BoxMesh" id="Mesh_Key"]
material = SubResource("Mat_Key")
size = Vector3(0.3, 0.3, 0.3)

[sub_resource type="CylinderShape3D" id="Shape_Interact"]
height = 3.0
radius = 4.0

[node name="ParzivalNPC" type="CharacterBody3D"]
script = ExtResource("1_script")

[node name="BodyMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.9, 0)
mesh = SubResource("Mesh_Body")

[node name="VisorMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.5, -0.3)
mesh = SubResource("Mesh_Visor")

[node name="KeyMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.4, 0)
mesh = SubResource("Mesh_Key")

[node name="NameTag" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.0, 0)
pixel_size = 0.015
text = "PARZIVAL (First to the Key)"
font_size = 36
outline_size = 8

[node name="DialogueLabel" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.8, 0)
pixel_size = 0.015
text = "PARZIVAL: 'Trouve la Clé de Cuivre!'"
font_size = 42
outline_size = 10

[node name="InteractionArea" type="Area3D" parent="."]

[node name="CollisionShape3D" type="CollisionShape3D" parent="InteractionArea"]
shape = SubResource("Shape_Interact")
"""

write_file(os.path.join(BASE_DIR, "scripts/characters/parzival_npc.gd"), PARZIVAL_GD)
write_file(os.path.join(BASE_DIR, "scenes/characters/parzival_npc.tscn"), PARZIVAL_TSCN)

print("Parzival character scene and script created successfully.")
