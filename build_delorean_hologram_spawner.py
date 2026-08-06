import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# 1. HOLOGRAPHIC CONSTRUCTION GDSHADER (materials/shaders/construction_hologram.gdshader)
# ==============================================================================
SHADER_CODE = """
shader_type spatial;
render_mode cull_disabled, blend_mix;

uniform float construction_progress : hint_range(0.0, 1.0) = 0.0;
uniform vec4 neon_color : source_color = vec4(0.0, 0.9, 1.0, 1.0);
uniform float grid_frequency = 25.0;

varying vec3 local_vertex;

void vertex() {
	local_vertex = VERTEX;
}

void fragment() {
	// Bottom-to-top sweep on Y-axis (height: -1.0 to 1.5)
	float height_norm = (local_vertex.y + 1.0) / 2.5;
	
	if (height_norm > construction_progress) {
		discard; // Hide unconstructed geometry
	}
	
	// Holographic Neon Grid Pattern
	float grid_x = abs(sin(local_vertex.x * grid_frequency));
	float grid_z = abs(sin(local_vertex.z * grid_frequency));
	float grid_line = step(0.92, max(grid_x, grid_z));
	
	// Frontline edge scan effect
	float edge = smoothstep(construction_progress - 0.08, construction_progress, height_norm);
	
	ALBEDO = mix(vec3(0.1, 0.15, 0.25), neon_color.rgb, edge + grid_line * 0.5);
	METALLIC = 0.8;
	ROUGHNESS = 0.2;
	EMISSION = neon_color.rgb * (edge * 4.0 + grid_line * 2.0);
	ALPHA = mix(0.95, 1.0, edge);
}
"""

write_file(os.path.join(BASE_DIR, "materials/shaders/construction_hologram.gdshader"), SHADER_CODE)

# ==============================================================================
# 2. DELOREAN CAR GDSCRIPT WITH MATERIALIZATION TWEEN & LIP-SYNC (scripts/vehicles/delorean_car.gd)
# ==============================================================================
DELOREAN_GD = """
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
"""

write_file(os.path.join(BASE_DIR, "scripts/vehicles/delorean_car.gd"), DELOREAN_GD)

# ==============================================================================
# 3. UPDATE PLAYER SPAWNER SCRIPT (scripts/player_vr/pc_player.gd)
# ==============================================================================
PC_PLAYER_GD = """
extends CharacterBody3D

@export var speed: float = 6.0
@export var jump_velocity: float = 4.5

var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")
var delorean_scene = preload("res://scenes/vehicles/delorean_car.tscn")

func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity.y -= gravity * delta

	if Input.is_action_just_pressed("ui_accept") and is_on_floor():
		velocity.y = jump_velocity

	var input_dir := Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	var direction := (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
	if direction:
		velocity.x = direction.x * speed
		velocity.z = direction.z * speed
	else:
		velocity.x = move_toward(velocity.x, 0, speed)
		velocity.z = move_toward(velocity.z, 0, speed)

	move_and_slide()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_F:
			spawn_delorean_in_front()

func spawn_delorean_in_front() -> void:
	var camera = $Camera3D
	var spawn_pos = camera.global_position - (camera.global_transform.basis.z * 4.0)
	spawn_pos.y -= 1.0
	
	var car = delorean_scene.instantiate()
	get_tree().current_scene.add_child(car)
	car.global_position = spawn_pos
	print("🏎️ [SPAWNER] DeLorean Materialized 4m in front of Player (Key: F)!")
"""

write_file(os.path.join(BASE_DIR, "scripts/player_vr/pc_player.gd"), PC_PLAYER_GD)

print("Holographic Construction Shader, DeLorean Spawner (Key F), and Driver Viseme Lip-Sync generated successfully!")
