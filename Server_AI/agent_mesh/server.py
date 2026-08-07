# Unified OASIS Agent Mesh Server
# Consolidates all sub-services into a single FastAPI instance.
# Supports Local RTX 2070 mode (Development) and GCP mode (Scale)

import asyncio
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()  # Load .env file if present

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from Server_AI.agent_mesh.broker import mesh_broker
from Server_AI.agent_mesh.ollama_agent import OllamaDialogueAgent
from Server_AI.agent_mesh.gemini_cloud_agent import GeminiCloudAgent
from Server_AI.agent_mesh.comfyui_agent import ComfyUITextureAgent
from Server_AI.agent_mesh.rvc_agent import RVCVoiceAgent
from Server_AI.gemini_qa_agent import QAskillsWorker

# Deployment Environment: 'local' (RTX 2070) or 'gcp' (Google Cloud)
ENVIRONMENT = os.getenv("OASIS_ENV", "local")

# --- Agent Initialization ---
if ENVIRONMENT == "local":
    dialogue_agent = OllamaDialogueAgent()
else:
    dialogue_agent = GeminiCloudAgent()

comfy_agent = ComfyUITextureAgent()
rvc_agent = RVCVoiceAgent()
qa_worker = QAskillsWorker()

# --- Conversation Memory (session-based) ---
conversation_sessions: dict[str, list[dict]] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start background workers on startup, clean up on shutdown."""
    print(f"=== INITIALIZING OASIS AMCP MESH IN '{ENVIRONMENT.upper()}' MODE ===")
    qa_task = asyncio.create_task(qa_worker.start())
    yield
    await qa_worker.stop()
    qa_task.cancel()


app = FastAPI(
    title="OASIS Unified Agent Mesh Server (AMCP)",
    description="Single-entry orchestrator for all OASIS AI services (Dialogue, PBR, Voice, QA).",
    version="4.0.0",
    lifespan=lifespan,
)


# ===========================================================================
# Models
# ===========================================================================
class SpeechEvent(BaseModel):
    npc_name: str
    persona: str
    player_text: str
    session_id: str = "default"

class TextureEvent(BaseModel):
    material_prompt: str

class QARequest(BaseModel):
    file_path: str


# ===========================================================================
# Routes — Core Mesh
# ===========================================================================
@app.get("/")
def index():
    return {
        "system": "Projet OASIS Unified AMCP",
        "environment": ENVIRONMENT,
        "llm_backend": "Ollama (Local 4-bit)" if ENVIRONMENT == "local" else "GCP Gemini API (Cloud)",
        "services": ["speak", "generate_pbr", "qa/review", "qa/unittest", "qa/improve", "vram/status"],
    }

@app.get("/api/vram/status")
def vram_status():
    """Real-time VRAM monitoring endpoint."""
    return mesh_broker.vram_governor.status()

@app.post("/api/mesh/speak")
async def process_npc_speech(event: SpeechEvent):
    # Retrieve or create conversation history for this session
    if event.session_id not in conversation_sessions:
        conversation_sessions[event.session_id] = []
    history = conversation_sessions[event.session_id]

    # Build full prompt with conversation context
    history.append({"role": "user", "content": event.player_text})
    context = "\n".join(
        f"{msg['role']}: {msg['content']}" for msg in history[-10:]  # Last 10 messages
    )
    full_prompt = f"{event.persona}\n\nConversation:\n{context}"

    response_text = await dialogue_agent.generate_response(full_prompt, event.player_text)
    history.append({"role": "assistant", "content": response_text})

    # Voice cloning
    audio_res_path = await rvc_agent.synthesize_character_voice(response_text, event.npc_name.lower())

    return {
        "status": "success",
        "environment": ENVIRONMENT,
        "npc_name": event.npc_name,
        "reply_text": response_text,
        "audio_stream_path": audio_res_path,
        "session_id": event.session_id,
    }

@app.post("/api/mesh/generate_pbr")
async def process_pbr_texture(event: TextureEvent):
    result = await comfy_agent.generate_pbr_material(event.material_prompt)
    result["environment"] = ENVIRONMENT
    return result


# ===========================================================================
# Routes — QA & Architecture (Gemini 3.1 Pro)
# ===========================================================================
@app.post("/api/qa/review")
async def qa_review(req: QARequest):
    fut = asyncio.get_event_loop().create_future()
    def cb(res: str):
        fut.set_result(res)
    await qa_worker.queue.put({"type": "review", "file": req.file_path, "callback": cb})
    result = await fut
    return {"result": result}

@app.post("/api/qa/unittest")
async def qa_unittest(req: QARequest):
    fut = asyncio.get_event_loop().create_future()
    def cb(res: str):
        fut.set_result(res)
    await qa_worker.queue.put({"type": "unittest", "file": req.file_path, "callback": cb})
    result = await fut
    return {"result": result}

@app.post("/api/qa/improve")
async def qa_improve(req: QARequest):
    fut = asyncio.get_event_loop().create_future()
    def cb(res: str):
        fut.set_result(res)
    await qa_worker.queue.put({"type": "improve", "file": req.file_path, "callback": cb})
    result = await fut
    return {"result": result}


# ===========================================================================
# Entry Point
# ===========================================================================
if __name__ == "__main__":
    port = 8005 if ENVIRONMENT == "local" else 8080
    host = "127.0.0.1" if ENVIRONMENT == "local" else "0.0.0.0"
    print(f"[OASIS Server] Starting Unified AMCP on http://{host}:{port}...")
    uvicorn.run(app, host=host, port=port)
