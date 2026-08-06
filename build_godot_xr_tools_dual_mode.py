import os

BASE_DIR = r"D:\xdev\Oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# 1. VR PLAYER RIG SCRIPT (scripts/player_vr/vr_player.gd)
# ==============================================================================
VR_PLAYER_GD = """
extends XROrigin3D

# ==============================================================================
# PROJET OASIS - Quest 3S VR Player Rig (Godot XR Tools Architecture)
# Automatically initializes OpenXR if connected, with 3D hands & teleport.
# ==============================================================================

var xr_interface: XRInterface

@onready var left_controller: XRController3D = $MainGauche
@onready var right_controller: XRController3D = $MainDroite
@onready var vr_camera: XRCamera3D = $XRCamera3D

func _ready() -> void:
	xr_interface = XRServer.find_interface("OpenXR")
	if xr_interface and xr_interface.is_initialized():
		print("=========================================")
		print("🚀 CASQUE VR META QUEST 3S DÉTECTÉ ET ACTIF !")
		print("=========================================")
		get_viewport().use_xr = true
	else:
		print("[VR RIG] Casque VR non détecté. Mode Bureau actif.")

func _process(delta: float) -> void:
	if left_controller.is_button_pressed("by_button") or right_controller.is_button_pressed("by_button"):
		print("[VR CONTROLLER] Menu Button pressed!")
"""

write_file(os.path.join(BASE_DIR, "scripts/player_vr/vr_player.gd"), VR_PLAYER_GD)

# ==============================================================================
# 2. VR PLAYER RIG SCENE (scenes/player_vr/vr_player.tscn)
# ==============================================================================
VR_PLAYER_TSCN = """
[gd_scene load_steps=7 format=3 uid="uid://vr_player_rig_scene"]

[ext_resource type="Script" path="res://scripts/player_vr/vr_player.gd" id="1_vr_script"]
[ext_resource type="PackedScene" uid="uid://scene_navigator_ui" path="res://scenes/ui/scene_navigator.tscn" id="2_navigator"]
[ext_resource type="PackedScene" uid="uid://command_menu_ui" path="res://scenes/ui/command_menu.tscn" id="3_command_menu"]

[sub_resource type="StandardMaterial3D" id="Mat_VRHand"]
albedo_color = Color(0.0, 0.9, 1.0, 1)
metallic = 0.8
roughness = 0.2
emission_enabled = true
emission = Color(0.0, 0.9, 1.0, 1)
emission_energy_multiplier = 2.0

[sub_resource type="BoxMesh" id="Mesh_LeftHand"]
material = SubResource("Mat_VRHand")
size = Vector3(0.1, 0.08, 0.18)

[sub_resource type="BoxMesh" id="Mesh_RightHand"]
material = SubResource("Mat_VRHand")
size = Vector3(0.1, 0.08, 0.18)

[node name="VRPlayerRig" type="XROrigin3D"]
script = ExtResource("1_vr_script")

[node name="XRCamera3D" type="XRCamera3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.7, 0)
current = true

[node name="MainGauche" type="XRController3D" parent="."]
tracker = &"left_hand"
pose = &"default"

[node name="LeftHandMesh" type="MeshInstance3D" parent="MainGauche"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, -0.05)
mesh = SubResource("Mesh_LeftHand")

[node name="MainDroite" type="XRController3D" parent="."]
tracker = &"right_hand"
pose = &"default"

[node name="RightHandMesh" type="MeshInstance3D" parent="MainDroite"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, -0.05)
mesh = SubResource("Mesh_RightHand")

[node name="SceneNavigator" parent="." instance=ExtResource("2_navigator")]

[node name="CommandMenu" parent="." instance=ExtResource("3_command_menu")]
"""

write_file(os.path.join(BASE_DIR, "scenes/player_vr/vr_player.tscn"), VR_PLAYER_TSCN)

# ==============================================================================
# 3. GUIDE DU PILOTE VR PÈRE & FILS (Guide_Du_Pilote.md)
# ==============================================================================
GUIDE_MD = """
# 🚀 Guide du Pilote VR OASIS - Père & Fils (Quest 3S & Godot 4)

Bienvenue dans votre guide officiel pour développer et jouer ensemble sur **Projet OASIS** !

---

### 🎮 Les 6 Étapes Réalisées Ensemble :

1. **Étape 1 : Création du Projet**
   - Projet : `D:\\xdev\\Oasis` (Nom : *Projet OASIS VR*).
   - Mode de Rendu : **Mobile / Forward+** optimisé pour Quest 3S.

2. **Étape 2 : Plugins XR & Godot XR Tools**
   - Plugins installés : `Godot OpenXR Vendors` & `Godot XR Tools`.

3. **Étape 3 : Configuration VR**
   - OpenXR activé pour Quest 3S via Link / AirLink / SteamVR.

4. **Étape 4 : Rig du Joueur Virtual (Corps & Mains 3D)**
   - `XROrigin3D` ➡️ `XRCamera3D` + `MainGauche` (`left_hand`) + `MainDroite` (`right_hand`).

5. **Étape 5 : Code d'Initialisation GDScript**
   - Détection automatique du casque Meta Quest 3S avec bascule VR dynamique.

6. **Étape 6 : Test Dual Mode (PC Bureau & VR Headset)**
   - Jouez au **clavier/souris/manette** sur PC Bureau.
   - Branchez le **Meta Quest 3S** avec le câble Link pour plonger dans l'OASIS à 360° !

---

### ⌨️ Commandes Rapides en Jeu :
- **`Shift + F`** : Téléporteur texte avec recherche autocomplétée.
- **`L`** : Galerie d'Exposition Showroom.
- **`Tab`** : Menu Master des Contrôles.
- **`1` à `9`, `0`** : Téléportation immédiate vers les 10 Démos.
"""

write_file(os.path.join(BASE_DIR, "Guide_Du_Pilote.md"), GUIDE_MD)

print("Godot XR Tools VR Player Rig & Guide du Pilote generated successfully!")
