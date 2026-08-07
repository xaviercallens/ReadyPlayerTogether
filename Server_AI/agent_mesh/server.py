# Agent Mesh Communication Protocol (AMCP) Server
# FastAPI Gateway exposing WebSocket & REST API to Godot 4

import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import uvicorn

from Server_AI.agent_mesh.broker import mesh_broker
from Server_AI.agent_mesh.ollama_agent import OllamaDialogueAgent
from Server_AI.agent_mesh.comfyui_agent import ComfyUITextureAgent
from Server_AI.agent_mesh.rvc_agent import RVCVoiceAgent

app = FastAPI(
    title="OASIS Agent Mesh Server (AMCP)",
    description="Asynchronous multi-agent backend orchestrator for Godot 4 VR",
    version="2.0.0"
)

ollama_agent = OllamaDialogueAgent()
comfy_agent = ComfyUITextureAgent()
rvc_agent = RVCVoiceAgent()

class SpeechEvent(BaseModel):
    npc_name: str
    persona: str
    player_text: str

class TextureEvent(BaseModel):
    material_prompt: str

@app.get("/")
def index():
    return {
        "system": "Projet OASIS Agent Mesh Communication Protocol (AMCP)",
        "gpu": "NVIDIA GeForce RTX 2070 (8GB VRAM)",
        "agents": ["Ollama_LLM", "ComfyUI_PBR", "RVC_VoiceCloning", "Godot_RL"]
    }

@app.post("/api/mesh/speak")
async def process_npc_speech(event: SpeechEvent):
    # 1. Ollama LLM Dialogue
    response_text = await ollama_agent.generate_response(event.persona, event.player_text)
    # 2. RVC Voice Cloning
    audio_res_path = await rvc_agent.synthesize_character_voice(response_text, event.npc_name.lower())
    
    return {
        "status": "success",
        "npc_name": event.npc_name,
        "reply_text": response_text,
        "audio_stream_path": audio_res_path
    }

@app.post("/api/mesh/generate_pbr")
async def process_pbr_texture(event: TextureEvent):
    result = await comfy_agent.generate_pbr_material(event.material_prompt)
    return result

if __name__ == "__main__":
    print("[Agent Mesh Server] Starting AMCP Orchestrator on http://127.0.0.1:8005...")
    uvicorn.run(app, host="127.0.0.1", port=8005)
