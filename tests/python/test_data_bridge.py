import pytest
from fastapi.testclient import TestClient
from Server_AI.oasis_data_bridge_server import app

client = TestClient(app)

def test_bridge_status():
    res = client.get("/api/bridge/status")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"
    assert "gpu" in data

def test_bridge_mesh():
    res = client.post("/api/bridge/mesh", json={"prompt": "cyberpunk_hoverboard"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "res_path" in data

def test_bridge_pbr():
    res = client.post("/api/bridge/pbr", json={"asset_name": "hoverboard"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"

def test_bridge_skybox():
    res = client.post("/api/bridge/skybox", json={"prompt": "Tokyo skyline"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"