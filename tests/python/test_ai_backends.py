import os
import sys
import pytest

# Add project root to sys.path to import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Server_AI.gemini_ultra_quest_engine import GeminiQuestEngine
from GenAI_Pipeline.google_flow_imagen import GoogleFlowAssetPipeline

def test_gemini_engine_initialization():
    engine = GeminiQuestEngine(project_id="test-project", location="us-central1")
    assert engine.project_id == "test-project"
    assert engine.location == "us-central1"

def test_gemini_dialogue_generation():
    engine = GeminiQuestEngine(project_id="test-project")
    response = engine.generate_npc_dialogue("Looked at the door", "Copper Key")
    
    assert "speaker" in response
    assert response["speaker"] == "Guardian PNJ"
    assert "dialogue" in response
    assert "unlocked_next_step" in response
    assert response["unlocked_next_step"] is True

def test_google_flow_pipeline():
    pipeline = GoogleFlowAssetPipeline(session_token="fake_token_123")
    assert pipeline.session_token == "fake_token_123"
    
    tex_response = pipeline.generate_avatar_texture("Cyberpunk jacket")
    assert tex_response["status"] == "success"
    assert tex_response["texture_file"] == "avatar_skin.png"
    
    sky_response = pipeline.generate_skybox_hdri("Planet Doom")
    assert sky_response["status"] == "success"
    assert "skybox_file" in sky_response
    assert sky_response["skybox_file"] == "skybox_planet_doom.png"
