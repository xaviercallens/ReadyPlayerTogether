import os
import math

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# 1. UPGRADED PC & GAMEPAD PLAYER SCRIPT (pc_player.gd)
# ==============================================================================
PC_PLAYER_GD = """
extends CharacterBody3D

# ==============================================================================
# PROJET OASIS - Dual Input PC & Gamepad Player Controller
# Supports Keyboard/Mouse + Xbox/PlayStation/Meta Quest Controllers
# ==============================================================================

const SPEED = 6.0
const JUMP_VELOCITY = 5.0
const MOUSE_SENSITIVITY = 0.002
const JOYPAD_SENSITIVITY = 2.5

@onready var camera: Camera3D = $Camera3D

var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")

func _ready() -> void:
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func _input(event: InputEvent) -> void:
	if event is InputEventMouseMotion and Input.get_mouse_mode() == Input.MOUSE_MODE_CAPTURED:
		rotate_y(-event.relative.x * MOUSE_SENSITIVITY)
		camera.rotate_x(-event.relative.y * MOUSE_SENSITIVITY)
		camera.rotation.x = clamp(camera.rotation.x, -PI/2, PI/2)
		
	if event.is_action_pressed("ui_cancel"):
		Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
		
	if event is InputEventMouseButton and event.pressed:
		Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func _physics_process(delta: float) -> void:
	# Apply Gravity
	if not is_on_floor():
		velocity.y -= gravity * delta

	# Handle Jump (Keyboard Space or Gamepad Button 0 / A / Cross)
	if (Input.is_action_just_pressed("ui_accept") or Input.is_action_just_pressed("jump")) and is_on_floor():
		velocity.y = JUMP_VELOCITY

	# Handle Gamepad Right Stick Camera Look
	var joy_look = Vector2(
		Input.get_joy_axis(0, JOY_AXIS_RIGHT_X),
		Input.get_joy_axis(0, JOY_AXIS_RIGHT_Y)
	)
	if joy_look.length() > 0.2:
		rotate_y(-joy_look.x * JOYPAD_SENSITIVITY * delta)
		camera.rotate_x(-joy_look.y * JOYPAD_SENSITIVITY * delta)
		camera.rotation.x = clamp(camera.rotation.x, -PI/2, PI/2)

	# Movement direction (WASD / Arrow Keys / Gamepad Left Stick / D-Pad)
	var input_dir = Vector2.ZERO
	if Input.is_action_pressed("move_forward"): input_dir.y -= 1
	if Input.is_action_pressed("move_backward"): input_dir.y += 1
	if Input.is_action_pressed("move_left"): input_dir.x -= 1
	if Input.is_action_pressed("move_right"): input_dir.x += 1
	
	# Also query raw Gamepad Left Stick if set
	var joy_move = Vector2(
		Input.get_joy_axis(0, JOY_AXIS_LEFT_X),
		Input.get_joy_axis(0, JOY_AXIS_LEFT_Y)
	)
	if joy_move.length() > 0.2:
		input_dir = joy_move

	var direction = (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
	if direction:
		velocity.x = direction.x * SPEED
		velocity.z = direction.z * SPEED
	else:
		velocity.x = move_toward(velocity.x, 0, SPEED)
		velocity.z = move_toward(velocity.z, 0, SPEED)

	move_and_slide()
"""

write_file(os.path.join(BASE_DIR, "scripts/player_vr/pc_player.gd"), PC_PLAYER_GD)

# ==============================================================================
# 2. UPGRADED HUB SCRIPT WITH INSTANT TELEPORT (KEYS 1-9, 0) (oasis_hub.gd)
# ==============================================================================
HUB_GD = """
extends Node3D

# ==============================================================================
# PROJET OASIS - Cyberpunk Hub Central Controller
# Supports Portal Area3D Teleport + Direct Keyboard Teleport (Keys 1-9 & 0)
# ==============================================================================

const DEMO_SCENES = [
	"res://scenes/demos/scene_01_the_stacks.tscn",
	"res://scenes/demos/scene_02_hallidays_journal.tscn",
	"res://scenes/demos/scene_03_copper_race.tscn",
	"res://scenes/demos/scene_04_distracted_globe.tscn",
	"res://scenes/demos/scene_05_arcade_retro.tscn",
	"res://scenes/demos/scene_06_planet_doom.tscn",
	"res://scenes/demos/scene_07_overlook_hotel.tscn",
	"res://scenes/demos/scene_08_ioi_citadel.tscn",
	"res://scenes/demos/scene_09_crystal_castle.tscn",
	"res://scenes/demos/scene_10_easter_egg.tscn"
]

func _ready() -> void:
	print("[OASIS HUB] Cyberpunk Hub active. Press 1-9 or 0 to Teleport instantly!")
	_connect_portals()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_1: _teleport_to_demo(1)
			KEY_2: _teleport_to_demo(2)
			KEY_3: _teleport_to_demo(3)
			KEY_4: _teleport_to_demo(4)
			KEY_5: _teleport_to_demo(5)
			KEY_6: _teleport_to_demo(6)
			KEY_7: _teleport_to_demo(7)
			KEY_8: _teleport_to_demo(8)
			KEY_9: _teleport_to_demo(9)
			KEY_0: _teleport_to_demo(10)

func _connect_portals() -> void:
	for i in range(1, 11):
		var portal_name = "Portal_%02d" % i
		var portal_node = get_node_or_null("Portals/" + portal_name)
		if portal_node:
			portal_node.body_entered.connect(_on_portal_entered.bind(i))

func _on_portal_entered(body: Node3D, demo_index: int) -> void:
	if body.is_in_group("player"):
		_teleport_to_demo(demo_index)

func _teleport_to_demo(demo_index: int) -> void:
	if demo_index >= 1 and demo_index <= DEMO_SCENES.size():
		print("[OASIS HUB] Teleporting to Demo %02d..." % demo_index)
		get_tree().change_scene_to_file(DEMO_SCENES[demo_index - 1])
"""

write_file(os.path.join(BASE_DIR, "scripts/hub/oasis_hub.gd"), HUB_GD)

# ==============================================================================
# 3. UPGRADED HUB SCENE WITH BILLBOARD LABELS & HUD (oasis_hub.tscn)
# ==============================================================================
HUB_TSCN_HEADER = """
[gd_scene load_steps=12 format=3 uid="uid://oasis_hub_cyberpunk"]

[ext_resource type="Script" path="res://scripts/hub/oasis_hub.gd" id="1_hub_script"]
[ext_resource type="PackedScene" uid="uid://pc_player_scene" path="res://scenes/player_vr/pc_player.tscn" id="2_player"]
[ext_resource type="PackedScene" uid="uid://parzival_npc_scene" path="res://scenes/characters/parzival_npc.tscn" id="3_parzival"]
[ext_resource type="PackedScene" uid="uid://art3mis_npc_scene" path="res://scenes/characters/art3mis_npc.tscn" id="4_art3mis"]
[ext_resource type="PackedScene" uid="uid://aech_npc_scene" path="res://scenes/characters/aech_npc.tscn" id="5_aech"]

[sub_resource type="Environment" id="Environment_cyberpunk"]
background_mode = 1
background_color = Color(0.02, 0.01, 0.05, 1)
glow_enabled = true
glow_intensity = 2.5
glow_bloom = 0.6
glow_blend_mode = 0
volumetric_fog_enabled = true
volumetric_fog_density = 0.015
volumetric_fog_albedo = Color(0.0, 0.7, 1.0, 1)
ssr_enabled = true

[sub_resource type="StandardMaterial3D" id="Mat_Floor"]
albedo_color = Color(0.05, 0.05, 0.08, 1)
metallic = 0.85
roughness = 0.15

[sub_resource type="CylinderMesh" id="Mesh_Floor"]
material = SubResource("Mat_Floor")
top_radius = 20.0
bottom_radius = 20.0
height = 0.5

[sub_resource type="StandardMaterial3D" id="Mat_Portal"]
albedo_color = Color(0.0, 1.0, 0.8, 1)
emission_enabled = true
emission = Color(0.0, 1.0, 0.8, 1)
emission_energy_multiplier = 4.0

[sub_resource type="TorusMesh" id="Mesh_Portal"]
material = SubResource("Mat_Portal")
inner_radius = 1.8
outer_radius = 2.2

[sub_resource type="CylinderShape3D" id="Shape_Portal"]
height = 3.0
radius = 2.0

[sub_resource type="BoxShape3D" id="Shape_Floor"]
size = Vector3(40, 0.5, 40)

[node name="OasisHub" type="Node3D"]
script = ExtResource("1_hub_script")

[node name="WorldEnvironment" type="WorldEnvironment" parent="."]
environment = SubResource("Environment_cyberpunk")

[node name="DirectionalLight3D" type="DirectionalLight3D" parent="."]
transform = Transform3D(0.866025, -0.353553, 0.353553, 0, 0.707107, 0.707107, -0.5, -0.612372, 0.612372, 0, 15, 0)
light_color = Color(0.4, 0.8, 1.0, 1)
light_energy = 1.5
shadow_enabled = true

[node name="CentralPlatform" type="StaticBody3D" parent="."]

[node name="MeshInstance3D" type="MeshInstance3D" parent="CentralPlatform"]
mesh = SubResource("Mesh_Floor")

[node name="CollisionShape3D" type="CollisionShape3D" parent="CentralPlatform"]
shape = SubResource("Shape_Floor")

[node name="PCPlayer" parent="." instance=ExtResource("2_player")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0)

[node name="ParzivalNPC" parent="." instance=ExtResource("3_parzival")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 3, 0.2, -4)

[node name="Art3misNPC" parent="." instance=ExtResource("4_art3mis")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 5, 0.2, -4)

[node name="AechNPC" parent="." instance=ExtResource("5_aech")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -4, 0.2, -4)

[node name="HubTitle" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 6, -10)
billboard = 1
pixel_size = 0.02
text = "WELCOME TO THE OASIS
[Keys 1-9, 0] Teleport Instantly | [Gamepad / Mouse] Look"
font_size = 64
outline_size = 16

[node name="Portals" type="Node3D" parent="."]
"""

portal_names = [
	"01: The Stacks [Press 1]", "02: Halliday's Journal [Press 2]", "03: Copper Race [Press 3]",
	"04: Distracted Globe [Press 4]", "05: Retro Arcade [Press 5]", "06: Planet Doom [Press 6]",
	"07: Overlook Hotel [Press 7]", "08: IOI Citadel [Press 8]", "09: Crystal Castle [Press 9]", "10: Easter Egg [Press 0]"
]

portals_tscn = ""
for i in range(1, 11):
	angle = (i - 1) * (2 * math.pi / 10)
	radius = 14.0
	x = math.cos(angle) * radius
	z = math.sin(angle) * radius
	rot_y = -angle + math.pi/2
	
	portals_tscn += f"""
[node name="Portal_{i:02d}" type="Area3D" parent="Portals"]
transform = Transform3D({math.cos(rot_y):.4f}, 0, {math.sin(rot_y):.4f}, 0, 1, 0, {-math.sin(rot_y):.4f}, 0, {math.cos(rot_y):.4f}, {x:.2f}, 2.0, {z:.2f})

[node name="MeshInstance3D" type="MeshInstance3D" parent="Portals/Portal_{i:02d}"]
transform = Transform3D(1, 0, 0, 0, -4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 0, 0)
mesh = SubResource("Mesh_Portal")

[node name="CollisionShape3D" type="CollisionShape3D" parent="Portals/Portal_{i:02d}"]
shape = SubResource("Shape_Portal")

[node name="Label3D" type="Label3D" parent="Portals/Portal_{i:02d}"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.5, 0)
billboard = 1
pixel_size = 0.015
text = "{portal_names[i-1]}"
font_size = 48
outline_size = 10
"""

write_file(os.path.join(BASE_DIR, "scenes/hub/oasis_hub.tscn"), HUB_TSCN_HEADER + portals_tscn)

# ==============================================================================
# 4. ENHANCED 10 DEMO SCENES WITH BILLBOARD LABELS & RETURN SCRIPT
# ==============================================================================
DEMO_RETURN_GD = """
extends Node3D

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_H or event.keycode == KEY_BACKSPACE:
			print("[OASIS DEMO] Returning to Cyberpunk HUB...")
			get_tree().change_scene_to_file("res://scenes/hub/oasis_hub.tscn")
			
	if event is InputEventJoypadButton and event.pressed:
		if event.button_index == JOY_BUTTON_START or event.button_index == JOY_BUTTON_BACK:
			get_tree().change_scene_to_file("res://scenes/hub/oasis_hub.tscn")
"""
write_file(os.path.join(BASE_DIR, "scripts/demos/demo_return.gd"), DEMO_RETURN_GD)

DEMOS = [
	("01_the_stacks", "Les Piles (Trailer Park)", "0.15, 0.1, 0.05", "0.8, 0.5, 0.2", True),
	("02_hallidays_journal", "Archives de Halliday", "0.85, 0.9, 1.0", "1.0, 1.0, 1.0", False),
	("03_copper_race", "Course de New York", "0.05, 0.05, 0.25", "0.0, 1.0, 0.9", True),
	("04_distracted_globe", "Le Globe Distrait (Club 0G)", "0.08, 0.0, 0.15", "1.0, 0.0, 0.8", True),
	("05_arcade_retro", "Garage de Aech", "0.08, 0.12, 0.08", "0.0, 1.0, 0.4", False),
	("06_planet_doom", "Planète Doom", "0.15, 0.02, 0.02", "1.0, 0.15, 0.0", True),
	("07_overlook_hotel", "Hôtel Overlook (Shining)", "0.18, 0.12, 0.08", "0.9, 0.7, 0.4", False),
	("08_ioi_citadel", "Citadelle IOI", "0.7, 0.85, 1.0", "0.4, 0.8, 1.0", True),
	("09_crystal_castle", "Château de Cristal", "0.3, 0.6, 0.95", "0.7, 0.9, 1.0", True),
	("10_easter_egg", "Salle de l'Easter Egg", "0.0, 0.0, 0.0", "1.0, 0.85, 0.0", True)
]

for demo_id, demo_name, bg_color, glow_color, fog in DEMOS:
	scene_str = f"""
[gd_scene load_steps=6 format=3 uid="uid://demo_{demo_id}"]

[ext_resource type="PackedScene" uid="uid://pc_player_scene" path="res://scenes/player_vr/pc_player.tscn" id="1_player"]
[ext_resource type="Script" path="res://scripts/demos/demo_return.gd" id="2_return_script"]

[sub_resource type="Environment" id="Environment_{demo_id}"]
background_mode = 1
background_color = Color({bg_color}, 1)
glow_enabled = true
glow_intensity = 2.5
glow_bloom = 0.6
glow_blend_mode = 0
volumetric_fog_enabled = {"true" if fog else "false"}
volumetric_fog_density = 0.02
volumetric_fog_albedo = Color({glow_color}, 1)
ssr_enabled = true

[sub_resource type="StandardMaterial3D" id="Mat_{demo_id}"]
albedo_color = Color({bg_color}, 1)
roughness = 0.2

[sub_resource type="PlaneMesh" id="Plane_{demo_id}"]
material = SubResource("Mat_{demo_id}")
size = Vector2(60, 60)

[node name="{demo_name.replace(' ', '').replace('(', '').replace(')', '')}" type="Node3D"]
script = ExtResource("2_return_script")

[node name="WorldEnvironment" type="WorldEnvironment" parent="."]
environment = SubResource("Environment_{demo_id}")

[node name="DirectionalLight3D" type="DirectionalLight3D" parent="."]
transform = Transform3D(0.866025, -0.353553, 0.353553, 0, 0.707107, 0.707107, -0.5, -0.612372, 0.612372, 0, 10, 0)
light_color = Color({glow_color}, 1)
shadow_enabled = true

[node name="Floor" type="MeshInstance3D" parent="."]
mesh = SubResource("Plane_{demo_id}")

[node name="Label3D" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 3.5, -6)
billboard = 1
pixel_size = 0.02
text = "OASIS DEMO: {demo_name}
[Press H or Gamepad Start to Return to HUB]"
font_size = 54
outline_size = 12

[node name="PCPlayer" parent="." instance=ExtResource("1_player")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 2)
"""
	write_file(os.path.join(BASE_DIR, f"scenes/demos/scene_{demo_id}.tscn"), scene_str)

# ==============================================================================
# 5. INPUT MAP IN PROJECT.GODOT (ADD JUMP AND GAMEPAD SUPPORT)
# ==============================================================================
PROJECT_GODOT_CONTENT = """
; Engine configuration file for Projet OASIS VR
; OpenXR Enabled for Meta Quest 3S / Quest Link / Standalone

config_version=5

[application]

config/name="Projet OASIS VR"
config/description="Ready Player One inspired VR game for Meta Quest 3S built with Father-Son pair programming."
run/main_scene="res://scenes/hub/oasis_hub.tscn"
config/features=PackedStringArray("4.2", "Forward Plus")

[xr]

openxr/enabled=true
openxr/reference_space=2
shaders/enabled=true

[rendering]

renderer/rendering_method="forward_plus"
textures/vram_compression/import_etc2_astc=true
environment/defaults/default_clear_color=Color(0.05, 0.02, 0.1, 1)

[input]

move_forward={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":87,"key_label":0,"unicode":119,"echo":false,"script":null), Object(InputEventJoypadMotion,"device":-1,"axis":1,"axis_value":-1.0,"script":null)
]
}
move_backward={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":83,"key_label":0,"unicode":115,"echo":false,"script":null), Object(InputEventJoypadMotion,"device":-1,"axis":1,"axis_value":1.0,"script":null)
]
}
move_left={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":65,"key_label":0,"unicode":97,"echo":false,"script":null), Object(InputEventJoypadMotion,"device":-1,"axis":0,"axis_value":-1.0,"script":null)
]
}
move_right={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":68,"key_label":0,"unicode":100,"echo":false,"script":null), Object(InputEventJoypadMotion,"device":-1,"axis":0,"axis_value":1.0,"script":null)
]
}
jump={
"deadzone": 0.5,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":32,"key_label":0,"unicode":32,"echo":false,"script":null), Object(InputEventJoypadButton,"device":-1,"button_index":0,"pressure":0.0,"pressed":false,"script":null)
]
}
"""

write_file(os.path.join(BASE_DIR, "project.godot"), PROJECT_GODOT_CONTENT)

print("Gamepads, Billboard titles, Direct Teleport (1-9), and Demo Return system applied successfully!")
