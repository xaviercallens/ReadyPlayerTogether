import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# UPDATED THIRD PERSON CONTROLLER WITH DUAL JOYSTICK & KEYBOARD CONTROLS
# ==============================================================================
CONTROLLER_GD = """
extends CharacterBody3D

# ==============================================================================
# PROJET OASIS - Third-Person Controller (emirthab Asset #440 + Full Joystick Map)
# Uses High-Quality RPO Mannequin Avatar & DeLorean Time Machine Spawner.
# Full Support for Gamepad / Joystick (Sticks, Triggers, Face Buttons).
# ==============================================================================

@export var speed: float = 6.0
@export var run_speed: float = 10.0
@export var jump_velocity: float = 4.8
@export var mouse_sensitivity: float = 0.003
@export var joystick_sensitivity: float = 2.5

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
	# 1. Right Joystick Camera Orbit Control
	var joy_rx = Input.get_joy_axis(0, JOY_AXIS_RIGHT_X)
	var joy_ry = Input.get_joy_axis(0, JOY_AXIS_RIGHT_Y)
	if abs(joy_rx) > 0.2:
		spring_arm.rotation.y -= joy_rx * joystick_sensitivity * delta
	if abs(joy_ry) > 0.2:
		spring_arm.rotation.x -= joy_ry * joystick_sensitivity * delta
		spring_arm.rotation.x = clamp(spring_arm.rotation.x, deg_to_rad(-60.0), deg_to_rad(30.0))

	# 2. Joystick Face Buttons Shortcuts (Y Button = DeLorean Spawn)
	if Input.is_joy_button_pressed(0, JOY_BUTTON_Y):
		spawn_delorean_with_cinematic_camera()

	# 3. Gravity & Fall State
	if not is_on_floor():
		velocity.y -= gravity * delta
		current_state = "FALL"
	else:
		if current_state == "FALL":
			current_state = "IDLE"

	# 4. Jump Handling (Space or Gamepad Button A)
	if (Input.is_action_just_pressed("jump") or Input.is_joy_button_pressed(0, JOY_BUTTON_A)) and is_on_floor():
		velocity.y = jump_velocity
		current_state = "JUMP"

	# 5. Left Joystick / WASD Locomotion
	var input_dir := Input.get_vector("move_left", "move_right", "move_forward", "move_backward")
	var move_speed = run_speed if (Input.is_key_pressed(KEY_SHIFT) or Input.is_joy_button_pressed(0, JOY_BUTTON_LEFT_STICK)) else speed
	
	var cam_yaw = spring_arm.rotation.y
	var direction := (Transform3D(Basis(Vector3.UP, cam_yaw), Vector3.ZERO) * Vector3(input_dir.x, 0, input_dir.y)).normalized()
	
	if direction:
		velocity.x = direction.x * move_speed
		velocity.z = direction.z * move_speed
		if is_on_floor():
			current_state = "RUN" if (Input.is_key_pressed(KEY_SHIFT) or Input.is_joy_button_pressed(0, JOY_BUTTON_LEFT_STICK)) else "WALK"
			
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
	print("🏎️ [JOYSTICK SPAWNER] DeLorean Materialized via Gamepad/Keyboard!")
"""

write_file(os.path.join(BASE_DIR, "scripts/player_vr/third_person_controller.gd"), CONTROLLER_GD)

print("Gamepad / Joystick controls & RPO Mannequin / DeLorean integration updated successfully!")
