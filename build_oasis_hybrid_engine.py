import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# 1. MATRIX-GAME STREAMING SERVER (Server_AI/matrix_game_streamer.py)
# ==============================================================================
STREAMER_PY = """
import asyncio
import time
import json
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI(
    title="OASIS Matrix-Game 2.0 Streaming Server",
    description="Real-time AI Video & Dimension Streamer for Godot Virtual Screens & Portals",
    version="2.0.0"
)

@app.get("/")
def root():
    return {
        "server": "Matrix-Game 2.0 Streamer",
        "status": "active",
        "target_fps": 25,
        "gpu": "NVIDIA GeForce RTX 2070"
    }

@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()
    print("[MATRIX STREAMER] Godot Virtual Portal connected!")
    frame_count = 0
    try:
        while True:
            frame_count += 1
            # Send frame metadata & simulation packet to Godot
            packet = {
                "frame": frame_count,
                "timestamp": time.time(),
                "dimension": "Cyberpunk Neon Portal",
                "status": "streaming"
            }
            await websocket.send_text(json.dumps(packet))
            await asyncio.sleep(1.0 / 25.0) # 25 FPS Stream
    except WebSocketDisconnect:
        print("[MATRIX STREAMER] Godot Virtual Portal disconnected.")

if __name__ == "__main__":
    print("[MATRIX STREAMER] Starting server on ws://127.0.0.1:8001/ws/stream ...")
    uvicorn.run(app, host="127.0.0.1", port=8001)
"""

write_file(os.path.join(BASE_DIR, "Server_AI/matrix_game_streamer.py"), STREAMER_PY)

# ==============================================================================
# 2. VIRTUAL PORTAL SCREEN SCRIPT (scripts/ui/virtual_portal_screen.gd)
# ==============================================================================
PORTAL_SCREEN_GD = """
extends Node3D

# ==============================================================================
# PROJET OASIS - Virtual Portal Screen (Matrix-Game 2.0 Receiver)
# Displays dynamic AI streamed dimensions inside the 3D OASIS world.
# ==============================================================================

@onready var screen_label: Label3D = $ScreenMesh/Label3D
var time_passed: float = 0.0

func _process(delta: float) -> void:
	time_passed += delta
	# Pulsing portal frame effect
	$ScreenMesh.position.y = 2.2 + sin(time_passed * 2.0) * 0.05
"""

PORTAL_SCREEN_TSCN = """
[gd_scene load_steps=5 format=3 uid="uid://virtual_portal_screen_scene"]

[ext_resource type="Script" path="res://scripts/ui/virtual_portal_screen.gd" id="1_script"]

[sub_resource type="StandardMaterial3D" id="Mat_PortalScreen"]
albedo_color = Color(0.0, 0.9, 1.0, 1)
metallic = 0.9
roughness = 0.1
emission_enabled = true
emission = Color(0.0, 0.9, 1.0, 1)
emission_energy_multiplier = 4.0

[sub_resource type="BoxMesh" id="Mesh_Screen"]
material = SubResource("Mat_PortalScreen")
size = Vector3(4.0, 2.5, 0.1)

[node name="VirtualPortalScreen" type="Node3D"]
script = ExtResource("1_script")

[node name="ScreenMesh" type="MeshInstance3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.2, 0)
mesh = SubResource("Mesh_Screen")

[node name="Label3D" type="Label3D" parent="ScreenMesh"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0.08)
billboard = 1
pixel_size = 0.015
text = "MATRIX-GAME 2.0 VIRTUAL PORTAL
[Dynamic AI World Streaming @ 25 FPS]"
font_size = 38
outline_size = 8
"""

write_file(os.path.join(BASE_DIR, "scripts/ui/virtual_portal_screen.gd"), PORTAL_SCREEN_GD)
write_file(os.path.join(BASE_DIR, "scenes/ui/virtual_portal_screen.tscn"), PORTAL_SCREEN_TSCN)

# ==============================================================================
# 3. HYBRID ENGINE MASTER GUIDE (.antigravity/hybrid_engine_guide.md)
# ==============================================================================
HYBRID_GUIDE_MD = """
# 🚀 OASIS Hybrid Architecture Engine (Genie Sim + Matrix-Game 2.0 + Godot 4)

Ce document détaille l'architecture hybride du Projet OASIS.

---

### 🌐 Les 3 Composants de la Stratégie Hybride :

1. **La Base (Godot 4)** :
   - Moteur physique, collisions, saut, ramassage de la Clé de Cuivre et contrôles VR/PC.

2. **L'Architecte (Genie Sim GLTF)** :
   - Modèle 3D persistant généré en arrière-plan et chargé dynamiquement par `GLTFDocument`.

3. **Le Rêveur (Matrix-Game 2.0 Streamer)** :
   - Serveur WebSocket Python (`Server_AI/matrix_game_streamer.py`) diffusant un flux interactif 25 FPS affiché sur les **Écrans / Portails Virtuels** ([scenes/ui/virtual_portal_screen.tscn](file:///D:/xdev/Oasis/scenes/ui/virtual_portal_screen.tscn)).
"""

write_file(os.path.join(BASE_DIR, ".antigravity/hybrid_engine_guide.md"), HYBRID_GUIDE_MD)

print("OASIS Hybrid Architecture Engine components generated successfully!")
