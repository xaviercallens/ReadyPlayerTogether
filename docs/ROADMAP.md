# OASIS Roadmap - De Redux à Unreal Engine

> Roadmap évolutive pour monter en compétence progressivement : du flux 2D rétro à la VR Godot, puis au photoréalisme Unreal Engine 5.

## Team Roles

- **Pilote (Fils, 10 ans)** : Gameplay, level design, interactions, logique visuelle/Blueprint.
- **Navigateur (Père, ML Expert)** : Architecture, pipeline VR, IA générative, orchestration backend.

---

## Phase 1 : GenieRedux (L'Ère Rétro / Arcade)

**Objectif** : Maîtriser la logique de jeu de base et la génération de mondes interactifs sans la complexité de la 3D physique.

**Technologie** : Matrix-Game 2.0 - génération de flux vidéo interactif à 25 FPS à partir des entrées clavier.

- Pas de polygones, pas de moteur 3D lourd.
- Frontend 2D simple (TextureRect / canvas) affichant le flux.
- Backend Python renvoie une image générée en fonction des touches pressées.

**Stack** :
- `Server_AI/Matrix-Game/`
- `scripts/redux/matrix_game_client.gd`

**Livrable** : Un mini-jeu 2D jouable au clavier, généré par IA en temps réel.

---

## Phase 2 : GenieGodot (Immersion VR & 3D Légère)

**Objectif** : Basculer vers la réalité virtuelle, la vraie géométrie 3D et le multijoueur.

**Technologie Frontend** : Godot 4.7+ avec Forward+ / Mobile rendering, optimisé pour Meta Quest 3S.

- Plugin `godot-xr-tools` pour la physique des mains, déplacements et collisions.
- Prévisualisation VR via `scenes/player_vr/pc_player.tscn`.

**Technologie Backend** : Genie Sim (AgibotTech) pour transformer des prompts textuels en environnements 3D (USD / GLTF / GLB).

- Génération asynchrone dans `assets/genie_worlds/`.
- Import runtime via `GLTFDocument.append_from_file()` pour instancier les scènes en direct.

**Automatisation** :
- `fetch_mechas.py` : téléchargement depuis Google Drive.
- `force_glb_to_tscn.gd` : conversion GLB → TSCN native.
- `oasis_asset_manager.gd` : analyse des mots-clés (`giant`, `hovercar`), ajustement d'échelle, ajout de composants physiques.

**Livrable** : Le projet actuel OASIS, jouable en VR avec des PNJ (Parzival, Iron Giant, DeLorean, etc.).

---

## Phase 3 : GenieOasis (Photoréalisme Unreal Engine 5)

**Objectif** : Atteindre une qualité visuelle AAA avec éclairage dynamique, Nanite et shaders avancés.

**Technologie Frontend** : Unreal Engine 5.

- Lumen pour l'éclairage global.
- Nanite pour les géométries complexes.
- Shaders holographiques de matérialisation (effet DeLorean).

**Intégration** : UE5 interroge la même API FastAPI, télécharge les environnements générés au format USD, applique Lumen et les shaders.

**Livrable** : Une expérience Ready Player One en photoréalisme.

---

## Transitions

Chaque phase réutilise la **Salle des Machines Invariable** (backend FastAPI / Python). Seul le **Poste de Pilotage** (frontend) évolue.

| Phase | Frontend | Backend | Format d'asset |
|-------|----------|---------|----------------|
| GenieRedux | TextureRect 2D | Matrix-Game | Images 25 FPS |
| GenieGodot | Godot 4 VR | Genie Sim | GLB / GLTF / TSCN |
| GenieOasis | Unreal Engine 5 | Genie Sim | USD / FBX |
