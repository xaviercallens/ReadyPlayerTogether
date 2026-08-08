extends CharacterBody3D

# ==============================================================================
# PROJET OASIS - Iron Giant Assignment (3D GLB Model via GLTFDocument)
# Protective Guardian with Head Tracking, Light Pulsing, and Hover Effects
# ==============================================================================

@export var hover_height: float = 0.3
@export var hover_speed: float = 2.5
@export var glb_path: String = "res://assets/iron_giant/3d_iron_giant_assignment.glb"
@export var converted_scene_path: String = "res://assets/oasis_mechas/3d_iron_giant_assignment_OASIS.tscn"

@onready var label_name: Label3D = get_node_or_null("NameTag")
@onready var label_dialogue: Label3D = get_node_or_null("DialogueLabel")
@onready var eye_light: OmniLight3D = get_node_or_null("EyeLight")
@onready var mesh_pivot: Node3D = get_node_or_null("MeshPivot")
@onready var model_root: Node3D = get_node_or_null("ModelPivot/ModelRoot")

var time_passed: float = 0.0
var base_y: float = 0.0
var target_player: Node3D = null
var glb_loaded: bool = false

func _ready() -> void:
	base_y = global_position.y
	if has_node("InteractionArea"):
		$InteractionArea.body_entered.connect(_on_body_entered)
		$InteractionArea.body_exited.connect(_on_body_exited)
	
	# Try to load the GLB model dynamically
	_load_glb_model()
	print("🤖 [IRON GIANT ASSIGNMENT] Imported GLB Iron Giant ready - 'I Am Not A Gun!'")

func _load_glb_model() -> void:
	"""Attempt to load the GLB model using GLTFDocument or converted scene."""
	
	# Approach 1: Try loading the pre-converted TSCN scene
	if ResourceLoader.exists(converted_scene_path):
		var scene = load(converted_scene_path)
		if scene != null and scene is PackedScene:
			var instance = scene.instantiate()
			if model_root != null:
				for child in model_root.get_children():
					child.queue_free()
				model_root.add_child(instance)
				glb_loaded = true
				print("✓ GLB model loaded from converted TSCN!")
				return
	
	# Approach 2: Load GLB directly using GLTFDocument (runtime conversion)
	if ResourceLoader.exists(glb_path):
		_load_glb_via_gltf_document(glb_path)
		if glb_loaded:
			return
	
	print("⚠ GLB model not available, using placeholder geometry")

func _load_glb_via_gltf_document(file_path: String) -> void:
	"""Load GLB using GLTFDocument for runtime conversion."""
	var gltf = GLTFDocument.new()
	var state = GLTFState.new()
	
	var err = gltf.append_from_file(file_path, state)
	if err != OK:
		printerr("❌ Failed to load GLB via GLTFDocument: ", file_path)
		return
	
	var root_node = gltf.generate_scene(state)
	if root_node == null:
		printerr("❌ Failed to generate scene from GLB")
		return
	
	if model_root != null:
		for child in model_root.get_children():
			child.queue_free()
		model_root.add_child(root_node)
		glb_loaded = true
		print("✓ GLB model loaded via GLTFDocument!")

func _process(delta: float) -> void:
	time_passed += delta
	
	# Hover floating animation
	if mesh_pivot != null:
		mesh_pivot.position.y = sin(time_passed * hover_speed) * 0.2
	
	# Eye light pulsing
	if eye_light != null:
		eye_light.light_energy = 2.5 + sin(time_passed * 3.0) * 0.8
	
	# Head tracking toward player
	if target_player != null and mesh_pivot != null:
		var dir = (target_player.global_position - global_position).normalized()
		dir.y = 0
		if dir.length() > 0.1:
			var target_rot = atan2(-dir.x, -dir.z)
			mesh_pivot.rotation.y = lerp_angle(mesh_pivot.rotation.y, target_rot, 2.0 * delta)

func _on_body_entered(body: Node3D) -> void:
	if body != null and body.is_in_group("player"):
		target_player = body
		if label_dialogue != null:
			label_dialogue.text = "IRON GIANT: 'I Am Not A Gun! Standing Guard Over The OASIS Protector Active!'"

func _on_body_exited(body: Node3D) -> void:
	if body != null and body.is_in_group("player"):
		target_player = null
		if label_dialogue != null:
			label_dialogue.text = "IRON GIANT: 'Standing Guard Over The OASIS.'"
