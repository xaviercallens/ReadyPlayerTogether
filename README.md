# Projet OASIS - VR Quest Experience (Father & Son Edition)

Inspired by Ready Player One, built for Meta Quest VR headset.

## Roadmap

Le projet évolue en **trois phases** pour permettre au Pilote de monter en compétence progressivement :

1. **GenieRedux** - Jeu 2D rétro / arcade généré par Matrix-Game.
2. **GenieGodot** - Immersion VR 3D légère avec Godot 4.
3. **GenieOasis** - Photoréalisme avec Unreal Engine 5.

→ Voir [`docs/ROADMAP.md`](docs/ROADMAP.md) pour le détail.

## Spécification Phasée

Chaque phase dispose de livrables, critères d'acceptation et tâches GitHub détaillés.

→ Voir [`docs/PHASED_SPECIFICATION.md`](docs/PHASED_SPECIFICATION.md).

→ Configuration du tableau GitHub Project : [`specs/GITHUB_PROJECT_SETUP.md`](specs/GITHUB_PROJECT_SETUP.md).

## Architecture

Le backend "Salle des Machines Invariable" reste le même pour toutes les phases. Seul le frontend change.

→ Voir [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) pour le détail.

## Project Structure
- `Hub/`: Central OASIS lounge & portal navigation.
- `CopperKey/`: Speed & Dodge mini-game.
- `JadeKey/`: Puzzle & VR Interface puzzle room.
- `CrystalKey/`: AI NPC Guardian & Easter Egg secret room.
- `Avatars/`: Ready Player Me integration assets.
- `AI_Services/`: Local/API AI integrations (GenAI 3D textures, avatar voice, world simulation).
- `Server_AI/fonderie_oasis_api.py`: Backend FastAPI unifié.

## Team Roles
- **Pilot (Son, 10yo)**: Gameplay mechanics, level design, object interactions, Blueprint/Visual logic.
- **Navigator (Father, ML Expert)**: System architecture, Meta Quest VR build pipeline, Ready Player Me SDK setup, GenAI asset pipelines & AI NPC logic.
