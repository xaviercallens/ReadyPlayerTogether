# ☁️ OASIS Hybrid Cloud Architecture (AMCP)

To balance **rapid local development** with **massive cloud scale**, the OASIS Agent Mesh Communication Protocol (AMCP) implements a **Hybrid Cloud Architecture**.

## 🔄 Environment Toggling
The entire backend orchestration behavior is controlled via the `OASIS_ENV` environment variable.

### 1. Local Mode (`OASIS_ENV="local"`)
*Target: RTX 2070 (8GB VRAM) for local testing and zero-cost development.*
- **LLM Engine**: `ollama_agent.py` routes NPC dialogue to a local 4-bit quantized Llama 3 / Mistral model (~4.5 GB VRAM).
- **PBR Textures**: `comfyui_agent.py` generates Normal/Roughness maps via a local ComfyUI instance.
- **Voice Cloning**: `rvc_agent.py` synthesizes speech locally via Edge-TTS and RVC.
- **RL Agent**: `godot_rl_agent.py` trains the DeLorean using local PyTorch/Ray.
- **VRAM Governor**: Ensures cumulative local GPU allocation never exceeds 7.5 GB to prevent crashing Godot 4 VR rendering.
- **Server**: FastAPI runs on `http://127.0.0.1:8005`.

### 2. Cloud Mode (`OASIS_ENV="gcp"`)
*Target: Google Cloud Platform (GCP) for global multiplayer scale and heavy compute.*
- **LLM Engine**: `gemini_cloud_agent.py` routes NPC dialogue to **GCP Vertex AI (Gemini 3.1 Pro/Ultra)** for infinite scale, extremely low latency, and zero local VRAM cost.
- **PBR Textures & Voice**: Agents can be mapped to custom endpoints deployed on **Cloud Run** or **Vertex AI Custom Prediction routines** (equipped with powerful L4 or A100 GPUs).
- **RL Agent**: Training data is streamed to a distributed **Ray Cluster** on GCP.
- **Server**: FastAPI binds to `0.0.0.0:8080`, ready to be containerized via Docker and deployed to **Google Cloud Run**.

## 🔌 Godot 4 Integration
Godot 4 (`res://scripts/ai/agent_mesh_bridge.gd`) remains completely agnostic to the environment. It always publishes events to the FastAPI Mesh Orchestrator, which acts as the intelligent router.
