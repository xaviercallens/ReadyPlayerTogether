extends Node3D

# ==============================================================================
# PROJET OASIS - DeLorean Time Machine with Holographic Construction Shader
# Spawns with a 2-second bottom-to-top neon grid materialization effect!
# Includes Driver Viseme Lip-Sync ("First key is earned, not taken!").
# ==============================================================================

@export var construction_duration: float = 2.0
@onready var body_mesh: MeshInstance3D = $CarMesh/Body
@onready var driver_label: Label3D = $Driver/VisemeLabel

var shader_material: ShaderMaterial
var time_passed: float = 0.0

func _ready() -> void:
	play_construction_effect()

func play_construction_effect() -> void:
	var mat = body_mesh.get_surface_override_material(0)
	if mat and mat is ShaderMaterial:
		shader_material = mat
		shader_material.set_shader_parameter("construction_progress", 0.0)
		var tween = create_tween()
		tween.tween_property(shader_material, "shader_parameter/construction_progress", 1.0, construction_duration)
		print("[DELOREAN] Holographic Construction Shader Sweep Initiated (2s)!")

func _process(delta: float) -> void:
	time_passed += delta
	# Simulated viseme lip-sync pulse for DeLorean driver reciting RPO quote
	var visemes = ["Aah", "Ohh", "Eee", "Mmm", "First key is earned!"]
	driver_label.text = "PARZIVAL: " + visemes[int(time_passed * 3.0) % visemes.size()]