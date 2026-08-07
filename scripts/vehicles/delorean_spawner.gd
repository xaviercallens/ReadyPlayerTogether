# DeLorean Sci-Fi Spawner for Projet OASIS
class_name DeLoreanSpawner
extends Node3D

@export var delorean_scene: PackedScene

func _input(event: InputEvent) -> void:
	# "spawn_car" must be mapped in Project > Input Map (default: F key)
	if event.is_action_pressed("spawn_car"):
		spawn_delorean()

func spawn_delorean() -> void:
	if not delorean_scene:
		print("[DeLoreanSpawner] Error: No DeLorean scene assigned in Inspector!")
		return

	# Lazy-fetch camera to avoid null crash during VR initialization
	var camera := get_viewport().get_camera_3d()
	if camera == null:
		print("[DeLoreanSpawner] Error: No active Camera3D found in viewport.")
		return

	var delorean := delorean_scene.instantiate()
	get_tree().current_scene.add_child(delorean)

	# 3 meters in front of camera, 1 meter lower
	var spawn_position := camera.global_position - (camera.global_transform.basis.z * 3.0)
	spawn_position.y -= 1.0
	delorean.global_position = spawn_position

	# Trigger construction shader sweep if available
	if delorean.has_node("CarMesh"):
		var mesh := delorean.get_node("CarMesh") as MeshInstance3D
		var material := mesh.get_surface_override_material(0)

		if material and material is ShaderMaterial:
			var tween := get_tree().create_tween()
			tween.tween_property(material, "shader_parameter/construction_progress", 1.0, 2.5)
			print("[DeLoreanSpawner] Holographic materialization started...")
	else:
		print("[DeLoreanSpawner] DeLorean placed successfully!")
