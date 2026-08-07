# Godot 4.3+ Procedural Generation with WorkerThreadPool (Inspired by gdquest-demos)
# Offloads procedural mesh and terrain creation to background threads to prevent VR frame stuttering.
class_name ProceduralWorldWorker
extends Node3D

signal chunk_generated(chunk_position: Vector3, mesh_instance: MeshInstance3D)
signal generation_completed(total_chunks: int)

@export var render_distance: int = 3
@export var chunk_size: float = 20.0
@export var grid_height_scale: float = 5.0

var noise: FastNoiseLite
var generated_chunks: Dictionary = {}
var pending_tasks: Array = []

func _ready() -> void:
	noise = FastNoiseLite.new()
	noise.seed = 1337
	noise.noise_type = FastNoiseLite.TYPE_PERLIN
	noise.frequency = 0.05
	
	print("[ProceduralWorldWorker] Démarrage de la génération arrière-plan VR...")
	generate_world_async()

func generate_world_async() -> void:
	var total = 0
	for x in range(-render_distance, render_distance + 1):
		for z in range(-render_distance, render_distance + 1):
			var chunk_pos = Vector3(x * chunk_size, 0, z * chunk_size)
			total += 1
			# Utiliser WorkerThreadPool de Godot 4 pour ne pas geler l'affichage VR
			var task_id = WorkerThreadPool.add_task(Callable(self, "_build_chunk_thread").bind(chunk_pos))
			pending_tasks.append(task_id)
			
	print("[ProceduralWorldWorker] ", total, " tâches soumises au WorkerThreadPool.")

func _build_chunk_thread(chunk_pos: Vector3) -> void:
	var plane_mesh = PlaneMesh.new()
	plane_mesh.size = Vector2(chunk_size, chunk_size)
	plane_mesh.subdivide_width = 10
	plane_mesh.subdivide_depth = 10
	
	var mesh_inst = MeshInstance3D.new()
	mesh_inst.mesh = plane_mesh
	mesh_inst.position = chunk_pos
	
	# Matériau Synthwave Neon Cyberpunk
	var mat = StandardMaterial3D.new()
	mat.albedo_color = Color(0.05, 0.0, 0.15)
	mat.emission_enabled = true
	mat.emission = Color(0.0, 0.8, 1.0)
	mat.emission_energy_multiplier = 0.5
	mesh_inst.material_override = mat
	
	# Publier sur le thread principal
	call_deferred("_on_chunk_completed", chunk_pos, mesh_inst)

func _on_chunk_completed(chunk_pos: Vector3, mesh_inst: MeshInstance3D) -> void:
	add_child(mesh_inst)
	generated_chunks[chunk_pos] = mesh_inst
	chunk_generated.emit(chunk_pos, mesh_inst)
	
	if generated_chunks.size() >= pending_tasks.size():
		generation_completed.emit(generated_chunks.size())
		print("[ProceduralWorldWorker] Génération du monde infini terminée avec succès!")
