# Ollama Local LLM Agent for Godot 4 NPCs
# Communicates with local Ollama server (Llama 3 / Mistral 4-bit) ~4.5GB VRAM

import httpx
import json

class OllamaDialogueAgent:
    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "llama3:8b-instruct-q4_0"):
        self.ollama_url = ollama_url
        self.model = model

    async def generate_response(self, persona_prompt: str, user_speech: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": persona_prompt},
                {"role": "user", "content": user_speech}
            ],
            "stream": False
        }
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(f"{self.ollama_url}/api/chat", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    return data.get("message", {}).get("content", "L'OASIS vous salue!")
        except Exception as e:
            print(f"[OllamaAgent] Connection error or offline fallback: {e}")
            
        return "Bienvenue dans l'OASIS! (Mode local Ollama prêt)."
