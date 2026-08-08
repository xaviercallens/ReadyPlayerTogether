extends CharacterBody3D

# ==============================================================================
# PROJET OASIS - Third Person Controller & Physical Ragdoll Integration
# Handlers desktop controls, camera springarm, and active physical bone ragdolls
# ==============================================================================

@export var speed: float = 6.0
@export var jump_velocity: float = 8.0
@export var gravity: float = 20.0

@onready var mesh_pivot: Node3D = get_node_or_null("Pivot")
@onready var camera_arm: SpringArm3D = get_node_or_null("SpringArm3D")
@onready var skeleton: Skeleton3D = get_node_or_null("Pivot/Skeleton3D")

var is_ragdoll: bool = false

func _ready() -> void:
	add_to_group("player")
	print("🎮 [PLAYER CONTROLLER] Third-person controller active with Physical Bone Ragdoll integration.")

func _physics_process(delta: float) -> void:
	if is_ragdoll:
		return

	# Gravity
	if not is_on_floor():
		velocity.y -= gravity * delta

	# Jump
	if Input.is_action_just_pressed("ui_accept") and is_on_floor():
		velocity.y = jump_velocity

	# Input movement
	var input_dir = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	var direction = Vector3(input_dir.x, 0, input_dir.y).normalized()
	
	if direction != Vector3.ZERO:
		velocity.x = direction.x * speed
		velocity.z = direction.z * speed
		if mesh_pivot != null:
			var target_angle = atan2(-direction.x, -direction.z)
			mesh_pivot.rotation.y = lerp_angle(mesh_pivot.rotation.y, target_angle, 10.0 * delta)
	else:
		velocity.x = move_toward(velocity.x, 0, speed)
		velocity.z = move_toward(velocity.z, 0, speed)

	move_and_slide()

func toggle_ragdoll() -> void:
	if skeleton == null:
		return
	is_ragdoll = !is_ragdoll
	if is_ragdoll:
		skeleton.physical_bones_start_simulation()
		print("🦴 [PLAYER RAGDOLL] Active!")
	else:
		skeleton.physical_bones_stop_simulation()
		print("🦴 [PLAYER RAGDOLL] Stopped.")
