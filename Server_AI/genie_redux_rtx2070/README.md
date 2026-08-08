# GenieRedux RTX 2070 Demo

Version légère de démonstration d'un **world model** entraînable sur une RTX 2070 8GB.

## Principe

Un petit modèle CNN apprend à prédire la frame suivante (`t+1`) à partir de la frame actuelle (`t`) et d'une action (clavier : noop, gauche, droite, haut, bas).

Le dataset est synthétique : une balle colorée se déplace dans un environnement 64x64.

## Fichiers

- `model.py` — `TinyWorldModel` (CNN encodeur/décodeur)
- `dataset.py` — génération du dataset synthétique + `SyntheticWorldDataset`
- `train.py` — entraînement sur RTX 2070
- `demo.py` — démo interactive (WASD / flèches)
- `setup_rtx2070.bat` — répare l'installation PyTorch CUDA

## Installation

Si PyTorch ne détecte pas le GPU (erreur `c10_cuda.dll`) :

```powershell
.\setup_rtx2070.bat
```

Puis testez :

```python
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```

## Utilisation

### 1. Générer le dataset

```python
python dataset.py
```

### 2. Entraîner le modèle

```python
python train.py --batch_size 64 --epochs 30
```

Sur RTX 2070, l'entraînement devrait prendre **moins de 10 minutes** pour 30 époques.

### 3. Lancer la démo

```python
python demo.py --checkpoint checkpoints/best_model.pt
```

Contrôles : **WASD** ou **Flèches**. **ESC** pour quitter.

## Limitations

C'est une démo pédagogique. Pour atteindre la qualité d'un Matrix-Game ou GenieRedux à l'échelle, il faudrait un modèle transformer beaucoup plus gros (nécessitant 24-80GB de VRAM) et un vrai dataset de jeux.

## Prochaine étape

Connecter `demo.py` au backend `Server_AI/fonderie_oasis_api.py` pour que le frontend GenieRedux (Godot 2D) reçoive les frames via WebSocket.
