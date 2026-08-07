# Gemini QA & Architecture Agent (Cloud Mode)
# Leverages Google Gemini API for deep code review,
# architecture improvements, and unit-test generation.
import os
import asyncio
from pathlib import Path
from typing import Optional

# Real Gemini SDK (google-genai)
try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    print("[Gemini QA] WARNING: google-genai not installed. Run: pip install google-genai")


class GeminiQAAgent:
    def __init__(self):
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.client: Optional[object] = None

        if GENAI_AVAILABLE and self.api_key:
            self.client = genai.Client(api_key=self.api_key)
            print(f"[Gemini QA] Connected to Gemini API with model: {self.model_name}")
        elif not self.api_key:
            print("[Gemini QA] WARNING: GEMINI_API_KEY not set. Agent will return offline fallback responses.")
        else:
            print("[Gemini QA] WARNING: google-genai SDK unavailable. Agent will return offline fallback responses.")

    async def _call_gemini_api(self, prompt: str) -> str:
        """Call the real Gemini API or return a fallback if unavailable."""
        if self.client is None:
            return self._offline_fallback(prompt)

        try:
            # Run the synchronous SDK call in a thread to avoid blocking the event loop
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                )
            )
            return response.text or "(Empty response from Gemini)"
        except Exception as e:
            print(f"[Gemini QA] API call failed: {e}")
            return f"[Gemini QA Error] {e}"

    def _offline_fallback(self, prompt: str) -> str:
        """Return a minimal offline fallback when no API key is configured."""
        if "review" in prompt.lower():
            return "[Offline] Code review unavailable. Set GEMINI_API_KEY to enable."
        elif "unittest" in prompt.lower() or "test" in prompt.lower():
            return "[Offline] Unit test generation unavailable. Set GEMINI_API_KEY to enable."
        elif "improve" in prompt.lower() or "architecture" in prompt.lower():
            return "[Offline] Architecture improvements unavailable. Set GEMINI_API_KEY to enable."
        return "[Offline] Gemini agent is offline. Set GEMINI_API_KEY to enable."

    async def review_code(self, file_path: str) -> str:
        code = Path(file_path).read_text(encoding="utf-8")
        prompt = (
            "You are an expert Godot 4 / GDScript code reviewer. "
            "Perform a strict code review of the following script. "
            "Point out bugs, null-safety issues, performance concerns, "
            "incorrect API usage for Godot 4.3+, and style issues. "
            "Be concise and actionable.\n\n"
            f"```gdscript\n{code}\n```"
        )
        return await self._call_gemini_api(prompt)

    async def generate_unittest(self, file_path: str) -> str:
        code = Path(file_path).read_text(encoding="utf-8")
        prompt = (
            "You are an expert Godot 4 test engineer using the GUT framework. "
            "Generate a complete GUT test file (.gd) for the following script. "
            "Include tests for all public functions and edge cases. "
            "Use extends GutTest, assert_eq, assert_true, assert_not_null.\n\n"
            f"```gdscript\n{code}\n```"
        )
        return await self._call_gemini_api(prompt)

    async def improve_architecture(self, file_path: str) -> str:
        code = Path(file_path).read_text(encoding="utf-8")
        prompt = (
            "You are an expert Godot 4 architect. "
            "Suggest concrete architectural improvements for the following script: "
            "Design patterns (State Machine, Component, Observer), "
            "refactorings, Godot 4.3+ API best practices, and performance tweaks. "
            "Return the improved code with comments explaining each change.\n\n"
            f"```gdscript\n{code}\n```"
        )
        return await self._call_gemini_api(prompt)


# Background Worker asynchrone pour traiter la file d'attente
class QAskillsWorker:
    def __init__(self):
        self.queue: asyncio.Queue = asyncio.Queue()
        self.running = False
        self.agent = GeminiQAAgent()

    async def start(self):
        self.running = True
        print("[QAskillsWorker] Background Worker started (Gemini API)...")
        while self.running:
            task = await self.queue.get()
            try:
                await self._handle_task(task)
            except Exception as e:
                print(f"[QAskillsWorker] Error processing task: {e}")
            finally:
                self.queue.task_done()

    async def stop(self):
        self.running = False

    async def _handle_task(self, task: dict):
        task_type = task.get("type")
        file_path = task.get("file")
        callback = task.get("callback")

        result = ""
        if task_type == "review":
            result = await self.agent.review_code(file_path)
        elif task_type == "unittest":
            result = await self.agent.generate_unittest(file_path)
        elif task_type == "improve":
            result = await self.agent.improve_architecture(file_path)
        else:
            result = f"Unsupported task type: {task_type}"

        if callable(callback):
            callback(result)
        else:
            print(f"\n[Gemini -> {task_type}] Result for {file_path}:\n{result}\n")
