# 🏛️ Projet OASIS - Architecture Master & Orchestrateur Backend

Ce document définit l'architecture hybride entre le copilote (développeur de 10 ans sur Windsurf) et la Salle des Machines (Google Antigravity & FastAPI Backend).

---

### 🧱 I. Les 4 Piliers GitHub du Projet

1. **La Fondation (`xaviercallens/ReadyPlayerTogether`)** :
   - Dépôt maître du jeu Godot 4.
   - Scènes découpées par quêtes (`scenes/hub/`, `scenes/demos/`, `scenes/artifacts/`).
   - Contient l'infrastructure IA sous `Server_AI/` et `scripts/ai/`.

2. **Gestion des Avatars & Lip-Sync (Visemes & Blendshapes)** :
   - Intégration des avatars Ready Player Me (`scenes/characters/`).
   - Endpoint FastAPI `/api/lipsync` pour l'animation buccale automatisée.

3. **L'Architecte 3D (Génération de Mondes & Objets)** :
   - Serveur FastAPI local (`Server_AI/oasis_fastapi_server.py`).
   - Chargement dynamique à l'exécution via la classe `GLTFDocument` de Godot (`scripts/ai/runtime_asset_loader.gd`).

4. **Référence Pédagogique (Ateliers GDScript)** :
   - Basé sur les dépôts de référence `Godot-Ready-Player-One` (`Workshop-3` & `Workshop-4`).

---

### ⚙️ II. Serveur Backend FastAPI
- URL locale : `http://127.0.0.1:8000`
- Fichier : [Server_AI/oasis_fastapi_server.py](file:///D:/xdev/Oasis/Server_AI/oasis_fastapi_server.py)