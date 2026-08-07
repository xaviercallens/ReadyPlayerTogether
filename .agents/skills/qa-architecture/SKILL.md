---
name: qa-architecture
description: Trigger the Gemini 3.1 Pro background agent to conduct Code Reviews, Unit Tests, and Architectural improvements on Godot scripts.
---

# QA & Architecture Skill (Gemini 3.1 Pro)

This skill interfaces with the local FastAPI server (`http://127.0.0.1:8007`) that acts as a proxy to the GCP Vertex AI Gemini 3.1 Pro model.

## Usage

When the user asks to "review", "test", or "improve" a script, you should:

1. Identify the target script path.
2. Send an HTTP POST request (via a curl command or python script) to the local QA server.

### Available Endpoints:
- `/api/qa/review`: Returns a strict Godot 4 Code Review.
- `/api/qa/unittest`: Generates a GUT (Godot Unit Test) framework file.
- `/api/qa/improve`: Suggests architectural patterns (State Machines, Component architecture).

### Example (Curl):
```bash
curl -X POST "http://127.0.0.1:8007/api/qa/improve" -H "Content-Type: application/json" -d '{"file_path":"scripts/player/third_person_controller.gd"}'
```
