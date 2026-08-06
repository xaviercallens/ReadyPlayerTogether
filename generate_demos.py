import os

BASE_DIR = r"C:\Users\Utilisateur\.gemini\antigravity\scratch\project_oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# 1. PC Player
PC_PLAYER_GD = """
extends CharacterBody3D

const SPEED = 5.0
const JUMP_VELOCITY = 4.5
const MOUSE_SENSITIVITY = 0.002

@onready var camera = $Camera3D

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")

func _ready():
    Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func _input(event):
    if event is InputEventMouseMotion:
        rotate_y(-event.relative.x * MOUSE_SENSITIVITY)
        camera.rotate_x(-event.relative.y * MOUSE_SENSITIVITY)
        camera.rotation.x = clamp(camera.rotation.x, -PI/2, PI/2)
    if event.is_action_pressed("ui_cancel"):
        Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)

func _physics_process(delta):
    if not is_on_floor():
        velocity.y -= gravity * delta

    if Input.is_action_just_pressed("ui_accept") and is_on_floor():
        velocity.y = JUMP_VELOCITY

    var input_dir = Vector2.ZERO
    if Input.is_action_pressed("move_forward"): input_dir.y -= 1
    if Input.is_action_pressed("move_backward"): input_dir.y += 1
    if Input.is_action_pressed("move_left"): input_dir.x -= 1
    if Input.is_action_pressed("move_right"): input_dir.x += 1
    
    var direction = (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
    if direction:
        velocity.x = direction.x * SPEED
        velocity.z = direction.z * SPEED
    else:
        velocity.x = move_toward(velocity.x, 0, SPEED)
        velocity.z = move_toward(velocity.z, 0, SPEED)

    move_and_slide()
"""

PC_PLAYER_TSCN = """
[gd_scene load_steps=3 format=3 uid="uid://pc_player_scene"]

[ext_resource type="Script" path="res://scripts/player_vr/pc_player.gd" id="1_pc_script"]

[sub_resource type="CapsuleShape3D" id="CapsuleShape3D_player"]

[node name="PCPlayer" type="CharacterBody3D" groups=["player"]]
script = ExtResource("1_pc_script")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0)
shape = SubResource("CapsuleShape3D_player")

[node name="Camera3D" type="Camera3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.6, 0)
current = true
"""

write_file(os.path.join(BASE_DIR, "scripts/player_vr/pc_player.gd"), PC_PLAYER_GD)
write_file(os.path.join(BASE_DIR, "scenes/player_vr/pc_player.tscn"), PC_PLAYER_TSCN)

# 2. Demo Scenes
DEMOS = [
    ("01_the_stacks", "Les Piles", "0.2, 0.2, 0.2", "0.8, 0.6, 0.2", True),
    ("02_hallidays_journal", "Les Archives de Halliday", "0.9, 0.9, 1.0", "1.0, 1.0, 1.0", False),
    ("03_copper_race", "Course de New York", "0.1, 0.1, 0.3", "0.0, 1.0, 0.8", True),
    ("04_distracted_globe", "Le Globe Distrait", "0.05, 0.0, 0.1", "1.0, 0.0, 1.0", True),
    ("05_arcade_retro", "Garage de Aech", "0.1, 0.1, 0.1", "0.0, 1.0, 0.0", False),
    ("06_planet_doom", "Planete Doom", "0.1, 0.0, 0.0", "1.0, 0.2, 0.0", True),
    ("07_overlook_hotel", "Hotel Overlook", "0.2, 0.1, 0.1", "0.8, 0.7, 0.5", False),
    ("08_ioi_citadel", "Citadelle IOI", "0.8, 0.9, 1.0", "0.5, 0.8, 1.0", True),
    ("09_crystal_castle", "Chateau de Cristal", "0.4, 0.7, 1.0", "0.8, 0.9, 1.0", True),
    ("10_easter_egg", "Easter Egg", "0.0, 0.0, 0.0", "1.0, 0.8, 0.0", True)
]

for demo_id, demo_name, bg_color, glow_color, fog in DEMOS:
    scene_str = f"""
[gd_scene load_steps=5 format=3 uid="uid://demo_{demo_id}"]

[ext_resource type="PackedScene" uid="uid://pc_player_scene" path="res://scenes/player_vr/pc_player.tscn" id="1_player"]

[subresource type="Environment" id="Environment_{demo_id}"]
background_mode = 1
background_color = Color({bg_color}, 1)
glow_enabled = true
glow_intensity = 2.0
glow_bloom = 0.5
glow_blend_mode = 0
volumetric_fog_enabled = {"true" if fog else "false"}
volumetric_fog_density = 0.02
volumetric_fog_albedo = Color({glow_color}, 1)

[subresource type="StandardMaterial3D" id="Mat_{demo_id}"]
albedo_color = Color({bg_color}, 1)
roughness = 0.2

[subresource type="PlaneMesh" id="Plane_{demo_id}"]
material = SubResource("Mat_{demo_id}")
size = Vector2(50, 50)

[node name="{demo_name.replace(' ', '')}" type="Node3D"]

[node name="WorldEnvironment" type="WorldEnvironment" parent="."]
environment = SubResource("Environment_{demo_id}")

[node name="DirectionalLight3D" type="DirectionalLight3D" parent="."]
transform = Transform3D(0.866025, -0.353553, 0.353553, 0, 0.707107, 0.707107, -0.5, -0.612372, 0.612372, 0, 10, 0)
light_color = Color({glow_color}, 1)
shadow_enabled = true

[node name="Floor" type="MeshInstance3D" parent="."]
mesh = SubResource("Plane_{demo_id}")

[node name="Label3D" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3, -5)
pixel_size = 0.02
text = "DEMO: {demo_name}"
font_size = 64
outline_size = 12

[node name="PCPlayer" parent="." instance=ExtResource("1_player")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 2)
"""
    write_file(os.path.join(BASE_DIR, f"scenes/demos/scene_{demo_id}.tscn"), scene_str)

print("Demo scenes generated successfully.")
