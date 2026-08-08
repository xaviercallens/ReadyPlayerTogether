# OASIS Architecture - La Fonderie IT Hybride

> L'objectif est de découpler totalement la génération d'assets (Backend) de l'affichage (Frontend) pour permettre une évolution de GenieRedux → GenieGodot → GenieOasis sans jamais refaire le backend.

---

## 1. Salle des Machines Invariable (Backend)

Ce backend reste **strictement inchangé** de la Phase 1 à la Phase 3.

### Composants

- **Orchestrateur** : Google Antigravity / serveur FastAPI central.
- **Entrées** : HTTP / WebSocket depuis le frontend (prompts, touches, état VR).
- **Moteurs IA** :
  - `Genie Sim` : génération 3D à partir de texte (USD / GLTF / GLB).
  - `Matrix-Game` : génération vidéo 2D interactive à 25 FPS.
  - `faster-whisper` : transcription vocale.
  - `RVC-WebUI` : synthèse vocale des PNJ.
  - `ComfyUI` / Stable Diffusion : génération de textures.
- **Sorties** : fichiers placés dans `assets/` (selon le format demandé).

### Contrat API

```
POST /api/v1/generate/world
{
  "prompt": "a giant robot in a cyberpunk plaza",
  "format": "glb",  // glb, usd, tscn, png
  "target_dir": "assets/genie_worlds/"
}

Response:
{
  "status": "ok",
  "asset_path": "assets/genie_worlds/giant_cyberpunk.glb",
  "format": "glb"
}
```

---

## 2. Poste de Pilotage Interchangeable (Frontend)

### GenieRedux (Phase 1)
- Captures les entrées clavier.
- Envoie via WebSocket au serveur.
- Affiche le flux vidéo renvoyé dans une `TextureRect`.

### GenieGodot (Phase 2)
- Envoie un prompt textuel depuis l'interface VR.
- Backend génère le fichier 3D.
- Godot charge via `GLTFDocument.append_from_file()` ou une scène `.tscn`.

### GenieOasis (Phase 3)
- Unreal Engine 5 interroge la même API.
- Télécharge l'environnement généré en USD.
- Applique Lumen, Nanite et shaders holographiques.

---

## 3. Découpage des dossiers

```
Oasis/
├── Server_AI/              # Fonderie - NE PAS TOUCHER entre les phases
│   ├── fonderie_oasis_api.py
│   ├── Matrix-Game/
│   ├── open_genie/
│   ├── faster-whisper/
│   └── RVC-WebUI/
├── assets/                  # Sorties de la Fonderie
│   ├── genie_worlds/        # Mondes générés
│   ├── iron_giant/
│   └── oasis_batch/         # Scènes converties
├── scenes/                  # Scènes Godot (GenieGodot)
├── scripts/                 # Logique Godot
├── docs/                    # Roadmap & Architecture
└── unreal/                  # Futures ressources UE5 (GenieOasis)
```

---

## 4. Flux de données

```
[Pilote clavier/VR] → [Frontend Redux/Godot/UE5]
                              ↓
                  [WebSocket / HTTP]
                              ↓
                [FastAPI - Fonderie OASIS]
                              ↓
        [Genie Sim / Matrix-Game / Whisper / RVC]
                              ↓
                      [assets/]
                              ↓
                [Frontend charge et affiche]
```

---

## 5. Principes de conception

1. **Backend stable, frontend interchangeable**.
2. **Format d'asset piloté par le frontend** (`glb` pour Godot, `usd` pour UE5, `png` pour Redux).
3. **Aucun fichier binaire lourd dans Git** (GLB, USD, textures générées) — ils sont générés ou téléchargés à la volée.
4. **Cache local** dans `assets/` pour éviter de regénérer un asset déjà existant.
