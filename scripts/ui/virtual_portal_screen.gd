extends Node3D

# ==============================================================================
# PROJET OASIS - Virtual Portal Screen (Matrix-Game 2.0 Receiver)
# Displays dynamic AI streamed dimensions inside the 3D OASIS world.
# ==============================================================================

@onready var screen_label: Label3D = $ScreenMesh/Label3D
var time_passed: float = 0.0

func _process(delta: float) -> void:
	time_passed += delta
	# Pulsing portal frame effect
	$ScreenMesh.position.y = 2.2 + sin(time_passed * 2.0) * 0.05