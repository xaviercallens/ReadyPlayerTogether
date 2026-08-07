import pytest
import asyncio
import os
import tempfile
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

# Import modules to test
from Server_AI.agent_mesh.broker import VRAMGovernor, AgentMeshBroker
from Server_AI.agent_mesh.ollama_agent import OllamaDialogueAgent
from Server_AI.agent_mesh.gemini_cloud_agent import GeminiCloudAgent
from Server_AI.agent_mesh.comfyui_agent import ComfyUITextureAgent
from Server_AI.agent_mesh.rvc_agent import RVCVoiceAgent
from Server_AI.agent_mesh.godot_rl_agent import GodotRLAgent
from Server_AI.gemini_qa_agent import GeminiQAAgent, QAskillsWorker
from Server_AI.gemini_ultra_quest_engine import GeminiQuestEngine
from Server_AI.ml_foundry_pipeline import run_sf3d_triposr_pipeline
from Server_AI.matrix_game_streamer import app as streamer_app, generate_noise_frame
from Server_AI.gemini_qa_server import app as qa_server_app
from Server_AI.oasis_fastapi_server import app as legacy_app
from Server_AI.agent_mesh.server import app as mesh_app


# ============================================================================
# 1. VRAMGovernor & AgentMeshBroker Tests
# ============================================================================
def test_vram_governor_allocation_and_release():
    gov = VRAMGovernor(max_vram_gb=7.5)
    assert gov.request_allocation("model_a", 3.0) is True
    assert gov.request_allocation("model_b", 4.0) is True
    # Total used = 7.0, allocating 1.0 exceeds 7.5
    assert gov.request_allocation("model_c", 1.0) is False

    status = gov.status()
    assert status["max_vram_gb"] == 7.5
    assert status["estimated_vram_used_gb"] == 7.0
    assert "model_a" in status["active_models"]

    gov.release_allocation("model_a")
    assert "model_a" not in gov.active_models
    assert gov.get_estimated_vram_used_gb() == 4.0


def test_vram_governor_with_pynvml_mock():
    mock_pynvml = MagicMock()
    mock_pynvml.nvmlDeviceGetMemoryInfo.return_value = MagicMock(total=8*1024**3, used=2*1024**3)

    with patch("Server_AI.agent_mesh.broker.pynvml", mock_pynvml, create=True):
        gov = VRAMGovernor(max_vram_gb=7.5)
        gov._handle = MagicMock()
        assert gov.get_real_vram_used_gb() == 2.0
        assert gov.get_effective_vram_used_gb() == 2.0


@pytest.mark.asyncio
async def test_agent_mesh_broker_pub_sub_and_dead_letter():
    broker = AgentMeshBroker()
    received = []

    async def good_handler(payload):
        received.append(payload)

    async def bad_handler(payload):
        raise ValueError("Simulated handler crash")

    broker.subscribe("speech_event", good_handler)
    broker.subscribe("speech_event", bad_handler)

    await broker.publish("speech_event", {"text": "hello"})
    await asyncio.sleep(0.05)

    assert len(received) == 1
    assert received[0]["text"] == "hello"
    assert len(broker.failed_events) == 1
    assert broker.failed_events[0]["error"] == "Simulated handler crash"


# ============================================================================
# 2. Individual Agent Tests
# ============================================================================
@pytest.mark.asyncio
async def test_ollama_dialogue_agent_fallback():
    agent = OllamaDialogueAgent(ollama_url="http://invalid_host:9999")
    resp = await agent.generate_response("System persona", "Player text")
    assert isinstance(resp, str)
    assert len(resp) > 0


@pytest.mark.asyncio
async def test_gemini_cloud_agent_without_key():
    agent = GeminiCloudAgent()
    agent.client = None  # Ensure fallback
    resp = await agent.generate_response("Persona", "Speech")
    assert "local" in resp or "mode" in resp.lower()


@pytest.mark.asyncio
async def test_gemini_cloud_agent_with_mock_client():
    agent = GeminiCloudAgent()
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Hello from Gemini Cloud!"
    mock_client.models.generate_content.return_value = mock_response
    agent.client = mock_client

    resp = await agent.generate_response("Persona", "Speech")
    assert resp == "Hello from Gemini Cloud!"


@pytest.mark.asyncio
async def test_comfyui_agent():
    agent = ComfyUITextureAgent()
    res = await agent.generate_pbr_material("cyberpunk metal")
    assert res["status"] == "success"
    assert res["material_name"] == "cyberpunk_metal"
    assert "albedo_map" in res


@pytest.mark.asyncio
async def test_rvc_agent():
    agent = RVCVoiceAgent()
    audio_path = await agent.synthesize_character_voice("Hello world", "parzival")
    assert audio_path == "res://assets/audio/npc_parzival_speech.wav"


def test_godot_rl_agent():
    rl = GodotRLAgent()
    action = rl.get_action([0.1, 0.2, 0.3])
    assert action == [0.0, 0.8, 0.0]
    rl.log_reward(1.5)


# ============================================================================
# 3. Gemini QA Agent & Worker Tests
# ============================================================================
@pytest.mark.asyncio
async def test_gemini_qa_agent_offline_fallbacks():
    agent = GeminiQAAgent()
    agent.client = None
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".gd", encoding="utf-8") as f:
        f.write("extends Node\nfunc _ready(): pass\n")
        f_path = f.name

    try:
        rev = await agent.review_code(f_path)
        assert "[Offline]" in rev

        unit = await agent.generate_unittest(f_path)
        assert "[Offline]" in unit

        imp = await agent.improve_architecture(f_path)
        assert "[Offline]" in imp
    finally:
        if os.path.exists(f_path):
            os.remove(f_path)


@pytest.mark.asyncio
async def test_gemini_qa_agent_with_mock_client():
    agent = GeminiQAAgent()
    mock_client = MagicMock()
    mock_resp = MagicMock()
    mock_resp.text = "GUT Test Code Generated"
    mock_client.models.generate_content.return_value = mock_resp
    agent.client = mock_client

    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".gd", encoding="utf-8") as f:
        f.write("extends Node\n")
        f_path = f.name

    try:
        res = await agent.review_code(f_path)
        assert res == "GUT Test Code Generated"
    finally:
        if os.path.exists(f_path):
            os.remove(f_path)


@pytest.mark.asyncio
async def test_qa_worker_queue_processing():
    worker = QAskillsWorker()
    worker.agent.client = None  # Use offline fallback

    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".gd", encoding="utf-8") as f:
        f.write("extends CharacterBody3D\n")
        f_path = f.name

    try:
        # Test worker execution loop with task
        results = []
        def callback(res):
            results.append(res)

        await worker.queue.put({"type": "review", "file": f_path, "callback": callback})
        await worker.queue.put({"type": "unittest", "file": f_path, "callback": callback})
        await worker.queue.put({"type": "improve", "file": f_path, "callback": callback})
        await worker.queue.put({"type": "unknown", "file": f_path, "callback": callback})

        # Process queued tasks manually via internal method
        while not worker.queue.empty():
            task = await worker.queue.get()
            await worker._handle_task(task)
            worker.queue.task_done()

        assert len(results) == 4
        assert "[Offline]" in results[0]
        assert "Unsupported task type" in results[3]
    finally:
        if os.path.exists(f_path):
            os.remove(f_path)


# ============================================================================
# 4. Quest Engine & ML Foundry Pipeline Tests
# ============================================================================
def test_gemini_quest_engine():
    engine = GeminiQuestEngine(project_id="oasis-test")
    res = engine.generate_npc_dialogue("Looked at portal", "Jade Key")
    assert res["speaker"] == "Guardian PNJ"
    assert "Jade Key" in res["dialogue"]
    assert res["unlocked_next_step"] is True


def test_sf3d_pipeline():
    with tempfile.TemporaryDirectory() as tmpdir:
        glb_path = run_sf3d_triposr_pipeline("laser sword", output_dir=tmpdir)
        assert os.path.exists(glb_path)
        meta_path = os.path.join(tmpdir, "laser_sword.json")
        assert os.path.exists(meta_path)


# ============================================================================
# 5. FastAPI Endpoints & Streamer Tests
# ============================================================================
def test_matrix_game_streamer():
    frame = generate_noise_frame()
    assert isinstance(frame, bytes)
    assert len(frame) > 0

    client = TestClient(streamer_app)
    with client.websocket_connect("/ws/dream_portal") as websocket:
        websocket.send_text("W")
        data = websocket.receive_bytes()
        assert isinstance(data, bytes)
        assert len(data) > 0


def test_legacy_fastapi_server():
    client = TestClient(legacy_app)
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "online"

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "healthy"

    asset_res = client.post("/api/generate_asset", json={"prompt": "cyberpunk hoverboard"})
    assert asset_res.status_code == 200
    assert asset_res.json()["status"] == "success"

    lipsync_res = client.post("/api/lipsync", json={"text": "hello", "avatar_id": "parzival"})
    assert lipsync_res.status_code == 200
    assert len(lipsync_res.json()["viseme_keyframes"]) > 0


def test_qa_fastapi_server():
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".gd", encoding="utf-8") as f:
        f.write("extends Node\n")
        f_path = f.name

    try:
        with TestClient(qa_server_app) as client:
            rev_res = client.post("/api/qa/review", json={"file_path": f_path})
            assert rev_res.status_code == 200
            assert "result" in rev_res.json()

            unit_res = client.post("/api/qa/unittest", json={"file_path": f_path})
            assert unit_res.status_code == 200

            imp_res = client.post("/api/qa/improve", json={"file_path": f_path})
            assert imp_res.status_code == 200
    finally:
        if os.path.exists(f_path):
            os.remove(f_path)


def test_unified_mesh_server_endpoints():
    with TestClient(mesh_app) as client:
        # 1. Index / Web interface HTML
        res = client.get("/")
        assert res.status_code == 200

        api_res = client.get("/api/status")
        assert api_res.status_code == 200
        assert "system" in api_res.json()

        # 2. VRAM Status
        vram_res = client.get("/api/vram/status")
        assert vram_res.status_code == 200
        assert "max_vram_gb" in vram_res.json()

        # 3. Speak endpoint
        speak_res = client.post("/api/mesh/speak", json={
            "npc_name": "Parzival",
            "persona": "Gunter warrior",
            "player_text": "Where is the Copper Key?",
            "session_id": "test_sess_1"
        })
        assert speak_res.status_code == 200
        assert speak_res.json()["status"] == "success"
        assert "reply_text" in speak_res.json()

        # 4. Generate PBR endpoint
        pbr_res = client.post("/api/mesh/generate_pbr", json={
            "material_prompt": "neon grid floor"
        })
        assert pbr_res.status_code == 200
        assert pbr_res.json()["material_name"] == "neon_grid_floor"

        # 5. QA endpoints on unified server
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".gd", encoding="utf-8") as f:
            f.write("extends Node\n")
            f_path = f.name

        try:
            qa_rev = client.post("/api/qa/review", json={"file_path": f_path})
            assert qa_rev.status_code == 200
            assert "result" in qa_rev.json()
        finally:
            if os.path.exists(f_path):
                os.remove(f_path)


# ============================================================================
# 6. Additional Coverage & Edge Case Tests
# ============================================================================
@pytest.mark.asyncio
async def test_ollama_agent_non_200_response():
    agent = OllamaDialogueAgent()
    mock_resp = MagicMock()
    mock_resp.status_code = 500

    with patch("httpx.AsyncClient.post", return_value=mock_resp):
        res = await agent.generate_response("Persona", "Text")
        assert "mode" in res.lower() or "local" in res.lower()


@pytest.mark.asyncio
async def test_gemini_qa_agent_api_exception():
    agent = GeminiQAAgent()
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = RuntimeError("API rate limit")
    agent.client = mock_client

    res = await agent._call_gemini_api("review code")
    assert "[Gemini QA Error]" in res


def test_gemini_qa_agent_general_offline_fallback():
    agent = GeminiQAAgent()
    agent.client = None
    res = agent._offline_fallback("custom prompt")
    assert "[Offline]" in res


@pytest.mark.asyncio
async def test_qa_worker_no_callback_printing():
    worker = QAskillsWorker()
    worker.agent.client = None

    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".gd", encoding="utf-8") as f:
        f.write("extends Node\n")
        f_path = f.name

    try:
        # Task without callback
        await worker._handle_task({"type": "review", "file": f_path, "callback": None})
    finally:
        if os.path.exists(f_path):
            os.remove(f_path)


def test_vram_governor_handle_exception():
    mock_pynvml = MagicMock()
    mock_pynvml.nvmlDeviceGetHandleByIndex.side_effect = RuntimeError("No GPU handle")

    with patch("Server_AI.agent_mesh.broker.pynvml", mock_pynvml, create=True):
        with patch("Server_AI.agent_mesh.broker.PYNVML_AVAILABLE", True):
            gov = VRAMGovernor(max_vram_gb=7.5)
            assert gov._handle is None
            assert gov.get_real_vram_used_gb() == -1.0


@pytest.mark.asyncio
async def test_gemini_cloud_agent_exception_and_init():
    with patch("Server_AI.agent_mesh.gemini_cloud_agent.GENAI_AVAILABLE", True):
        with patch("os.getenv", side_effect=lambda k, d="": "fake_key" if k == "GEMINI_API_KEY" else d):
            with patch("google.genai.Client", create=True) as mock_genai_client:
                mock_client = MagicMock()
                mock_client.models.generate_content.side_effect = RuntimeError("Quota exceeded")
                mock_genai_client.return_value = mock_client

                agent = GeminiCloudAgent()
                assert agent.client is not None
                res = await agent.generate_response("Persona", "Speech")
                assert "Erreur de connexion" in res


def test_main_block_executions():
    # 1. GeminiQuestEngine main block simulation
    engine = GeminiQuestEngine()
    dlg = engine.generate_npc_dialogue("test action", "Copper Key")
    assert "dialogue" in dlg

    # 2. ML Foundry pipeline main block simulation
    with tempfile.TemporaryDirectory() as tmpdir:
        res = run_sf3d_triposr_pipeline("test prop", output_dir=tmpdir)
        assert os.path.exists(res)


