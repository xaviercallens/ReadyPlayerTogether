---
name: developer
description: Full-stack developer skill for OASIS (`xaviercallens/ReadyPlayerTogether`). Covers Python automation script patterns (`build_*.py`), FastAPI backend integration, Father-Son pair programming workflow guidelines, GDScript integration, and codebase maintenance.
---

# OASIS Full-Stack Developer Skill

This skill defines the software development standards, Python automation patterns, backend AI integrations, and pair-programming workflows for the **OASIS** project (`xaviercallens/ReadyPlayerTogether`).

---

## 1. Project Workflow & Multi-Tool Father-Son Setup

OASIS is designed as a collaborative Ready Player One inspired universe built with a **Father-Son pair programming methodology** leveraging multiple AI tools:

- **Son's Front-End Environment (Google Antigravity Chat + Godot 4 Editor)**:
  - Uses **Antigravity Chat** as an interactive front-end assistant to discuss features, ask for GDScript guidance, test 3D scene mechanics, and playtest on Meta Quest 3S / PC.
  - Antigravity acts as a pedagogical coach for the son, explaining concepts clearly and providing runnable snippets.
- **Father's Heavy Automation Environment (Antigravity IDE / Windsurf / Claude Code)**:
  - Uses **Antigravity IDE**, **Windsurf**, or **Claude Code** to write Python generator scripts (`build_*.py`, `add_*.py`), configure FastAPI server endpoints (`Server_AI`), run 3D world generators (`AgibotTech/genie_sim`), and manage master repository architecture (`xaviercallens/ReadyPlayerTogether`).
- **Antigravity AI Agent (Collaborative Bridge)**:
  - Maintains dual-persona behavior: providing pedagogical, step-by-step guidance when interacting with the Son, and automated, high-throughput script generation/refactoring when interacting with the Father.
  - Master blueprint details are stored in [OASIS_MODUS_OPERANDI.md](file:///d:/xdev/Oasis/OASIS_MODUS_OPERANDI.md).

---

## 2. Python Scene Generator Pattern (`build_*.py`)

In OASIS, scenes and resources are programmatically built or modified using Python scripts to eliminate manual GUI assembly errors.

### Standard Script Template
```python
import os
import re

SCENE_PATH = "scenes/hub/oasis_master_rpo_movie.tscn"

def build_scene():
    print(f"[OASIS Dev] Updating scene: {SCENE_PATH}")

    tscn_content = """[gd_scene load_steps=5 format=3 uid="uid://oasis_master_hub"]

[ext_resource type="Script" path="res://scripts/hub/cyberpunk_hub.gd" id="1_script"]

[node name="OasisMasterHub" type="Node3D"]
script = ExtResource("1_script")

[node name="DirectionalLight3D" type="DirectionalLight3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 0.707, 0.707, 0, -0.707, 0.707, 0, 10, 0)
light_color = Color(0.9, 0.85, 1, 1)
shadow_enabled = true

[node name="Ground" type="CSGBox3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, -0.5, 0)
use_collision = true
size = Vector3(100, 1, 100)
"""
    os.makedirs(os.path.dirname(SCENE_PATH), exist_ok=True)
    with open(SCENE_PATH, "w", encoding="utf-8") as f:
        f.write(tscn_content.strip())
    print("[OASIS Dev] Scene generated successfully!")

if __name__ == "__main__":
    build_scene()
```

---

## 3. Server AI & FastAPI Integration (`Server_AI`)

Backend AI services reside in `Server_AI/`:
- `oasis_fastapi_server.py`: Primary game orchestrator API (port 8000/8007).
- `gemini_qa_server.py`: Gemini 3.1 Pro proxy for code review, unit tests, and architecture (`/api/qa/*`).
- `oasis_data_bridge_server.py`: Real-time WebSocket/HTTP bridge for character sync and quest data.

### Developing FastAPI Endpoints
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="OASIS Game Orchestrator")

class QuestStatus(BaseModel):
    user_id: str
    key_name: str # "CopperKey", "JadeKey", "CrystalKey"
    completed: bool

@app.post("/api/quest/update")
async def update_quest(status: QuestStatus):
    print(f"[OASIS Backend] Player {status.user_id} updated quest {status.key_name}: {status.completed}")
    return {"status": "success", "user_id": status.user_id, "key": status.key_name}
```

---

## 4. Code Standards & Git Best Practices

- **Repository Target**: `xaviercallens/ReadyPlayerTogether`
- **File Naming**:
  - GDScript: `snake_case.gd` (e.g. `third_person_controller.gd`)
  - Godot Scenes: `snake_case.tscn` (e.g. `cyberpunk_hub.tscn`)
  - Python Scripts: `snake_case.py` (e.g. `build_cyberpunk_hub_and_rpm.py`)
- **Error Logs**: Inspect `godot_runtime.log` and `notify.log` whenever fixing runtime or compile bugs. Never mask errors.
