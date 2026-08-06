extends XROrigin3D

# ==============================================================================
# PROJET OASIS - VR Player Rig Controller (OpenXR for Meta Quest 3S)
# Designed for Father-Son Pair Programming
# ==============================================================================

@export var move_speed: float = 3.0
@export var turn_speed: float = 1.5

@onready var camera: XRCamera3D = $XRCamera3D
@onready var left_controller: XRController3D = $LeftHandController
@onready var right_controller: XRController3D = $RightHandController

var interface: XRInterface

func _ready() -> void:
	interface = XRServer.find_interface("OpenXR")
	if interface and interface.is_initialized():
		print("[OASIS VR] OpenXR Interface initialized successfully!")
		get_viewport().use_xr = true
	else:
		print("[OASIS VR] Warning: OpenXR interface not initialized. Running in Desktop fallback mode.")

func _process(delta: float) -> void:
	_handle_vr_movement(delta)

func _handle_vr_movement(delta: float) -> void:
	if not left_controller:
		return
	
	# Read thumbstick input vector from left VR controller
	var joystick_vector = left_controller.get_vector2("primary_thumbstick")
	if joystick_vector.length() > 0.1:
		# Calculate forward direction based on headset camera facing angle
		var forward = -camera.global_transform.basis.z
		var right = camera.global_transform.basis.x
		forward.y = 0.0
		right.y = 0.0
		forward = forward.normalized()
		right = right.normalized()
		
		# Move the XROrigin3D base
		var move_dir = (forward * -joystick_vector.y) + (right * joystick_vector.x)
		global_position += move_dir * move_speed * delta
