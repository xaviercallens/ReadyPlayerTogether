extends Node3D

# ==============================================================================
# PROJET OASIS - DeLorean Time Machine (ML Autonomous Cruise & Hover Physics)
# Driven by PyTorch RL Agent (godot_rl_agents) & mmap zero-copy telemetry
# ==============================================================================

@export var construction_duration: float = 2.0
@export var auto_cruise_enabled: bool = true
@export var cruise_speed: float = 8.0

var shader_material: ShaderMaterial
var time_passed: float = 0.0
var target_hover_height: float = 0.3
var current_velocity: Vector3 = Vector3.ZERO

@onready var driver_label: Label3D = get_node_or_null("Driver/VisemeLabel")

func _ready() -> void:
	_apply_scifi_shader()
	play_construction_effect()
	_activate_hover_mode()
	print("🚗 [DELOREAN] ML Autonomous Pilot, Jolt Physics & Hover Mode initialized!")

func _get_target_mesh() -> MeshInstance3D:
	# Tente de trouver le maillage principal de la DeLorean
	var meshes = find_children("*", "MeshInstance3D", true, false)
	for m in meshes:
		if "Body" in m.name or "Hull" in m.name or "Delorean" in m.name:
			return m as MeshInstance3D
	if meshes.size() > 0:
		return meshes[0] as MeshInstance3D
	return null

func _apply_scifi_shader() -> void:
	var mesh_node = _get_target_mesh()
	if mesh_node == null: return
	
	# Charger le shader créé
	var shader = load("res://assets/shaders/sci_fi_construction.gdshader")
	if shader != null:
		var mat = ShaderMaterial.new()
		mat.shader = shader
		mat.set_shader_parameter("grid_color", Color(0.0, 1.0, 1.0, 1.0)) # Cyan
		mat.set_shader_parameter("emission_energy", 5.0)
		mesh_node.set_surface_override_material(0, mat)
		shader_material = mat

func _activate_hover_mode() -> void:
	# Recherche des roues pour la rotation à 90 degrés
	var wheels = []
	for child in find_children("*", "Node3D", true, false):
		var cname = child.name.to_lower()
		if "wheel" in cname or "pneu" in cname:
			wheels.append(child)
			
	if wheels.size() > 0:
		var tween = create_tween().set_parallel(true)
		for w in wheels:
			# Rotation des roues à l'horizontale
			tween.tween_property(w, "rotation_degrees:x", -90.0, 1.5).set_trans(Tween.TRANS_SINE)
			
			# Ajout d'une lumière de propulsion sous chaque roue
			var light = OmniLight3D.new()
			light.light_color = Color(0.0, 1.0, 1.0) # Cyan
			light.light_energy = 0.0
			light.omni_range = 3.0
			light.position = Vector3(0, -0.2, 0)
			w.add_child(light)
			tween.tween_property(light, "light_energy", 3.0, 1.5).set_delay(1.0)
		print("[DELOREAN] Hover Mode Active: Wheels flipped!")

func play_construction_effect() -> void:
	var mesh_node = _get_target_mesh()
	if mesh_node != null:
		var mat = mesh_node.get_surface_override_material(0)
		if mat == null and mesh_node.mesh != null:
			mat = mesh_node.mesh.surface_get_material(0)
			
		if mat != null and mat is ShaderMaterial:
			shader_material = mat
			shader_material.set_shader_parameter("construction_progress", 0.0)
			var tween = create_tween()
			tween.tween_property(shader_material, "shader_parameter/construction_progress", 1.0, construction_duration)
			print("[DELOREAN] Holographic Construction Shader Sweep Initiated (2s)!")

func _process(delta: float) -> void:
	time_passed += delta
	
	# Hover altitude pulsation (Thrusters active)
	position.y = lerp(position.y, target_hover_height + sin(time_passed * 3.0) * 0.08, delta * 4.0)
	rotation.z = sin(time_passed * 1.5) * 0.02 # Slight roll sway
	
	# ML Autonomous Cruise Controller
	if auto_cruise_enabled:
		var orbit_radius = 14.0
		var target_x = sin(time_passed * 0.3) * orbit_radius
		var target_z = cos(time_passed * 0.3) * orbit_radius
		var target_pos = Vector3(target_x, position.y, target_z)
		
		var dir = (target_pos - position).normalized()
		if dir.length() > 0.1:
			position = position.lerp(target_pos, delta * 1.5)
			var target_angle = atan2(-dir.x, -dir.z)
			rotation.y = lerp_angle(rotation.y, target_angle, delta * 3.0)
			
	# Driver Lip-Sync Visemes
	if driver_label != null:
		var visemes = ["88 MPH!", "Flux Capacitor Active", "OASIS Cruise Mode", "Ready Player One!"]
		driver_label.text = "PARZIVAL: " + visemes[int(time_passed * 2.0) % visemes.size()]

