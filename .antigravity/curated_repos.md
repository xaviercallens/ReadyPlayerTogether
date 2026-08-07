# 📚 OASIS Curated Repositories & Tech Stack

This document tracks the best open-source repositories integrated into **Projet OASIS (ReadyPlayerTogether)**.

## 1. Ready Player Me Avatar Plugin for Godot 4
- **Repository**: [Malcolmnixon/GodotReadyPlayerMeAvatar](https://github.com/Malcolmnixon/GodotReadyPlayerMeAvatar) & [readyplayerme](https://github.com/readyplayerme)
- **Role**: Universal avatar engine. Handles GLTF/GLB runtime downloading, skeleton bone mapping, morph target facial expressions, and VR IK hands.

## 2. Godot AI Dialog (The Brain of the OASIS)
- **Repository**: [krishsharma0413/godot-AI-Dialog](https://github.com/krishsharma0413/godot-AI-Dialog)
- **Role**: Asynchronous LLM dialogue manager for Godot 4 (OpenAI, OpenRouter, Llama 3, Gemini). Manages system personas, NPC responses, and GDScript signal triggers (e.g., puzzle solved event).

## 3. Godot 4 Procedural Generation (The Architect)
- **Repository**: [gdquest-demos/godot-4-procedural-generation](https://github.com/gdquest-demos/godot-4-procedural-generation)
- **Role**: Infinite world generator using WorkerThreadPool/WorkerThreads. Prevents VR frame drops by loading planets, asteroid fields, and dungeons in background threads.

## 4. Agentic AI Skills & Godot 4 Context Prompter (The Developer Multiplier)
- **Repository**: [jame581/GodotPrompter](https://github.com/jame581/GodotPrompter) / [thedivergentai/gd-agentic-skills](https://github.com/thedivergentai/gd-agentic-skills)
- **Role**: Antigravity & Windsurf prompt engineering context files enforcing strict Godot 4.3+ GDScript syntax (Callable, WorkerThreadPool, CharacterBody3D, `@export`), preventing Godot 3 API hallucinations.

## 5. Mixamo to Godot 4 Animation Pipeline (3D Avatars Engine)
- **Repository**: [bogdanMerkulow/MixamoToGodot](https://github.com/bogdanMerkulow/MixamoToGodot)
- **Role**: Automated Blender/Python pipeline converting Mixamo animations (walk, run, dance, combat) with Root Motion directly into Godot 4 `AnimationTree`.

## 6. Godot RL Agents (Reinforcement Learning for NPCs & Vehicles)
- **Repository**: [godotengine/godot-rl-agents](https://github.com/godotengine/godot-rl-agents)
- **Role**: Reinforcement learning framework (PyTorch/Ray) for training autonomous DeLorean vehicles and mechs in the Copper Key track by trial and error.

## 7. Ollama Local LLMs (4-bit Quantized Local NPC Brain)
- **Repositories**: [ollama/ollama](https://github.com/ollama/ollama) & [Manoj-Make-Games/Godot-Ollama-Plugin](https://github.com/Manoj-Make-Games/Godot-Ollama-Plugin)
- **Role**: Runs 4-bit Llama 3 / Mistral locally on RTX 2070 GPU (~4.5 GB VRAM), leaving plenty of memory for Godot 4 VR rendering.

## 8. RVC Voice Cloning (Retrieval-based Voice Conversion)
- **Repository**: [RVC-Project/Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)
- **Role**: Deep learning voice conversion pipeline (Edge-TTS + RVC) giving Parzival, Art3mis, and Anorak iconic voices.

## 9. ComfyUI PBR Material Foundry (VRAM-Efficient Textures)
- **Repository**: [comfyanonymous/ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- **Role**: Node-based Stable Diffusion API generating Albedo, Normal, and Roughness maps for neon cyberpunk surfaces.

## 10. Agent Mesh Orchestrator (AMCP Asynchronous Protocol)
- **Location**: `Server_AI/agent_mesh/` & `scripts/ai/agent_mesh_bridge.gd`
- **Role**: Asynchronous event broker with VRAM Governor capping total GPU memory under 7.5 GB for RTX 2070.

## 11. Third Person Controller & Desktop Fallback
- **Repository**: [emirthab/third-person-controller](https://github.com/emirthab/third-person-controller)
- **Role**: Desktop/Screen fallback mechanics with SpringArm3D to allow testing avatars and gameplay without wearing the VR headset constantly.

## 12. Phantom Camera (Cinematics & Transitions)
- **Repository**: [ramokz/phantom-camera](https://github.com/ramokz/phantom-camera)
- **Role**: Dynamic, procedural camera control inspired by Unity Cinemachine, perfect for switching between VR first-person and desktop third-person testing modes.

## 13. Genie Sim (The Spatial Builder)
- **Repository**: [AgibotTech/Genie-Sim](https://github.com/AgibotTech/Genie-Sim) *(concept)*
- **Role**: Spatial World Model generating physical `.gltf` and `.usd` 3D environments from text/images, imported natively into Godot 4 via `GLTFDocument`.

## 14. Matrix-Game 2.0 (The Real-Time Dreamer)
- **Repository**: [SkyworkAI/Matrix-Game-2](https://github.com/SkyworkAI/Matrix-Game-2) *(concept)*
- **Role**: Playable AI video hallucinator running via FastAPI/WebSockets on the RTX 2070, streamed directly onto 3D arcade screens or portals inside Godot VR.

## 15. ReadyPlayerTogether (Our Open-Source Project)
- **Repository**: [xaviercallens/ReadyPlayerTogether](https://github.com/xaviercallens/ReadyPlayerTogether)
- **Role**: Main open-source collaborative project for father & son pair programming.

## 16. Gemini 3.1 Pro (QA & Architecture Agent)
- **Role**: Background Worker interacting with GCP Vertex AI to provide automated Godot 4 Code Review, Unit-Test generation (GUT), and Architectural improvements via the `qa-architecture` custom Antigravity Skill.