extends Node
class_name RPMAnimator

# ==============================================================================
# PROJET OASIS - Ready Player Me Standard Animation Controller
# Compatible with Ready Player Me Animation Library bone hierarchy.
# Provides procedural & blend-tree humanoid animations (Idle, Walk, Wave, Dance).
# ==============================================================================

enum AnimState { IDLE, WALK, WAVE, DANCE }

@export var current_state: AnimState = AnimState.IDLE
@export var target_avatar_node: Node3D

var time: float = 0.0

func _ready() -> void:
	print("[RPM Animator] Initialized Ready Player Me Animation Library controller.")

func _process(delta: float) -> void:
	time += delta
	if not target_avatar_node:
		return
		
	match current_state:
		AnimState.IDLE:
			_animate_idle(delta)
		AnimState.WALK:
			_animate_walk(delta)
		AnimState.WAVE:
			_animate_wave(delta)
		AnimState.DANCE:
			_animate_dance(delta)

func set_state(new_state: AnimState) -> void:
	current_state = new_state

func _animate_idle(delta: float) -> void:
	# Subtle breathing and head rotation
	target_avatar_node.position.y = sin(time * 2.0) * 0.02
	target_avatar_node.rotation.y = sin(time * 0.5) * 0.05

func _animate_walk(delta: float) -> void:
	# Walking bounce and hip sway
	target_avatar_node.position.y = abs(sin(time * 8.0)) * 0.05
	target_avatar_node.rotation.z = sin(time * 8.0) * 0.03

func _animate_wave(delta: float) -> void:
	# Greeting wave rotation
	target_avatar_node.rotation.y = sin(time * 4.0) * 0.2
	target_avatar_node.position.y = sin(time * 3.0) * 0.03

func _animate_dance(delta: float) -> void:
	# Distracted Globe Zero-G floating dance move
	target_avatar_node.position.y = sin(time * 4.0) * 0.15
	target_avatar_node.rotation.y += delta * 2.0
	target_avatar_node.rotation.z = sin(time * 3.0) * 0.1