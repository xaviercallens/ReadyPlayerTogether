# Matrix-Game 2.0 WebSocket Streamer (The Dreamer)
# Simulates interactive 25 FPS playable video hallucinated by AI on the RTX 2070.

import asyncio
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import cv2
import numpy as np

app = FastAPI(title="Matrix-Game Dream Streamer")

def generate_noise_frame(width=320, height=240, text="MATRIX GAME 2.0"):
    """Simule une frame d'IA générative (bruit + texte de debug)"""
    frame = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    # Ajouter un effet cyberpunk
    frame[:, :, 1] = 0 # Pas de vert, que du violet/magenta
    cv2.putText(frame, text, (20, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    
    # Encode as JPEG
    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
    return buffer.tobytes()

@app.websocket("/ws/dream_portal")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("[Matrix-Game] Portal connection established. Dreaming at 25 FPS...")
    
    try:
        while True:
            # 1. Attendre les inputs du joueur (ex: W, A, S, D) depuis Godot
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=0.04) # ~25fps non bloquant
                print(f"[Matrix-Game] Player Input: {data}")
            except asyncio.TimeoutError:
                pass # Continue generating frames even if no input
                
            # 2. L'IA génère la prochaine frame (Simulation)
            # Dans un vrai scénario, Matrix-Game prend `data` et infère la vidéo
            jpeg_bytes = generate_noise_frame(text=f"DREAMING... {int(time.time()*10)%100}")
            
            # 3. Envoyer la frame à Godot
            await websocket.send_bytes(jpeg_bytes)
            
            await asyncio.sleep(0.04) # Lock à ~25 FPS pour épargner la RTX 2070
    except WebSocketDisconnect:
        print("[Matrix-Game] Player disconnected from the dream portal.")

if __name__ == "__main__":
    print("[Matrix-Game Streamer] Ready on ws://127.0.0.1:8006/ws/dream_portal")
    uvicorn.run(app, host="127.0.0.1", port=8006)
