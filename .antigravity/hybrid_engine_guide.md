# 🚀 OASIS Hybrid Architecture Engine (Genie Sim + Matrix-Game 2.0 + Godot 4)

Ce document détaille l'architecture hybride du Projet OASIS.

---

### 🌐 Les 3 Composants de la Stratégie Hybride :

1. **La Base (Godot 4)** :
   - Moteur physique, collisions, saut, ramassage de la Clé de Cuivre et contrôles VR/PC.

2. **L'Architecte (Genie Sim GLTF)** :
   - Modèle 3D persistant généré en arrière-plan et chargé dynamiquement par `GLTFDocument`.

3. **Le Rêveur (Matrix-Game 2.0 Streamer)** :
   - Serveur WebSocket Python (`Server_AI/matrix_game_streamer.py`) diffusant un flux interactif 25 FPS affiché sur les **Écrans / Portails Virtuels** ([scenes/ui/virtual_portal_screen.tscn](file:///D:/xdev/Oasis/scenes/ui/virtual_portal_screen.tscn)).