---
name: godot
description: Godot 4.x engine skill for OASIS. Provides GDScript 2.0 coding conventions, Node3D scene management, XR/Desktop dual-mode controllers, Forward+ rendering, and pedagogical references from Godot-Ready-Player-One workshops.
---

# Godot 4 Engine Skill - OASIS Project

This skill provides comprehensive instructions for writing, refactoring, and maintaining GDScript 2.0 code and Godot 4 scenes in the **OASIS Ready Player One / Ready Player Together** codebase.

## 1. Engine & Configuration Context
- **Godot Version**: 4.x (Forward+ Mobile/Desktop rendering pipeline, compatibility mode for Web/Quest 3S ASTC textures).
- **Project Root File**: `project.godot`
- **Main Scene**: `res://scenes/hub/oasis_master_rpo_movie.tscn`
- **Input Map Actions**: `move_forward`, `move_backward`, `move_left`, `move_right`, `jump`.
- **Pedagogical References**:
  - `Godot-Ready-Player-One/Workshop-3-base-project`: Core GDScript 3D mechanics & puzzle interaction patterns.
  - `Godot-Ready-Player-One/Workshop_4_base_project`: Advanced VR interaction, UI overlay, and event handlers.

---

## 2. GDScript 2.0 Coding Conventions

### Class Definition & Annotations
```gdscript
class_name PlayerController3D
extends CharacterBody3D

signal health_changed(new_health: float)
signal quest_item_collected(item_name: String)

@export_category("Movement Settings")
@export var speed: float = 5.0
@export var jump_velocity: float = 4.5
@export var rotation_sensitivity: float = 0.003

@onready var camera_3d: Camera3D = $Camera3D
@onready var animation_player: AnimationPlayer = $AnimationPlayer
```

### Type Safety & Clean Execution
- Always specify static type annotations (`: String`, `: Vector3`, `: float`, `-> void`).
- Use `@onready` variables for child node retrieval; avoid repeated `get_node()` inside `_process()` or `_physics_process()`.
- Check node validity with `is_instance_valid(node)` before dereferencing variables that might be freed asynchronously.

### Physics & Input Loop Pattern
```gdscript
func _physics_process(delta: float) -> void:
	# Apply gravity if not on floor
	if not is_on_floor():
		velocity += get_gravity() * delta

	# Handle Jump
	if Input.is_action_just_pressed("jump") and is_on_floor():
		velocity.y = jump_velocity

	# Get input vector
	var input_dir := Input.get_vector("move_left", "move_right", "move_forward", "move_backward")
	var direction := (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()

	if direction:
		velocity.x = direction.x * speed
		velocity.z = direction.z * speed
	else:
		velocity.x = move_toward(velocity.x, 0, speed)
		velocity.z = move_toward(velocity.z, 0, speed)

	move_and_slide()
```

---

## 3. Scene Architecture & Hierarchy Guidelines

### Standard Scene Layout
Each OASIS scene should follow a clean, modular structure:
```text
RootNode3D (Node3D / WorldEnvironment)
├── DirectionalLight3D
├── WorldEnvironment
├── Ground (StaticBody3D)
├── Player (CharacterBody3D or XRToolsPlayer)
├── Environment/
│   ├── HubMesh (MeshInstance3D)
│   └── Spawnables/
├── NPCs/
│   ├── Parzival (CharacterBody3D + LipSyncViseme)
│   ├── Art3mis
│   └── Aech
└── CanvasLayer/ (UI & CommandMenu)
```

---

## 4. Dual Mode Controller (XR VR + Keyboard Desktop)

OASIS supports both Meta Quest 3S VR headset controllers and traditional PC Desktop WASD controls.
- Detect OpenXR runtime at startup:
```gdscript
func _setup_xr_or_desktop() -> void:
	var xr_interface = XRServer.find_interface("OpenXR")
	if xr_interface and xr_interface.is_initialized():
		DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
		get_viewport().use_xr = true
		print("[OASIS Godot] OpenXR initialized successfully.")
	else:
		print("[OASIS Godot] OpenXR not detected. Falling back to Desktop 3D Mode.")
```

---

## 5. Headless Execution & CLI Commands

You can run Godot headless for verification or automated tests:
```powershell
# Run Godot in headless mode to verify scene compilation
.\Godot4.exe --headless --script scripts/solve_all_node_warnings_and_errors.py
```
