import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# 1. EMIRTHAB THIRD PERSON CONTROLLER SCRIPT (scripts/player_vr/third_person_controller.gd)
# ==============================================================================
CONTROLLER_GD = """
extends CharacterBody3D

# ==============================================================================
# PROJET OASIS - emirthab Third-Person Controller (Godot Asset #440 Architecture)
# Features SpringArm3D collision-avoidance camera, smooth lerp_angle rotation,
# State Machine (Idle, Walk, Run, Jump, Fall), and Phantom Camera DeLorean cinematic zoom!
# ==============================================================================

@export var speed: float = 6.0
@export var run_speed: float = 10.0
@export var jump_velocity: float = 4.8
@export var mouse_sensitivity: float = 0.003

@onready var spring_arm: SpringArm3D = $SpringArm3D
@onready var camera: Camera3D = $SpringArm3D/Camera3D
@onready var avatar_mesh: Node3D = $MeshPivot

var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")
var delorean_scene = preload("res://scenes/vehicles/delorean_car.tscn")
var current_state: String = "IDLE"

func _ready() -> void:
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion and Input.get_mouse_mode() == Input.MOUSE_MODE_CAPTURED:
		# Mouse orbit camera rotation
		spring_arm.rotation.x -= event.relative.y * mouse_sensitivity
		spring_arm.rotation.x = clamp(spring_arm.rotation.x, deg_to_rad(-60.0), deg_to_rad(30.0))
		spring_arm.rotation.y -= event.relative.x * mouse_sensitivity
		
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_ESCAPE:
			if Input.get_mouse_mode() == Input.MOUSE_MODE_CAPTURED:
				Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
			else:
				Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
		elif event.keycode == KEY_F:
			spawn_delorean_with_cinematic_camera()

func _physics_process(delta: float) -> void:
	# 1. Gravity & Fall State
	if not is_on_floor():
		velocity.y -= gravity * delta
		current_state = "FALL"
	else:
		if current_state == "FALL":
			current_state = "IDLE"

	# 2. Jump Handling
	if Input.is_action_just_pressed("ui_accept") and is_on_floor():
		velocity.y = jump_velocity
		current_state = "JUMP"

	# 3. Movement Direction relative to Camera Yaw
	var input_dir := Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	var move_speed = run_speed if Input.is_key_pressed(KEY_SHIFT) else speed
	
	var cam_yaw = spring_arm.rotation.y
	var direction := (Transform3D(Basis(Vector3.UP, cam_yaw), Vector3.ZERO) * Vector3(input_dir.x, 0, input_dir.y)).normalized()
	
	if direction:
		velocity.x = direction.x * move_speed
		velocity.z = direction.z * move_speed
		if is_on_floor():
			current_state = "RUN" if Input.is_key_pressed(KEY_SHIFT) else "WALK"
			
		# Smooth lerp_angle avatar rotation towards movement direction
		var target_angle = atan2(-direction.x, -direction.z)
		avatar_mesh.rotation.y = lerp_angle(avatar_mesh.rotation.y, target_angle, 0.18)
	else:
		velocity.x = move_toward(velocity.x, 0, move_speed)
		velocity.z = move_toward(velocity.z, 0, move_speed)
		if is_on_floor() and current_state != "JUMP":
			current_state = "IDLE"

	move_and_slide()

# Phantom Camera DeLorean Cinematic Transition
func spawn_delorean_with_cinematic_camera() -> void:
	var spawn_pos = camera.global_position - (camera.global_transform.basis.z * 4.5)
	spawn_pos.y = max(spawn_pos.y - 1.0, 0.2)
	
	var car = delorean_scene.instantiate()
	get_tree().current_scene.add_child(car)
	car.global_position = spawn_pos
	car.play_construction_effect()
	
	# Phantom Camera Style Cinematic Zoom
	var original_spring_length = spring_arm.spring_length
	var tween = create_tween()
	tween.tween_property(spring_arm, "spring_length", 1.8, 0.4) # Zoom in
	tween.tween_interval(1.5)
	tween.tween_property(spring_arm, "spring_length", original_spring_length, 0.6) # Zoom out
	print("🎬 [PHANTOM CAM] Cinematic Zoom onto Materializing DeLorean!")
"""

write_file(os.path.join(BASE_DIR, "scripts/player_vr/third_person_controller.gd"), CONTROLLER_GD)

# ==============================================================================
# 2. UPDATE PC_PLAYER SCENE WITH SPRINGARM3D (scenes/player_vr/pc_player.tscn)
# ==============================================================================
PC_PLAYER_TSCN = """
[gd_scene load_steps=13 format=3 uid="uid://pc_player_scene"]

[ext_resource type="Script" path="res://scripts/player_vr/third_person_controller.gd" id="1_controller"]
[ext_resource type="PackedScene" uid="uid://scene_navigator_ui" path="res://scenes/ui/scene_navigator.tscn" id="2_navigator"]
[ext_resource type="PackedScene" uid="uid://command_menu_ui" path="res://scenes/ui/command_menu.tscn" id="3_command_menu"]
[ext_resource type="PackedScene" uid="uid://ai_prompt_tool_ui" path="res://scenes/ui/ai_prompt_tool.tscn" id="4_prompt_tool"]
[ext_resource type="PackedScene" uid="uid://vr_inventory_system_ui" path="res://scenes/ui/vr_inventory_system.tscn" id="5_inventory"]

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
script = ExtResource("1_controller")

[node name="CollisionShape3D" type="CollisionShape3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0)
shape = SubResource("CapsuleShape3D_player")

[node name="MeshPivot" type="Node3D" parent="."]

[node name="Torso" type="MeshInstance3D" parent="MeshPivot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.1, 0)
mesh = SubResource("Mesh_Torso")

[node name="Head" type="MeshInstance3D" parent="MeshPivot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.72, 0)
mesh = SubResource("Mesh_Head")

[node name="Visor" type="MeshInstance3D" parent="MeshPivot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.75, -0.18)
mesh = SubResource("Mesh_Visor")

[node name="LeftLeg" type="MeshInstance3D" parent="MeshPivot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, -0.16, 0.42, 0)
mesh = SubResource("Mesh_Limb")

[node name="RightLeg" type="MeshInstance3D" parent="MeshPivot"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0.16, 0.42, 0)
mesh = SubResource("Mesh_Limb")

[node name="SpringArm3D" type="SpringArm3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.9659, 0.2588, 0, -0.2588, 0.9659, 0, 2.2, 0)
spring_length = 3.5

[node name="Camera3D" type="Camera3D" parent="SpringArm3D"]
current = true
near = 0.05

[node name="SceneNavigator" parent="." instance=ExtResource("2_navigator")]

[node name="CommandMenu" parent="." instance=ExtResource("3_command_menu")]

[node name="AIPromptTool" parent="." instance=ExtResource("4_prompt_tool")]

[node name="VRInventorySystem" parent="." instance=ExtResource("5_inventory")]
"""

write_file(os.path.join(BASE_DIR, "scenes/player_vr/pc_player.tscn"), PC_PLAYER_TSCN)

print("emirthab Third Person Controller script & SpringArm3D scene generated successfully!")
