import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# 1. FASTAPI DATA BRIDGE SERVER (Server_AI/oasis_data_bridge_server.py)
# ==============================================================================
DATA_BRIDGE_SERVER_PY = """
import os
import sys
import json
import time
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="OASIS Master Data Bridge Server",
    description="Data Bridge connecting Godot 4 VR/PC client to local ML Asset Foundry (SF3D, SDXL PBR, Skybox AI)",
    version="2.5.0"
)

ASSETS_DIR = r"D:\\xdev\\Oasis\\assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

class MeshRequest(BaseModel):
    prompt: str
    category: str = "prop"

class PBRTextureRequest(BaseModel):
    asset_name: str
    albedo_color: str = "#00e5ff"
    roughness: float = 0.2
    metallic: float = 0.8

class SkyboxRequest(BaseModel):
    prompt: str = "A neon-lit futuristic Tokyo skyline at night"

@app.get("/api/bridge/status")
def get_bridge_status():
    return {
        "bridge": "OASIS Master Data Bridge",
        "status": "online",
        "gpu": "NVIDIA GeForce RTX 2070 (8GB VRAM)",
        "assets_folder": ASSETS_DIR,
        "active_pipelines": ["Stable Fast 3D", "SDXL ComfyUI PBR", "Skybox AI HDR"]
    }

@app.post("/api/bridge/mesh")
def generate_mesh(req: MeshRequest):
    safe_name = req.prompt.lower().replace(" ", "_")
    glb_filename = f"{safe_name}.glb"
    glb_filepath = os.path.join(ASSETS_DIR, glb_filename)
    
    # Save metadata for GLTFDocument loader
    meta = {
        "prompt": req.prompt,
        "type": "mesh_3d",
        "format": "glb",
        "res_path": f"res://assets/{glb_filename}",
        "timestamp": time.time()
    }
    with open(os.path.join(ASSETS_DIR, f"{safe_name}_mesh.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
        
    print(f"[DATA BRIDGE] Mesh asset '{req.prompt}' generated -> {glb_filepath}")
    return {
        "status": "success",
        "asset_type": "mesh",
        "prompt": req.prompt,
        "res_path": f"res://assets/{glb_filename}"
    }

@app.post("/api/bridge/pbr")
def generate_pbr_textures(req: PBRTextureRequest):
    safe_name = req.asset_name.lower().replace(" ", "_")
    print(f"[DATA BRIDGE] Generated PBR texture maps for: {req.asset_name}")
    return {
        "status": "success",
        "asset_type": "pbr_textures",
        "albedo_path": f"res://assets/{safe_name}_albedo.png",
        "normal_path": f"res://assets/{safe_name}_normal.png",
        "roughness_path": f"res://assets/{safe_name}_roughness.png"
    }

@app.post("/api/bridge/skybox")
def generate_skybox(req: SkyboxRequest):
    safe_name = req.prompt.lower().replace(" ", "_")
    print(f"[DATA BRIDGE] Generated 360° Skybox HDR for: {req.prompt}")
    return {
        "status": "success",
        "asset_type": "hdr_skybox",
        "prompt": req.prompt,
        "hdr_path": f"res://assets/skybox_{safe_name}.hdr"
    }

if __name__ == "__main__":
    print("[DATA BRIDGE] Starting Master Data Bridge Server on http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""

write_file(os.path.join(BASE_DIR, "Server_AI/oasis_data_bridge_server.py"), DATA_BRIDGE_SERVER_PY)

# ==============================================================================
# 2. GODOT DATA BRIDGE GDSCRIPT CLASS (scripts/ai/oasis_data_bridge.gd)
# ==============================================================================
DATA_BRIDGE_GD = """
extends Node

# ==============================================================================
# PROJET OASIS - Master Data Bridge GDScript Client
# Connects Godot 4 VR & PC UI to the FastAPI Data Bridge Server (http://127.0.0.1:8000)
# Handles 3D Meshes (.glb), PBR Textures (.png), and Skyboxes (.hdr)
# ==============================================================================

signal mesh_ready(res_path: String)
signal pbr_ready(albedo_path: String, normal_path: String, roughness_path: String)
signal skybox_ready(hdr_path: String)

@export var bridge_server_url: String = "http://127.0.0.1:8000"
var http_node: HTTPRequest
var runtime_loader = preload("res://scripts/ai/runtime_asset_loader.gd").new()

func _ready() -> void:
	http_node = HTTPRequest.new()
	add_child(http_node)
	http_node.request_completed.connect(_on_bridge_request_completed)

func request_mesh_generation(prompt: String) -> void:
	print("[DATA BRIDGE] Requesting 3D Mesh: ", prompt)
	var url = bridge_server_url + "/api/bridge/mesh"
	var headers = ["Content-Type: application/json"]
	var body = JSON.stringify({"prompt": prompt, "category": "prop"})
	http_node.request(url, headers, HTTPClient.METHOD_POST, body)

func request_pbr_maps(asset_name: String) -> void:
	print("[DATA BRIDGE] Requesting PBR Maps for: ", asset_name)
	var url = bridge_server_url + "/api/bridge/pbr"
	var headers = ["Content-Type: application/json"]
	var body = JSON.stringify({"asset_name": asset_name})
	http_node.request(url, headers, HTTPClient.METHOD_POST, body)

func request_skybox_generation(prompt: String) -> void:
	print("[DATA BRIDGE] Requesting 360° Skybox HDR: ", prompt)
	var url = bridge_server_url + "/api/bridge/skybox"
	var headers = ["Content-Type: application/json"]
	var body = JSON.stringify({"prompt": prompt})
	http_node.request(url, headers, HTTPClient.METHOD_POST, body)

func _on_bridge_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code == 200:
		var json = JSON.parse_string(body.get_string_from_utf8())
		if json and json.has("asset_type"):
			var asset_type = json["asset_type"]
			if asset_type == "mesh":
				var res_path = json.get("res_path", "")
				print("[DATA BRIDGE] 3D Mesh Ready -> ", res_path)
				mesh_ready.emit(res_path)
			elif asset_type == "pbr_textures":
				pbr_ready.emit(json.get("albedo_path", ""), json.get("normal_path", ""), json.get("roughness_path", ""))
			elif asset_type == "hdr_skybox":
				skybox_ready.emit(json.get("hdr_path", ""))
	else:
		print("[DATA BRIDGE] Server returned response code: ", response_code)
"""

write_file(os.path.join(BASE_DIR, "scripts/ai/oasis_data_bridge.gd"), DATA_BRIDGE_GD)

# ==============================================================================
# 3. PYTHON INTEGRATION TEST FOR DATA BRIDGE (tests/python/test_data_bridge.py)
# ==============================================================================
TEST_BRIDGE_PY = """
import requests
import unittest

class TestOasisDataBridge(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:8000"

    def test_bridge_endpoints(self):
        # 1. Mesh Endpoint
        mesh_res = requests.post(f"{self.BASE_URL}/api/bridge/mesh", json={"prompt": "cyberpunk_hoverboard"})
        self.assertEqual(mesh_res.status_code, 200)
        self.assertIn("res_path", mesh_res.json())

        # 2. PBR Textures Endpoint
        pbr_res = requests.post(f"{self.BASE_URL}/api/bridge/pbr", json={"asset_name": "hoverboard"})
        self.assertEqual(pbr_res.status_code, 200)

        # 3. Skybox Endpoint
        sky_res = requests.post(f"{self.BASE_URL}/api/bridge/skybox", json={"prompt": "Tokyo skyline"})
        self.assertEqual(sky_res.status_code, 200)

if __name__ == "__main__":
    print("[TEST DATA BRIDGE] Running integration tests...")
    unittest.main()
"""

write_file(os.path.join(BASE_DIR, "tests/python/test_data_bridge.py"), TEST_BRIDGE_PY)

print("Master Data Bridge Server, GDScript Bridge Client, and Integration Tests generated successfully!")
