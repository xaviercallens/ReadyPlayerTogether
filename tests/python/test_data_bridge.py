import requests
import unittest

class TestOasisDataBridge(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:8000"

    def test_bridge_endpoints(self):
        # 1. Mesh Endpoint
        mesh_res = requests.post(f"{self.BASE_URL}/api/bridge/mesh", json={"prompt": "cyberpunk_hoverboard"})
        self.assertEqual(mesh_res.status_code, 200)
        self.assertIn("res_path", mesh_res.json())

        # 2. PBR Textures Endpoint
        pbr_res = requests.post(f"{self.BASE_URL}/api/bridge/pbr", json={"asset_name": "hoverboard"})
        self.assertEqual(pbr_res.status_code, 200)

        # 3. Skybox Endpoint
        sky_res = requests.post(f"{self.BASE_URL}/api/bridge/skybox", json={"prompt": "Tokyo skyline"})
        self.assertEqual(sky_res.status_code, 200)

if __name__ == "__main__":
    print("[TEST DATA BRIDGE] Running integration tests...")
    unittest.main()