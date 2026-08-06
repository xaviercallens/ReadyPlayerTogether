import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# 1. FIX PARZIVAL NPC SCRIPT (scripts/characters/parzival_npc.gd)
# ==============================================================================
PARZIVAL_GD = """
extends CharacterBody3D

# ==============================================================================
# PROJET OASIS - Parzival (Ready Player One Gunter NPC)
# ==============================================================================

@onready var key_mesh: Node3D = get_node_or_null("KeyMesh")
@onready var dialogue_label: Label3D = get_node_or_null("DialogueLabel")
@onready var body_mesh: Node3D = get_node_or_null("BodyMesh")

var anim_controller: RPMAnimator
var time_passed: float = 0.0
var is_player_near: bool = false

func _ready() -> void:
	if has_node("InteractionArea"):
		$InteractionArea.body_entered.connect(_on_body_entered)
		$InteractionArea.body_exited.connect(_on_body_exited)
	if dialogue_label != null:
		dialogue_label.text = "PARZIVAL: 'Trouve la Clé de Cuivre!'"
	
	if body_mesh != null:
		anim_controller = RPMAnimator.new()
		anim_controller.target_avatar_node = body_mesh
		add_child(anim_controller)

func _process(delta: float) -> void:
	time_passed += delta
	if key_mesh != null:
		key_mesh.rotation.y += delta * 2.0
		key_mesh.position.y = 2.4 + sin(time_passed * 3.0) * 0.1

func _on_body_entered(body: Node3D) -> void:
	if body != null and body.is_in_group("player"):
		is_player_near = true
		if dialogue_label != null:
			dialogue_label.text = "PARZIVAL: 'Bienvenue Gunter! Traverse le portail 03 pour la course!'"
		if anim_controller != null:
			anim_controller.set_state(RPMAnimator.AnimState.WAVE)

func _on_body_exited(body: Node3D) -> void:
	if body != null and body.is_in_group("player"):
		is_player_near = false
		if dialogue_label != null:
			dialogue_label.text = "PARZIVAL: 'Trouve la Clé de Cuivre!'"
		if anim_controller != null:
			anim_controller.set_state(RPMAnimator.AnimState.IDLE)
"""

write_file(os.path.join(BASE_DIR, "scripts/characters/parzival_npc.gd"), PARZIVAL_GD)

# ==============================================================================
# 2. FIX COMMAND MENU SCRIPT (scripts/ui/command_menu.gd)
# ==============================================================================
COMMAND_MENU_GD = """
extends CanvasLayer

# ==============================================================================
# PROJET OASIS - Controls & Commands Overlay HUD
# ==============================================================================

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_TAB or event.keycode == KEY_ESCAPE:
			var overlay = get_node_or_null("Overlay")
			if overlay == null:
				overlay = get_node_or_null("Control")
			if overlay != null:
				overlay.visible = not overlay.visible
"""

write_file(os.path.join(BASE_DIR, "scripts/ui/command_menu.gd"), COMMAND_MENU_GD)

# ==============================================================================
# 3. FIX DELOREAN CAR SCRIPT (scripts/vehicles/delorean_car.gd)
# ==============================================================================
DELOREAN_GD = """
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
		var b = get_node("Body")
		if b is MeshInstance3D:
			return b as MeshInstance3D
	elif has_node("CarMesh/Body"):
		var cb = get_node("CarMesh/Body")
		if cb is MeshInstance3D:
			return cb as MeshInstance3D
	
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
	var driver_label = get_node_or_null("Driver/VisemeLabel") as Label3D
	if driver_label != null:
		var visemes = ["Aah", "Ohh", "Eee", "Mmm", "First key is earned!"]
		driver_label.text = "PARZIVAL: " + visemes[int(time_passed * 3.0) % visemes.size()]
"""

write_file(os.path.join(BASE_DIR, "scripts/vehicles/delorean_car.gd"), DELOREAN_GD)

print("Runtime script errors for Parzival NPC, CommandMenu, and DeLorean fixed successfully!")
