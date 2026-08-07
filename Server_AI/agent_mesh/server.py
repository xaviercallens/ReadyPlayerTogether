# Hybrid Agent Mesh Communication Protocol (AMCP) Server
# Supports Local RTX 2070 mode (Development) and GCP mode (Scale)

import asyncio
import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from Server_AI.agent_mesh.broker import mesh_broker
from Server_AI.agent_mesh.ollama_agent import OllamaDialogueAgent
from Server_AI.agent_mesh.gemini_cloud_agent import GeminiCloudAgent
from Server_AI.agent_mesh.comfyui_agent import ComfyUITextureAgent
from Server_AI.agent_mesh.rvc_agent import RVCVoiceAgent

app = FastAPI(
    title="Hybrid OASIS Agent Mesh Server (AMCP)",
    description="Asynchronous multi-agent backend orchestrator for Godot 4 VR",
    version="3.0.0"
)

# Deployment Environment: 'local' (RTX 2070) or 'gcp' (Google Cloud)
ENVIRONMENT = os.getenv("OASIS_ENV", "local")

print(f"=== INITIALIZING AMCP MESH IN '{ENVIRONMENT.upper()}' MODE ===")

if ENVIRONMENT == "local":
    dialogue_agent = OllamaDialogueAgent()
else:
    dialogue_agent = GeminiCloudAgent()

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
        "system": "Projet OASIS Hybrid AMCP",
        "environment": ENVIRONMENT,
        "llm_backend": "Ollama (Local 4-bit)" if ENVIRONMENT == "local" else "GCP Gemini API (Cloud)"
    }

@app.post("/api/mesh/speak")
async def process_npc_speech(event: SpeechEvent):
    # Route dialogue based on environment
    response_text = await dialogue_agent.generate_response(event.persona, event.player_text)
    
    # RVC Voice Cloning (could also be routed to GCP Vertex Custom Prediction in Cloud mode)
    audio_res_path = await rvc_agent.synthesize_character_voice(response_text, event.npc_name.lower())
    
    return {
        "status": "success",
        "environment": ENVIRONMENT,
        "npc_name": event.npc_name,
        "reply_text": response_text,
        "audio_stream_path": audio_res_path
    }

@app.post("/api/mesh/generate_pbr")
async def process_pbr_texture(event: TextureEvent):
    result = await comfy_agent.generate_pbr_material(event.material_prompt)
    result["environment"] = ENVIRONMENT
    return result

if __name__ == "__main__":
    port = 8005 if ENVIRONMENT == "local" else 8080
    host = "127.0.0.1" if ENVIRONMENT == "local" else "0.0.0.0"
    print(f"[Agent Mesh Server] Starting AMCP on http://{host}:{port}...")
    uvicorn.run(app, host=host, port=port)
