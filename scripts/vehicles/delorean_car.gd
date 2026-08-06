extends Node3D

# ==============================================================================
# PROJET OASIS - DeLorean Time Machine (Null-Safe Construction Shader & Driver Viseme)
# ==============================================================================

@export var construction_duration: float = 2.0
var shader_material: ShaderMaterial
var time_passed: float = 0.0

func _ready() -> void:
	play_construction_effect()

func _get_target_mesh() -> MeshInstance3D:
	if has_node("Body"):
		return get_node("Body") as MeshInstance3D
	elif has_node("CarMesh/Body"):
		return get_node("CarMesh/Body") as MeshInstance3D
	
	var meshes = find_children("*", "MeshInstance3D", true, false)
	if meshes.size() > 0:
		return meshes[0] as MeshInstance3D
	return null

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
	if has_node("Driver/VisemeLabel"):
		var driver_label = get_node("Driver/VisemeLabel") as Label3D
		if driver_label != null:
			var visemes = ["Aah", "Ohh", "Eee", "Mmm", "First key is earned!"]
			driver_label.text = "PARZIVAL: " + visemes[int(time_passed * 3.0) % visemes.size()]