# Fallback Third-Person Controller for Desktop Testing
# Based on emirthab's architecture, adapted for Ready Player Me Avatars
class_name AvatarThirdPersonController
extends CharacterBody3D

@export var speed: float = 5.0
@export var sprint_speed: float = 8.0
@export var jump_velocity: float = 4.5
var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")

@onready var spring_arm: SpringArm3D = get_node_or_null("SpringArm3D")
@onready var avatar_mesh: Node3D = get_node_or_null("MeshPivot")
@onready var anim_tree: AnimationTree = get_node_or_null("MeshPivot/Avatar_RPM/AnimationTree")

func _ready() -> void:
	print("[TPC] Third-Person Controller initialized for desktop testing.")

func _physics_process(delta: float) -> void:
	# Gravity
	if not is_on_floor():
		velocity.y -= gravity * delta

	# Jump — uses the project's custom "jump" action (Space / Gamepad A)
	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = jump_velocity

	# Movement — uses the project's custom move_* actions (WASD + Gamepad sticks)
	var input_dir := Input.get_vector("move_left", "move_right", "move_forward", "move_backward")

	# Camera-relative movement when SpringArm exists
	var direction := Vector3.ZERO
	if spring_arm:
		direction = (spring_arm.global_transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
	else:
		direction = (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()

	var current_speed := speed
	if direction:
		velocity.x = direction.x * current_speed
		velocity.z = direction.z * current_speed

		# Smooth avatar rotation toward movement direction
		if avatar_mesh:
			var target_rotation := atan2(-direction.x, -direction.z)
			avatar_mesh.rotation.y = lerp_angle(avatar_mesh.rotation.y, target_rotation, 10.0 * delta)
	else:
		velocity.x = move_toward(velocity.x, 0, current_speed)
		velocity.z = move_toward(velocity.z, 0, current_speed)

	# Drive AnimationTree blend position from movement speed
	if anim_tree:
		var move_speed := Vector2(velocity.x, velocity.z).length()
		anim_tree.set("parameters/BlendSpace1D/blend_position", move_speed)

	move_and_slide()
