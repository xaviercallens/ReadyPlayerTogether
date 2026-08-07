# GCP Gemini API Cloud Agent for Godot 4 NPCs
# Communicates with Google Gemini API for scalable NPC dialogue

import os
import asyncio

try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class GeminiCloudAgent:
    def __init__(self, project_id: str = "oasis-gcp-project", region: str = "us-central1"):
        self.project_id = project_id
        self.region = region
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.client = None

        if GENAI_AVAILABLE and self.api_key:
            self.client = genai.Client(api_key=self.api_key)
            print(f"[GeminiCloudAgent] Connected to Gemini API ({self.model_name}) in {self.region}")
        else:
            print("[GeminiCloudAgent] WARNING: Gemini SDK or API key unavailable. Using offline fallback.")

    async def generate_response(self, persona_prompt: str, user_speech: str) -> str:
        if self.client is None:
            return "L'OASIS fonctionne en mode local. Configurez GEMINI_API_KEY pour le mode cloud."

        prompt = (
            f"System: {persona_prompt}\n\n"
            f"User: {user_speech}\n\n"
            "Respond in character. Keep responses under 3 sentences for VR dialogue."
        )

        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                )
            )
            return response.text or "..."
        except Exception as e:
            print(f"[GeminiCloudAgent] API error: {e}")
            return f"Erreur de connexion au cloud Gemini: {e}"
