# 🎯 Strict Godot 4.3+ Agentic GDScript Rules for Antigravity & Windsurf

All GDScript code generated or modified in this workspace **MUST** adhere strictly to Godot 4.3+ standards. 

## 🚫 FORBIDDEN (Godot 3 Legacy API - DO NOT USE)
- ❌ `KinematicBody`, `KinematicBody3D`, `Spatial` ➔ Use `CharacterBody3D`, `Node3D`.
- ❌ `export var x = 1` ➔ Use `@export var x = 1`.
- ❌ `onready var node = $Node` ➔ Use `@onready var node = $Node`.
- ❌ `scene.instance()` ➔ Use `scene.instantiate()`.
- ❌ `connect("signal_name", target, "method")` ➔ Use `signal_name.connect(target.method)`.
- ❌ `emit_signal("signal_name", arg)` ➔ Use `signal_name.emit(arg)`.
- ❌ `ARVROrigin`, `ARVRCamera`, `ARVRController` ➔ Use `XROrigin3D`, `XRCamera3D`, `XRController3D`.
- ❌ `yield()` ➔ Use `await`.
- ❌ `rand_range(min, max)` ➔ Use `randf_range(min, max)` or `randi_range(min, max)`.
- ❌ `str2var()`, `var2str()` ➔ Use `str_to_var()`, `var_to_str()`.

## ✅ MANDATORY (Godot 4.3+ Standards)
1. **Annotations**: Use `@export`, `@export_category`, `@export_range`, `@onready`, `@icon`, `@tool`.
2. **Signals**:
   ```gdscript
   signal puzzle_solved(key_id: String)
   
   func _ready() -> void:
       puzzle_solved.connect(_on_puzzle_solved)
       
   func solve() -> void:
       puzzle_solved.emit("CopperKey")
   ```
3. **Async / HTTP Requests**:
   ```gdscript
   func query_ai_async(prompt: String) -> String:
       var http = HTTPRequest.new()
       add_child(http)
       var error = http.request("https://api.openai.com/v1/chat/completions", headers, HTTPClient.METHOD_POST, json_payload)
       if error != OK:
           return "Error"
       var result = await http.request_completed
       http.queue_free()
       return result[3].get_string_from_utf8()
   ```
4. **Multithreading for VR**:
   Use `WorkerThreadPool` to process heavy procedural algorithms (Perlin noise, voxel meshes, terrain) off the main rendering thread so VR frame rate remains strictly 90+ FPS.

5. **Type Hints**: Always use explicit types in parameters and return types (`func calculate(val: float) -> int:`).
