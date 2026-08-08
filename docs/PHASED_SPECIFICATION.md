# OASIS - Spécification Phasée (Phased Specification)

> Document de référence technique liant la [Roadmap](ROADMAP.md), l'[Architecture](ARCHITECTURE.md) et un plan d'exécution avec critères d'acceptation, jalons et tâches GitHub.

**Statut du projet** : Phase 2 (GenieGodot) en cours.
**Dernière mise à jour** : Août 2026.

---

## Vue d'ensemble des phases

| Phase | Nom | Statut | Jalon GitHub |
|-------|-----|--------|--------------|
| 0 | Fondations | ✅ Terminé | `v0.1-fondations` |
| 1 | GenieRedux | 🟡 En cours (démo RTX 2070) | `v1.0-genieredux` |
| 2 | GenieGodot | 🟡 En cours (Iron Giant intégré) | `v2.0-geniegodot` |
| 3 | GenieOasis | ⚪ Planifié | `v3.0-genieoasis` |

---

## Phase 0 : Fondations

**Objectif** : Poser l'architecture Backend/Frontend découplée et le squelette du projet Godot.

### Livrables
- [x] Structure du dépôt `ReadyPlayerTogether` (`Hub/`, `scenes/`, `scripts/`, `Server_AI/`)
- [x] `Server_AI/fonderie_oasis_api.py` — squelette FastAPI unifié
- [x] `docs/ROADMAP.md` et `docs/ARCHITECTURE.md`
- [x] Intégration Git + `.gitignore` (exclusion des binaires lourds)

### Critères d'acceptation
- Le dépôt se clone et s'ouvre dans Godot 4.7+ sans erreur bloquante.
- `python Server_AI/fonderie_oasis_api.py` démarre sans exception.

---

## Phase 1 : GenieRedux (L'Ère Rétro / Arcade)

**Objectif** : Maîtriser la boucle de génération interactive (action → prédiction → frame) sans 3D physique.

### Prérequis
- Python 3.10/3.11, PyTorch (CUDA 11.8 pour RTX 2070).
- Disque D configuré pour `TEMP`/`TMP`/pip cache (voir `cleanup_and_configure.ps1`).

### Livrables
- [x] `Server_AI/genie_redux_rtx2070/model.py` — `TinyWorldModel` (CNN léger)
- [x] `dataset.py` — dataset synthétique interactif (balle + actions clavier)
- [x] `train.py` — entraînement local RTX 2070 (~5-10 min / 30 époques)
- [x] `demo_interactive.py` + `demo_generate_gif.py` — démonstration
- [x] `download_pretrained.py` — téléchargement de modèles Hugging Face (Matrix-Game 2.0/3.0)
- [x] Scripts Windows : `run_training.ps1`, `run_demo.ps1`, `full_pipeline.ps1`
- [ ] Intégration WebSocket avec `fonderie_oasis_api.py` (`/ws/matrix-game`)
- [ ] Frontend Godot 2D (`TextureRect`) consommant le flux généré

### Critères d'acceptation
- `train.py` produit un `best_model.pt` avec `val_loss` décroissant sur 30 époques.
- `demo_interactive.py --mode auto` boucle sans crash pendant ≥ 60 secondes.
- (Cible) Le frontend Godot affiche une image mise à jour à chaque frappe clavier envoyée au backend.

### Tâches restantes (issues suggérées)
1. `feat(redux): WebSocket bridge entre TinyWorldModel et fonderie_oasis_api`
2. `feat(godot): scène GenieRedux2DViewer.tscn avec TextureRect + capture clavier`
3. `chore(redux): benchmark VRAM/latence sur RTX 2070 réel`

---

## Phase 2 : GenieGodot (Immersion VR & 3D Légère)

**Objectif** : VR fonctionnelle sur Meta Quest 3S avec assets générés dynamiquement.

### Prérequis
- Godot 4.7+, plugin `godot-xr-tools` installé dans `addons/`.
- Backend `Genie Sim` (ou pipeline de substitution `GLTFDocument`) opérationnel.

### Livrables
- [x] `scenes/characters/iron_giant_assignment.tscn` + script associé
- [x] `scripts/characters/iron_giant_assignment.gd` — chargement runtime via `GLTFDocument`
- [x] `force_glb_to_tscn.gd` (`@tool`) — conversion GLB → TSCN, contournement de l'import strict de Godot
- [x] `fetch_mechas.py` — récupération d'assets depuis Google Drive
- [x] `scenes/hub/oasis_master_rpo_movie.tscn` — hub central avec PNJ/véhicules
- [ ] `oasis_asset_manager.gd` — analyse sémantique des noms de fichiers (`giant`, `hovercar`) pour ajuster échelle/collision automatiquement
- [ ] Intégration `godot-xr-tools` validée en casque réel (mains, téléportation)
- [ ] Multijoueur (sync des positions PNJ/joueurs) — optionnel selon portée V2

### Critères d'acceptation
- Le hub `oasis_master_rpo_movie.tscn` se lance sans erreur (`GenieOASIS.bat`).
- Le Géant de Fer (`IronGiantAssignment`) est visible, avec hover/light pulsing actifs.
- Les GLB générés dynamiquement s'affichent sans nécessiter de réimport manuel Godot.

### Tâches restantes (issues suggérées)
1. `feat(godot): oasis_asset_manager.gd - scaling & physics auto depuis mots-clés`
2. `test(vr): validation manette/tracking sur Meta Quest 3S`
3. `feat(backend): endpoint /api/v1/generate/world branché sur Genie Sim réel`
4. `fix(import): documenter le contournement GLTFDocument dans CONTRIBUTING.md`

---

## Phase 3 : GenieOasis (Photoréalisme Unreal Engine 5)

**Objectif** : Qualité visuelle AAA (Lumen, Nanite, shaders holographiques).

### Prérequis
- Licence/installation Unreal Engine 5.
- Pipeline d'export USD depuis `Genie Sim` validé en Phase 2.

### Livrables
- [ ] Projet UE5 `unreal/OasisUE5/` consommant `Server_AI/fonderie_oasis_api.py`
- [ ] Import USD automatisé (Python Editor Scripting UE5 ou Datasmith)
- [ ] Shader de matérialisation holographique (effet DeLorean) porté depuis Godot
- [ ] Lumen + Nanite activés sur les scènes clés (Hub, CopperKey, JadeKey)

### Critères d'acceptation
- Un asset généré par `fonderie_oasis_api.py` en `.usd` s'importe dans UE5 sans étape manuelle.
- Le shader de matérialisation reproduit l'effet du film (transition progressive, particules).

### Tâches restantes (issues suggérées)
1. `feat(ue5): squelette projet Unreal Engine 5 + connexion API FastAPI`
2. `feat(ue5): import USD automatisé via Python Editor Scripting`
3. `feat(shaders): port du shader scifi_construction vers UE5 Material Editor`

---

## Gouvernance & suivi

### Convention de nommage des commits
```
feat(scope): description courte
fix(scope): description courte
docs(scope): description courte
chore(scope): description courte
```
Scopes usuels : `redux`, `godot`, `ue5`, `backend`, `docs`.

### Jalons GitHub (Milestones)
Créer sur GitHub → Issues → Milestones :
- `v1.0-genieredux` — clôture Phase 1
- `v2.0-geniegodot` — clôture Phase 2
- `v3.0-genieoasis` — clôture Phase 3

### Board GitHub Project
Voir [`specs/GITHUB_PROJECT_SETUP.md`](../specs/GITHUB_PROJECT_SETUP.md) pour la configuration du tableau Kanban (colonnes, automatisations, liaison aux issues ci-dessus).
