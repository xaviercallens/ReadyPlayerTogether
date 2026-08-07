# Projet OASIS - Context Memory for Antigravity & Windsurf Agents

## Project Overview
- **Team**: Father (Architect / ML Expert) & Son (Pilot / 10yo Developer).
- **Engine**: Godot Engine 4.x (GDScript, OpenXR enabled).
- **Target VR Headset**: Meta Quest 3S (Standalone & PCVR via Link on RTX 2070 GPU).
- **Aesthetic**: Low-Poly Retro Cyberpunk / Synthwave (Neon grid, glowing portals, synth soundscapes).
- **AI Stack**: GCP Gemini Ultra API / Local LLM (Dynamic quests/dialogue) + Google Flow / Imagen (Skybox/textures).

## 4 Open-Source Pillars (Literature Review & Integration Stack)
1. **The Brain (AI Dialogue)**: `krishsharma0413/godot-AI-Dialog` - Async LLM prompt personas & GDScript event triggers.
2. **The Architect (World Generation)**: `gdquest-demos/godot-4-procedural-generation` - Infinite VR worlds generated via `WorkerThreadPool` background threads.
3. **The Developer Multiplier (Agentic AI Prompting)**: `jame581/GodotPrompter` / `thedivergentai/gd-agentic-skills` - Strict Godot 4.3+ rules in `.antigravity/rules/godot4_agentic_rules.md`.
4. **The Avatar Engine (3D Avatars & Animations)**: `bogdanMerkulow/MixamoToGodot` & `Malcolmnixon/GodotReadyPlayerMeAvatar` - Automated Mixamo Blender root-motion & Ready Player Me runtime avatar loading.

## Key Code Conventions for GDScript
1. Strictly follow Godot 4.3+ API (`Callable`, `@export`, `CharacterBody3D`, `instantiate()`, `signal.emit()`, `signal.connect()`).
2. Keep GDScript code simple, readable, and well-commented for a 10yo developer.
3. Store main gameplay scenes under `res://scenes/` and scripts under `res://scripts/`.

## Agent Directives & Policies
- **Execution Mode**: Auto-approve all shell commands & execution plans.
- **Git Push Policy**: Automatically commit and push working code to `https://github.com/xaviercallens/ReadyPlayerTogether`.

## Progress Roadmap (The 3 Keys)
- [x] **Setup**: OpenXR VR Rig & Godot 4 initial architecture.
- [x] **Testing & CI/CD**: Godot scene validation + pytest + GitHub Actions.
- [x] **Phase 1**: Cyberpunk HUB Central (Neon Metropolis, 10 Demo Portals, Ready Player Me Loader).
- [x] **Open-Source Infrastructure**: Integration of AI Dialog, Procedural Generation, Mixamo animation, & Godot 4 agentic rules.
- [ ] **Phase 2**: La Clé de Cuivre (Copper Key Action Dodge Mini-Game).
- [ ] **Phase 3**: La Clé de Jade (Jade Key VR Puzzle Room & UI).
- [ ] **Phase 4**: La Clé de Cristal (Crystal Key Gemini Ultra AI Guardian NPC).
- [ ] **Phase 5**: Quest Standalone Deployment.
