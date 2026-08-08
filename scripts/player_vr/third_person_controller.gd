extends CharacterBody3D

# ==============================================================================
# PROJET OASIS - Parzival GDQuest 3D Mannequin Controller
# Leverages the official GDQuest 3D Mannequiny skeletal avatar, animations,
# bone-attached Ready Player One VR Visor & Arc Reactor, and DeLorean spawner.
# ==============================================================================

@export var speed: float = 6.0
@export var run_speed: float = 10.5
@export var jump_velocity: float = 5.2
@export var mouse_sensitivity: float = 0.003
@export var joystick_sensitivity: float = 2.5

@onready var spring_arm: SpringArm3D = $SpringArm3D
@onready var camera: Camera3D = $SpringArm3D/Camera3D
@onready var avatar_mesh: Node3D = $MeshPivot

var anim_player: AnimationPlayer = null
var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")
var delorean_scene = preload("res://scenes/vehicles/delorean_car.tscn")
var current_anim: String = ""

func _ready() -> void:
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
	_setup_mannequin_animation()

func _setup_mannequin_animation() -> void:
	if has_node("MeshPivot/MannequinyModel"):
		var mannequin = $MeshPivot/MannequinyModel
		anim_player = mannequin.find_child("AnimationPlayer", true, false) as AnimationPlayer
		if anim_player:
			print("🤖 [GDQUEST MANNEQUIN] Found AnimationPlayer! Playing default 'idle'...")
			_play_anim("idle")

func _play_anim(anim_name: String, custom_speed: float = 1.0) -> void:
	if anim_player == null:
		return
	if current_anim != anim_name:
		if anim_player.has_animation(anim_name):
			current_anim = anim_name
			anim_player.play(anim_name, 0.15, custom_speed)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion and Input.get_mouse_mode() == Input.MOUSE_MODE_CAPTURED:
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
		elif event.keycode == KEY_E:
			_play_anim("fight_punch", 1.2)

func _physics_process(delta: float) -> void:
	# 1. Gamepad Right Stick Camera Orbit Control
	var joy_rx = Input.get_joy_axis(0, JOY_AXIS_RIGHT_X)
	var joy_ry = Input.get_joy_axis(0, JOY_AXIS_RIGHT_Y)
	if abs(joy_rx) > 0.2:
		spring_arm.rotation.y -= joy_rx * joystick_sensitivity * delta
	if abs(joy_ry) > 0.2:
		spring_arm.rotation.x -= joy_ry * joystick_sensitivity * delta
		spring_arm.rotation.x = clamp(spring_arm.rotation.x, deg_to_rad(-60.0), deg_to_rad(30.0))

	# 2. Gamepad Face Buttons
	if Input.is_joy_button_pressed(0, JOY_BUTTON_Y):
		spawn_delorean_with_cinematic_camera()

	# 3. Gravity & Air Animations
	if not is_on_floor():
		velocity.y -= gravity * delta
		_play_anim("air_jump")
	else:
		if (Input.is_action_just_pressed("jump") or Input.is_joy_button_pressed(0, JOY_BUTTON_A)):
			velocity.y = jump_velocity
			_play_anim("air_jump_anticipation")

	# 4. WASD / Left Stick Locomotion
	var input_dir := Input.get_vector("move_left", "move_right", "move_forward", "move_backward")
	var is_sprinting = Input.is_key_pressed(KEY_SHIFT) or Input.is_joy_button_pressed(0, JOY_BUTTON_LEFT_STICK)
	var move_speed = run_speed if is_sprinting else speed
	
	var cam_yaw = spring_arm.rotation.y
	var direction := (Transform3D(Basis(Vector3.UP, cam_yaw), Vector3.ZERO) * Vector3(input_dir.x, 0, input_dir.y)).normalized()
	
	if direction:
		velocity.x = direction.x * move_speed
		velocity.z = direction.z * move_speed
		
		# Smooth lerp_angle avatar rotation towards movement direction
		var target_angle = atan2(-direction.x, -direction.z)
		avatar_mesh.rotation.y = lerp_angle(avatar_mesh.rotation.y, target_angle, 0.2)
		
		if is_on_floor():
			if is_sprinting:
				_play_anim("dash", 1.3)
			else:
				_play_anim("run", 1.0)
	else:
		velocity.x = move_toward(velocity.x, 0, move_speed)
		velocity.z = move_toward(velocity.z, 0, move_speed)
		if is_on_floor() and current_anim != "fight_punch":
			_play_anim("idle", 1.0)

	move_and_slide()

	# Void Safety Teleport Check
	if global_position.y < -5.0:
		global_position = Vector3(0, 1.5, 8.0)
		velocity = Vector3.ZERO
		print("[OASIS Player] Teleported back to ground plaza.")

func spawn_delorean_with_cinematic_camera() -> void:
	var spawn_pos = camera.global_position - (camera.global_transform.basis.z * 4.5)
	spawn_pos.y = max(spawn_pos.y - 1.0, 0.2)
	
	var car = delorean_scene.instantiate()
	get_tree().current_scene.add_child(car)
	car.global_position = spawn_pos
	car.play_construction_effect()
	
	var original_spring_length = spring_arm.spring_length
	var tween = create_tween()
	tween.tween_property(spring_arm, "spring_length", 1.8, 0.4)
	tween.tween_interval(1.5)
	tween.tween_property(spring_arm, "spring_length", original_spring_length, 0.6)
	print("🏎️ [MANNEQUIN PARZIVAL] Materialized DeLorean Time Machine!")