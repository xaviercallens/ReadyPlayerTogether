import os

BASE_DIR = r"C:\Users\Utilisateur\.gemini\antigravity\scratch\project_oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# 1. ART3MIS SCRIPT
ART3MIS_GD = """
extends CharacterBody3D

@onready var key_mesh: MeshInstance3D = $KeyMesh
@onready var dialogue_label: Label3D = $DialogueLabel
@onready var body_mesh: MeshInstance3D = $BodyMesh

var anim_controller: RPMAnimator
var time_passed: float = 0.0

func _ready() -> void:
	$InteractionArea.body_entered.connect(_on_body_entered)
	$InteractionArea.body_exited.connect(_on_body_exited)
	dialogue_label.text = "ART3MIS: 'La Clé de Jade t'attend...'"
	
	anim_controller = RPMAnimator.new()
	anim_controller.target_avatar_node = body_mesh
	add_child(anim_controller)

func _process(delta: float) -> void:
	time_passed += delta
	if key_mesh:
		key_mesh.rotation.y += delta * 2.5
		key_mesh.position.y = 2.4 + sin(time_passed * 3.5) * 0.1

func _on_body_entered(body: Node3D) -> void:
	if body.is_in_group("player"):
		dialogue_label.text = "ART3MIS: 'Salut Gunter! La Clé de Jade est cachée dans le portail 05!'"
		if anim_controller:
			anim_controller.set_state(RPMAnimator.AnimState.WAVE)

func _on_body_exited(body: Node3D) -> void:
	if body.is_in_group("player"):
		dialogue_label.text = "ART3MIS: 'La Clé de Jade t'attend...'"
		if anim_controller:
			anim_controller.set_state(RPMAnimator.AnimState.IDLE)
"""

# 2. ART3MIS TSCN
ART3MIS_TSCN = """
[gd_scene load_steps=9 format=3 uid="uid://art3mis_npc_scene"]

[ext_resource type="Script" path="res://scripts/characters/art3mis_npc.gd" id="1_script"]

[sub_resource type="StandardMaterial3D" id="Mat_Art3misBody"]
albedo_color = Color(0.8, 0.1, 0.4, 1)
roughness = 0.3

[sub_resource type="CapsuleMesh" id="Mesh_Body"]
material = SubResource("Mat_Art3misBody")
radius = 0.35
height = 1.75

[sub_resource type="StandardMaterial3D" id="Mat_Visor"]
albedo_color = Color(1.0, 0.0, 0.5, 1)
emission_enabled = true
emission = Color(1.0, 0.0, 0.5, 1)
emission_energy_multiplier = 4.0

[sub_resource type="BoxMesh" id="Mesh_Visor"]
material = SubResource("Mat_Visor")
size = Vector3(0.45, 0.12, 0.18)

[sub_resource type="StandardMaterial3D" id="Mat_JadeKey"]
albedo_color = Color(0.1, 0.9, 0.4, 1)
metallic = 0.5
roughness = 0.1
emission_enabled = true
emission = Color(0.1, 0.9, 0.4, 1)
emission_energy_multiplier = 3.0

[sub_resource type="BoxMesh" id="Mesh_JadeKey"]
material = SubResource("Mat_JadeKey")
size = Vector3(0.25, 0.25, 0.25)

[sub_resource type="CylinderShape3D" id="Shape_Interact"]
height = 3.0
radius = 4.0

[node name="Art3misNPC" type="CharacterBody3D"]
script = ExtResource("1_script")

[node name="BodyMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0.875, 0)
mesh = SubResource("Mesh_Body")

[node name="VisorMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.45, -0.28)
mesh = SubResource("Mesh_Visor")

[node name="KeyMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.4, 0)
mesh = SubResource("Mesh_JadeKey")

[node name="NameTag" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.0, 0)
pixel_size = 0.015
text = "ART3MIS (Sixer Hunter)"
font_size = 36
outline_size = 8

[node name="DialogueLabel" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.8, 0)
pixel_size = 0.015
text = "ART3MIS: 'La Clé de Jade t'attend...'"
font_size = 42
outline_size = 10

[node name="InteractionArea" type="Area3D" parent="."]

[node name="CollisionShape3D" type="CollisionShape3D" parent="InteractionArea"]
shape = SubResource("Shape_Interact")
"""

# 3. AECH SCRIPT
AECH_GD = """
extends CharacterBody3D

@onready var dialogue_label: Label3D = $DialogueLabel
@onready var body_mesh: MeshInstance3D = $BodyMesh

var anim_controller: RPMAnimator
var time_passed: float = 0.0

func _ready() -> void:
	$InteractionArea.body_entered.connect(_on_body_entered)
	$InteractionArea.body_exited.connect(_on_body_exited)
	dialogue_label.text = "AECH: 'Bienvenue au Garage!'"
	
	anim_controller = RPMAnimator.new()
	anim_controller.target_avatar_node = body_mesh
	add_child(anim_controller)

func _on_body_entered(body: Node3D) -> void:
	if body.is_in_group("player"):
		dialogue_label.text = "AECH: 'Hey Gunter! Besoin de réparer ton Iron Giant ou ta DeLorean?'"
		if anim_controller:
			anim_controller.set_state(RPMAnimator.AnimState.WAVE)

func _on_body_exited(body: Node3D) -> void:
	if body.is_in_group("player"):
		dialogue_label.text = "AECH: 'Bienvenue au Garage!'"
		if anim_controller:
			anim_controller.set_state(RPMAnimator.AnimState.IDLE)
"""

# 4. AECH TSCN
AECH_TSCN = """
[gd_scene load_steps=7 format=3 uid="uid://aech_npc_scene"]

[ext_resource type="Script" path="res://scripts/characters/aech_npc.gd" id="1_script"]

[sub_resource type="StandardMaterial3D" id="Mat_AechBody"]
albedo_color = Color(0.2, 0.5, 0.8, 1)
metallic = 0.7
roughness = 0.2

[sub_resource type="BoxMesh" id="Mesh_MechBody"]
material = SubResource("Mat_AechBody")
size = Vector3(1.2, 2.2, 0.9)

[sub_resource type="StandardMaterial3D" id="Mat_AechEye"]
albedo_color = Color(0.0, 0.8, 1.0, 1)
emission_enabled = true
emission = Color(0.0, 0.8, 1.0, 1)
emission_energy_multiplier = 4.0

[sub_resource type="BoxMesh" id="Mesh_Eye"]
material = SubResource("Mat_AechEye")
size = Vector3(0.6, 0.2, 0.1)

[sub_resource type="CylinderShape3D" id="Shape_Interact"]
height = 3.0
radius = 4.5

[node name="AechNPC" type="CharacterBody3D"]
script = ExtResource("1_script")

[node name="BodyMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.1, 0)
mesh = SubResource("Mesh_MechBody")

[node name="EyeMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.8, -0.45)
mesh = SubResource("Mesh_Eye")

[node name="NameTag" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.5, 0)
pixel_size = 0.015
text = "AECH (Master Builder & Warrior)"
font_size = 36
outline_size = 8

[node name="DialogueLabel" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3.2, 0)
pixel_size = 0.015
text = "AECH: 'Bienvenue au Garage!'"
font_size = 42
outline_size = 10

[node name="InteractionArea" type="Area3D" parent="."]

[node name="CollisionShape3D" type="CollisionShape3D" parent="InteractionArea"]
shape = SubResource("Shape_Interact")
"""

write_file(os.path.join(BASE_DIR, "scripts/characters/art3mis_npc.gd"), ART3MIS_GD)
write_file(os.path.join(BASE_DIR, "scenes/characters/art3mis_npc.tscn"), ART3MIS_TSCN)

write_file(os.path.join(BASE_DIR, "scripts/characters/aech_npc.gd"), AECH_GD)
write_file(os.path.join(BASE_DIR, "scenes/characters/aech_npc.tscn"), AECH_TSCN)

print("Art3mis and Aech NPC scenes and scripts created successfully.")
