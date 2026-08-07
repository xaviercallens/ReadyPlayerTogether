---
name: qa
description: Quality Assurance & Testing skill for OASIS. Provides GUT (Godot Unit Test) frameworks, headless engine execution, log analysis (`godot_runtime.log`), pytest for FastAPI backends, and Gemini QA Server endpoints (`/api/qa/review`, `/unittest`, `/improve`).
---

# OASIS Quality Assurance & Testing Skill

This skill defines the testing procedures, automated verification protocols, log analysis rules, and AI QA integrations for the **OASIS** codebase.

---

## 1. Testing Frameworks Overview

| Framework / Tool | Scope | Command / Endpoint |
|---|---|---|
| **GUT (Godot Unit Test)** | GDScript 2.0 unit & integration tests | `tests/godot/` |
| **Pytest** | Python scripts, GenAI pipelines, FastAPI servers | `pytest tests/python/` |
| **Headless Engine Runner** | Scene loading & compile verification | `.\Godot4.exe --headless --script <script.gd>` |
| **Gemini QA Agent Server** | AI-driven code review, test gen & architecture | `http://127.0.0.1:8007/api/qa/*` |

---

## 2. GUT (Godot Unit Test) Standard Template

Create GUT test files under `tests/godot/test_<name>.gd`:

```gdscript
extends GutTest

var player: PlayerController3D

func before_each():
	player = PlayerController3D.new()
	add_child_autofree(player)

func after_each():
	pass

func test_player_initial_health():
	assert_eq(player.speed, 5.0, "Player default speed should be 5.0")

func test_player_jump_velocity():
	assert_gt(player.jump_velocity, 0.0, "Jump velocity must be positive")

func test_player_gravity_applied():
	player.velocity = Vector3.ZERO
	player._physics_process(0.016)
	assert_true(player.velocity.y <= 0, "Gravity should pull velocity downwards")
```

---

## 3. Gemini QA Server API Integration

The OASIS project runs a local Gemini QA proxy on port 8007 (`Server_AI/gemini_qa_server.py`).

### Endpoints
- `POST http://127.0.0.1:8007/api/qa/review`: Returns strict Godot 4 / GDScript code review.
- `POST http://127.0.0.1:8007/api/qa/unittest`: Automatically generates GUT framework unit tests.
- `POST http://127.0.0.1:8007/api/qa/improve`: Recommends state machine & component architectural refactorings.

### Curl Examples
```bash
# Code Review
curl -X POST "http://127.0.0.1:8007/api/qa/review" -H "Content-Type: application/json" -d "{\"file_path\":\"scripts/player/third_person_controller.gd\"}"

# Generate GUT Unit Test
curl -X POST "http://127.0.0.1:8007/api/qa/unittest" -H "Content-Type: application/json" -d "{\"file_path\":\"scripts/hub/cyberpunk_hub.gd\"}"

# Architecture Improvement
curl -X POST "http://127.0.0.1:8007/api/qa/improve" -H "Content-Type: application/json" -d "{\"file_path\":\"scripts/vehicles/delorean_controller.gd\"}"
```

---

## 4. Headless Compilation & Log Inspection Protocol

When checking for broken nodes, missing resources, or script syntax errors:

1. **Run Headless Check**:
```powershell
.\Godot4.exe --headless --script scripts/solve_all_node_warnings_and_errors.py
```

2. **Inspect Log Files**:
   - Check `godot_runtime.log` for standard runtime errors, broken paths, or null references.
   - Check `notify.log` for background service notifications.

3. **Error Resolution Rules**:
   - Never suppress or comment out failing assertions.
   - Trace upstream script instantiation or node paths (`$Path/To/Node`) if a Null Instance error occurs.
   - Verify parameter types match function signatures across calls.
