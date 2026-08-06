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