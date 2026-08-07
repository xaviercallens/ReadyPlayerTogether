# 💃 Guide de la Pipeline Mixamo ➔ Godot 4 (Projet OASIS)

Ce guide permet de télécharger des milliers d'animations gratuites depuis Adobe Mixamo et de les appliquer automatiquement à vos avatars 3D **Ready Player Me** (Parzival, Art3mis, Aech, etc.) dans Godot 4.

---

### 1. Télécharger des animations depuis Mixamo :
1. Rendez-vous sur [mixamo.com](https://www.mixamo.com).
2. Choisissez une animation (ex: *Idle, Walking, Running, Hip Hop Dance, Cyberpunk Pistol Shoot*).
3. Cliquez sur **Download** avec les paramètres suivants :
   - **Format** : `FBX (.fbx)`
   - **Skin** : `Without Skin` (seule l'animation est nécessaire)
   - **Frames per second** : `30` ou `60`
   - **Keyframe Reduction** : `none`

---

### 2. Exportation Automatisée vers Godot 4 :

#### Option A (Directement dans Godot 4) :
- Glissez vos fichiers `.fbx` de Mixamo dans le dossier `res://assets/animations/`.
- Le script `res://scripts/avatars/mixamo_godot4_controller.gd` réaligne automatiquement les os (`mixamorig:Hips`, `mixamorig:Spine`, etc.) sur le profil standard `SkeletonProfileHumanoid` de Godot 4.

#### Option B (Batch Blender avec Root Motion) :
Si vous avez Blender installé sur votre PC :
```cmd
blender --background --python mixamo_to_godot4_blender.py -- ./mixamo_raw ./assets/animations
```
Ce script convertit tous vos FBX en `.glb` légers avec **Root Motion** configuré pour le Quest 3S.

---

### 3. Utilisation en GDScript :
```gdscript
var mixamo_ctrl = MixamoGodot4Controller.new()
mixamo_ctrl.avatar_skeleton = $Parzival/GeneralSkeleton
mixamo_ctrl.animation_player = $Parzival/AnimationPlayer
mixamo_ctrl.play_action("CyberpunkDance")
```
