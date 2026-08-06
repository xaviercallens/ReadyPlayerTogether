# Projet OASIS - Context Memory for Antigravity & Windsurf Agents

## Project Overview
- **Team**: Father (Architect / ML Expert) & Son (Pilot / 10yo Developer).
- **Engine**: Godot Engine 4.x (GDScript, OpenXR enabled).
- **Target VR Headset**: Meta Quest 3S (Standalone & PCVR via Link on RTX 2070 GPU).
- **Aesthetic**: Low-Poly Retro Cyberpunk / Synthwave (Neon grid, glowing portals, synth soundscapes).
- **AI Stack**: GCP Gemini Ultra API (Dynamic quests/dialogue) + Google Flow / Imagen (Skybox/textures).

## Key Code Conventions for GDScript
1. Keep GDScript code simple, readable, and well-commented for a 10yo developer.
2. Use descriptive variable names (e.g. `var player_score = 0`, `var has_copper_key = false`).
3. Prefer signals for decoupled UI updates (`signal key_collected(key_name)`).
4. Store main gameplay scenes under `res://scenes/` and scripts under `res://scripts/`.

## Progress Roadmap (The 3 Keys)
- [x] **Setup**: OpenXR VR Rig & Godot 4 initial architecture.
- [ ] **Phase 1**: HUB Central (Halliday's Arcade Lounge).
- [ ] **Phase 2**: La Clé de Cuivre (Copper Key Action Dodge Mini-Game).
- [ ] **Phase 3**: La Clé de Jade (Jade Key VR Puzzle Room & UI).
- [ ] **Phase 4**: La Clé de Cristal (Crystal Key Gemini Ultra AI Guardian NPC).
- [ ] **Phase 5**: Quest Standalone Deployment.
