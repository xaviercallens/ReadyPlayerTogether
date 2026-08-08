# GenieRedux RTX 2070 Demo

Version légère de démonstration d'un **world model** entraînable sur une RTX 2070 8GB.

## Principe

Un petit modèle CNN apprend à prédire la frame suivante (`t+1`) à partir de la frame actuelle (`t`) et d'une action (clavier : noop, gauche, droite, haut, bas).

Le dataset est synthétique : une balle colorée se déplace dans un environnement 64x64.

## Fichiers

- `model.py` — `TinyWorldModel` (CNN encodeur/décodeur)
- `dataset.py` — génération du dataset synthétique + `SyntheticWorldDataset`
- `train.py` — entraînement sur RTX 2070
- `demo_interactive.py` — démo interactive (GPU ou simulation)
- `demo_generate_gif.py` — génère un GIF de démo
- `download_pretrained.py` — télécharge les modèles pré-entraînés depuis Hugging Face
- `setup_rtx2070.bat` — répare l'installation PyTorch CUDA

## Scripts de lancement (Windows)

### Lancer la démo
```powershell
.\run_demo.ps1
# ou
.\run_demo.bat
```

### Entraîner le modèle
```powershell
.\run_training.ps1
# ou
.\run_training.bat
```

### Télécharger les modèles pré-entraînés
```powershell
.\download_pretrained.ps1
# ou
python download_pretrained.py
```

## Installation

Si PyTorch ne détecte pas le GPU (erreur `c10_cuda.dll`) :

```powershell
.\setup_rtx2070.bat
```

Puis testez :

```powershell
python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

## Utilisation détaillée

### 1. Générer le dataset (automatique)

```powershell
python dataset.py
```

Génère 50 000 frames synthétiques dans `data/frames.npy` et `data/actions.npy`.

### 2. Entraîner le modèle

```powershell
python train.py --batch_size 64 --epochs 30
```

Sur RTX 2070, l'entraînement devrait prendre **5-10 minutes** pour 30 époques.

Modèles sauvegardés :
- `checkpoints/best_model.pt` — meilleur modèle (validation loss minimale)
- `checkpoints/final_model.pt` — dernier modèle

### 3. Lancer la démo interactive

```powershell
python demo_interactive.py --mode auto
```

Modes disponibles :
- `auto` — détecte automatiquement GPU ou simulation
- `pytorch` — force le mode GPU
- `simulation` — force le mode simulation (pas de GPU nécessaire)

La démo génère des frames en continu avec des actions aléatoires.

### 4. Générer un GIF de démo

```powershell
python demo_generate_gif.py
```

Génère `output/demo.gif` (120 frames, 25 FPS).

## Télécharger les modèles pré-entraînés

```powershell
python download_pretrained.py
```

Tente de télécharger depuis Hugging Face :
- `INSAIT-Institute/GenieRedux` — modèle GenieRedux distillé
- `Skywork/Matrix-Game-2.0` — modèle Matrix-Game 2.0
- `Skywork/Matrix-Game-3.0` — modèle Matrix-Game 3.0 (5B)

**Note :** Les modèles complets de GenieRedux/Matrix-Game nécessitent 24-80GB de VRAM. Cette démo utilise un modèle léger (TinyWorldModel) pour RTX 2070.

## Limitations

C'est une démo pédagogique. Pour atteindre la qualité d'un Matrix-Game ou GenieRedux à l'échelle, il faudrait :
- Un modèle transformer beaucoup plus gros (nécessitant 24-80GB de VRAM)
- Un vrai dataset de jeux (Minecraft, GTA, etc.)
- Entraînement distribué sur plusieurs GPUs A100/H100

## Prochaine étape

Connecter `demo_interactive.py` au backend `Server_AI/fonderie_oasis_api.py` pour que le frontend GenieRedux (Godot 2D) reçoive les frames via WebSocket.
