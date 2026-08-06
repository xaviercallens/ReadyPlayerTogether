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