import os
import sys
import json
import time
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="OASIS ML Foundry & Orchestrator API",
    description="Asynchronous Backend ML Server for Project OASIS - ReadyPlayerTogether",
    version="1.0.0"
)

ASSETS_DIR = r"D:\xdev\Oasis\assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

class AssetPromptRequest(BaseModel):
    prompt: str
    category: str = "prop"

class LipSyncRequest(BaseModel):
    text: str
    avatar_id: str = "parzival"

@app.get("/")
def read_root():
    return {
        "status": "online",
        "project": "Projet OASIS - ReadyPlayerTogether",
        "gpu": "NVIDIA GeForce RTX 2070 (8GB VRAM)",
        "orchestrator": "Google Antigravity Backend Engine"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/api/generate_asset")
def generate_asset(req: AssetPromptRequest):
    print(f"[ML FOUNDRY] Received prompt from Godot: '{req.prompt}'")
    safe_name = req.prompt.lower().replace(" ", "_")
    output_glb_path = os.path.join(ASSETS_DIR, f"{safe_name}.glb")
    
    # Generate placeholder metadata for GLTFDocument loader
    meta_file = os.path.join(ASSETS_DIR, f"{safe_name}.json")
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump({
            "prompt": req.prompt,
            "glb_file": f"res://assets/{safe_name}.glb",
            "status": "ready"
        }, f, indent=2)
        
    return {
        "status": "success",
        "prompt": req.prompt,
        "asset_res_path": f"res://assets/{safe_name}.glb",
        "message": f"Asset '{req.prompt}' ready for GLTFDocument runtime loading!"
    }

@app.post("/api/lipsync")
def generate_lipsync(req: LipSyncRequest):
    visemes = [
        {"time": 0.0, "viseme": "sil"},
        {"time": 0.1, "viseme": "AA"},
        {"time": 0.25, "viseme": "E"},
        {"time": 0.4, "viseme": "O"},
        {"time": 0.55, "viseme": "sil"}
    ]
    return {
        "status": "success",
        "avatar_id": req.avatar_id,
        "text": req.text,
        "viseme_keyframes": visemes
    }

if __name__ == "__main__":
    print("[OASIS BACKEND] Starting FastAPI Orchestrator on http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)