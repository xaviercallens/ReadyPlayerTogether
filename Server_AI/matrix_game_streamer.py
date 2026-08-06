import asyncio
import time
import json
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI(
    title="OASIS Matrix-Game 2.0 Streaming Server",
    description="Real-time AI Video & Dimension Streamer for Godot Virtual Screens & Portals",
    version="2.0.0"
)

@app.get("/")
def root():
    return {
        "server": "Matrix-Game 2.0 Streamer",
        "status": "active",
        "target_fps": 25,
        "gpu": "NVIDIA GeForce RTX 2070"
    }

@app.websocket("/ws/stream")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()
    print("[MATRIX STREAMER] Godot Virtual Portal connected!")
    frame_count = 0
    try:
        while True:
            frame_count += 1
            # Send frame metadata & simulation packet to Godot
            packet = {
                "frame": frame_count,
                "timestamp": time.time(),
                "dimension": "Cyberpunk Neon Portal",
                "status": "streaming"
            }
            await websocket.send_text(json.dumps(packet))
            await asyncio.sleep(1.0 / 25.0) # 25 FPS Stream
    except WebSocketDisconnect:
        print("[MATRIX STREAMER] Godot Virtual Portal disconnected.")

if __name__ == "__main__":
    print("[MATRIX STREAMER] Starting server on ws://127.0.0.1:8001/ws/stream ...")
    uvicorn.run(app, host="127.0.0.1", port=8001)