#!/usr/bin/env python3
"""
Fonderie OASIS - Backend API unifié pour GenieRedux, GenieGodot et GenieOasis.

Ce serveur FastAPI agit comme la "Salle des Machines Invariable".
Il est indépendant du frontend (2D, Godot VR, Unreal Engine 5).
"""

import os
import asyncio
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(
    title="Fonderie OASIS",
    description="Backend unifié de génération d'assets pour OASIS.",
    version="0.1.0"
)

BASE_DIR = Path(r"D:\xdev\Oasis")
ASSETS_DIR = BASE_DIR / "assets"


class GenerationRequest(BaseModel):
    prompt: str
    format: Literal["glb", "usd", "tscn", "png"]
    target_dir: str = "assets/genie_worlds"
    cache: bool = True


class GenerationResponse(BaseModel):
    status: str
    asset_path: str
    format: str
    url: str


@app.get("/")
async def root():
    return {"message": "Fonderie OASIS opérationnelle", "phases": ["GenieRedux", "GenieGodot", "GenieOasis"]}


@app.post("/api/v1/generate/world", response_model=GenerationResponse)
async def generate_world(request: GenerationRequest):
    """
    Génère un asset 3D ou 2D à partir d'un prompt textuel.
    Le format détermine le moteur à utiliser.
    """
    target = BASE_DIR / request.target_dir
    target.mkdir(parents=True, exist_ok=True)

    # TODO: brancher les vrais moteurs (Genie Sim, Matrix-Game, etc.)
    if request.format == "png":
        # Phase 1 : Matrix-Game génère une image
        output_path = target / "generated_world.png"
    elif request.format in ("glb", "usd", "tscn"):
        # Phase 2/3 : Genie Sim génère la géométrie 3D
        output_path = target / f"generated_world.{request.format}"
    else:
        raise HTTPException(status_code=400, detail=f"Format non supporté: {request.format}")

    # Placeholder : en vrai, appeler le moteur correspondant
    if not output_path.exists():
        # Créer un fichier vide pour le développement
        output_path.write_text("")

    return GenerationResponse(
        status="ok",
        asset_path=str(output_path.relative_to(BASE_DIR)).replace("\\", "/"),
        format=request.format,
        url=f"/api/v1/assets/{output_path.relative_to(BASE_DIR).as_posix()}"
    )


@app.get("/api/v1/assets/{path:path}")
async def serve_asset(path: str):
    """Sert un asset généré (GLB, USD, PNG, etc.)."""
    file_path = BASE_DIR / path
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Asset non trouvé")
    return FileResponse(file_path)


@app.websocket("/ws/matrix-game")
async def matrix_game_stream(websocket):
    """Flux interactif Matrix-Game pour GenieRedux (Phase 1)."""
    await websocket.accept()
    try:
        while True:
            # Attend les frappes clavier du frontend
            data = await websocket.receive_text()
            # TODO: envoyer à Matrix-Game et renvoyer l'image encodée
            await websocket.send_text(f"frame:{data}")
    except Exception:
        pass
    finally:
        await websocket.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8766)
