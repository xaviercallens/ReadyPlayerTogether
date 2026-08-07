# Genie Sim GLTF Runtime Importer (The Builder)
# Imports physical .gltf files using threaded loading to prevent VR frame drops.
class_name RuntimeAssetLoader
extends Node3D

signal gltf_loaded(node: Node3D)
signal load_failed(error: String)

var _loading_path: String = ""

func load_genie_sim_environment(file_path: String) -> void:
	print("[RuntimeAssetLoader] Queueing threaded import: ", file_path)
	_loading_path = file_path

	# Use Godot's threaded resource loader to avoid blocking the VR render loop.
	# ResourceLoader works with .tscn/.tres; for raw GLTF we use a WorkerThread.
	var thread := Thread.new()
	thread.start(_threaded_gltf_import.bind(file_path, thread))

func _threaded_gltf_import(file_path: String, thread: Thread) -> void:
	var gltf_doc := GLTFDocument.new()
	var gltf_state := GLTFState.new()

	var error := gltf_doc.append_from_file(file_path, gltf_state)
	if error != OK:
		call_deferred("_on_load_failed", "GLTF read error: " + str(error))
		return

	var generated_node := gltf_doc.generate_scene(gltf_state)
	if generated_node:
		call_deferred("_on_load_success", generated_node)
	else:
		call_deferred("_on_load_failed", "Failed to generate 3D scene from GLTF.")

func _on_load_success(node: Node3D) -> void:
	add_child(node)
	print("[RuntimeAssetLoader] GLTF environment loaded successfully!")
	gltf_loaded.emit(node)

func _on_load_failed(error_msg: String) -> void:
	print("[RuntimeAssetLoader] ERROR: ", error_msg)
	load_failed.emit(error_msg)
