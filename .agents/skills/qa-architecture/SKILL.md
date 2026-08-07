---
name: qa-architecture
description: Trigger the Gemini 3.1 Pro background agent to conduct Code Reviews, Unit Tests, and Architectural improvements on Godot scripts.
---

# QA & Architecture Skill (Gemini 3.1 Pro)

This skill uses the **Unified OASIS AMCP Server** (`http://127.0.0.1:8005`) which hosts both the game mesh endpoints and the QA/Architecture endpoints. The QA agent runs as a background worker within the same server process, powered by the real Gemini API via `google-genai`.

## Prerequisites

- `GEMINI_API_KEY` environment variable must be set (or in `.env` file).
- Server running: `python Server_AI/agent_mesh/server.py`

## Usage

When the user asks to "review", "test", or "improve" a script:

1. Identify the target script path (relative to project root).
2. Send an HTTP POST request to the unified server's QA endpoints.

### Available Endpoints (all on port 8005):

| Endpoint | Purpose |
|----------|---------|
| `POST /api/qa/review` | Strict Godot 4 Code Review |
| `POST /api/qa/unittest` | GUT test file generation |
| `POST /api/qa/improve` | Architecture & pattern suggestions |
| `GET /api/vram/status` | Real-time GPU VRAM monitoring |

### Example:
```bash
# Code review
curl -X POST "http://127.0.0.1:8005/api/qa/review" \
  -H "Content-Type: application/json" \
  -d '{"file_path":"scripts/player/third_person_controller.gd"}'

# VRAM status
curl "http://127.0.0.1:8005/api/vram/status"
```

## Agent Behavior

- When the Gemini API key is configured, the agent sends real prompts to the Gemini model.
- When offline (no API key), it returns a clear message indicating the agent is unavailable.
- Results are returned asynchronously through a background worker queue.
