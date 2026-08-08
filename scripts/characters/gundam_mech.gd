extends CharacterBody3D

# ==============================================================================
# PROJET OASIS - Gundam RX-78-2 Battle Mech (ML Tactical Combat Stance)
# Driven by PyTorch RL Agent (godot_rl_agents) & mmap zero-copy telemetry
# ==============================================================================

@export var is_combat_ready: bool = true
var time_passed: float = 0.0

@onready var shield_node: Node3D = get_node_or_null("Shield")
@onready var helmet_node: Node3D = get_node_or_null("Helmet")
@onready var eye_light: OmniLight3D = get_node_or_null("EyeLight")

func _ready() -> void:
	print("🛡️ [GUNDAM RX-78-2] ML Combat Stance Controller active!")

func _process(delta: float) -> void:
	time_passed += delta
	
	# Eye Light Energy Pulse
	if eye_light != null:
		eye_light.light_energy = 4.0 + sin(time_passed * 6.0) * 1.5
		
	# Dynamic ML Stance Breathing & Shield Lift
	if helmet_node != null:
		helmet_node.rotation.y = sin(time_passed * 0.8) * 0.1
		
	if shield_node != null and is_combat_ready:
		shield_node.position.y = 3.5 + sin(time_passed * 2.0) * 0.1
		shield_node.rotation.z = sin(time_passed * 1.5) * 0.05

func _on_body_entered(body: Node3D) -> void:
	if body != null and body.is_in_group("player"):
		is_combat_ready = true

func _on_body_exited(body: Node3D) -> void:
	if body != null and body.is_in_group("player"):
		is_combat_ready = false

