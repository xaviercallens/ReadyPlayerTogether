# Configuration du GitHub Project - OASIS

> Guide pour configurer un tableau Kanban GitHub Project lié aux phases décrites dans [`docs/PHASED_SPECIFICATION.md`](../docs/PHASED_SPECIFICATION.md).

## 1. Créer le Project

1. Aller sur `https://github.com/xaviercallens/ReadyPlayerTogether`
2. Onglet **Projects** → **New project** → template **Board**
3. Nommer le projet : `OASIS Roadmap`

## 2. Colonnes (Kanban)

| Colonne | Description |
|---------|-------------|
| `Backlog` | Idées et tâches non priorisées |
| `À faire (Phase actuelle)` | Tâches planifiées pour le sprint en cours |
| `En cours` | Tâches en développement actif |
| `Revue / Test` | Code à valider (PR ouverte, test manuel VR/GPU) |
| `Terminé` | Tâches closes et mergées |

## 3. Milestones (Jalons)

Créer dans **Issues → Milestones** :

| Milestone | Description | Date cible |
|-----------|-------------|------------|
| `v1.0-genieredux` | Démo 2D interactive connectée au frontend Godot | À définir |
| `v2.0-geniegodot` | VR Quest 3S stable avec assets générés dynamiquement | À définir |
| `v3.0-genieoasis` | Prototype Unreal Engine 5 photoréaliste | À définir |

## 4. Labels suggérés

| Label | Couleur | Usage |
|-------|---------|-------|
| `phase:redux` | `#FBCA04` | Tâches Phase 1 |
| `phase:godot` | `#0E8A16` | Tâches Phase 2 |
| `phase:ue5` | `#5319E7` | Tâches Phase 3 |
| `type:backend` | `#1D76DB` | Fonderie / API / IA |
| `type:frontend` | `#D93F0B` | Godot / UE5 / rendu |
| `type:docs` | `#C5DEF5` | Documentation |
| `priority:high` | `#B60205` | Bloquant |

## 5. Issues initiales à créer (Phase 1 - GenieRedux)

```
[ ] feat(redux): WebSocket bridge entre TinyWorldModel et fonderie_oasis_api
    Labels: phase:redux, type:backend

[ ] feat(godot): scène GenieRedux2DViewer.tscn avec TextureRect + capture clavier
    Labels: phase:redux, type:frontend

[ ] chore(redux): benchmark VRAM/latence sur RTX 2070 réel
    Labels: phase:redux, priority:high
```

## 6. Issues initiales à créer (Phase 2 - GenieGodot)

```
[ ] feat(godot): oasis_asset_manager.gd - scaling & physics auto depuis mots-clés
    Labels: phase:godot, type:frontend

[ ] test(vr): validation manette/tracking sur Meta Quest 3S
    Labels: phase:godot, priority:high

[ ] feat(backend): endpoint /api/v1/generate/world branché sur Genie Sim réel
    Labels: phase:godot, type:backend

[ ] fix(import): documenter le contournement GLTFDocument dans CONTRIBUTING.md
    Labels: phase:godot, type:docs
```

## 7. Issues initiales à créer (Phase 3 - GenieOasis)

```
[ ] feat(ue5): squelette projet Unreal Engine 5 + connexion API FastAPI
    Labels: phase:ue5, type:backend

[ ] feat(ue5): import USD automatisé via Python Editor Scripting
    Labels: phase:ue5, type:frontend

[ ] feat(shaders): port du shader scifi_construction vers UE5 Material Editor
    Labels: phase:ue5, type:frontend
```

## 8. Automatisation recommandée (GitHub Project Workflows)

Dans les paramètres du Project (**⋯ → Workflows**) :
- **Item added to project** → statut `Backlog`
- **Pull request merged** → statut `Terminé`
- **Issue closed** → statut `Terminé`

## 9. Lien avec les commits

Utiliser la syntaxe de fermeture automatique dans les messages de commit/PR :
```
git commit -m "feat(redux): WebSocket bridge (closes #12)"
```

---

**Note** : Ce guide décrit une configuration manuelle via l'interface GitHub. Il n'existe pas d'API Git pour créer un Project directement depuis ce dépôt local ; utilisez `gh project create` (GitHub CLI) si vous préférez une approche scriptée.
