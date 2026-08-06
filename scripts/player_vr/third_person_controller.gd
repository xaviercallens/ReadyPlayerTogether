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