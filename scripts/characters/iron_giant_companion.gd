extends CharacterBody3D

# ==============================================================================
# PROJET OASIS - Aech's Iron Giant (ML Active Ragdoll & Protective Stance)
# Driven by PyTorch RL Agent (godot_rl_agents) & mmap zero-copy telemetry
# ART PASS: SkeletonIK3D Head Tracking + ML Textures
# ==============================================================================

@export var protective_mode: bool = true
var time_passed: float = 0.0

@onready var mech_body: Node3D = get_node_or_null("MechBody")
@onready var eye_light: OmniLight3D = get_node_or_null("EyeLight")

# VR Head Tracking
var head_ik: SkeletonIK3D = null
var vr_player: Node3D = null

func _ready() -> void:
	print("🤖 [IRON GIANT] 'I Am Not A Gun' - ML Protective Stance & Head Tracking active!")
	
	# Find SkeletonIK3D (should be placed on the neck bone)
	head_ik = get_node_or_null("MechBody/Armature/Skeleton3D/HeadIK")
	if head_ik != null:
		head_ik.start()

func _process(delta: float) -> void:
	time_passed += delta
	
	# Subtle breathing & balance sway for the giant mech
	if mech_body != null:
		mech_body.position.y = 4.0 + sin(time_passed * 1.5) * 0.1
		mech_body.rotation.z = sin(time_passed * 1.0) * 0.03
		
	if eye_light != null:
		eye_light.light_energy = 5.0 + sin(time_passed * 4.0) * 1.5 # Increased energy for Art Pass
		
	# Update Head IK target to follow the VR Player
	if head_ik != null:
		if vr_player == null:
			# Auto-find the player or XRCamera3D
			vr_player = get_tree().get_first_node_in_group("player")
			if vr_player == null:
				var cameras = get_tree().get_nodes_in_group("xr_camera")
				if cameras.size() > 0:
					vr_player = cameras[0]
					
		if vr_player != null:
			# Interpolate the IK target towards the player's head for smooth motion
			var target_pos = vr_player.global_position
			var current_target = head_ik.target_node
			if current_target and has_node(current_target):
				var target_node = get_node(current_target)
				target_node.global_position = target_node.global_position.lerp(target_pos, delta * 2.0)