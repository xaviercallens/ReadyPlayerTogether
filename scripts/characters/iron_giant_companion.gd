extends CharacterBody3D

@onready var label: Label3D = $Label3D
var time_passed: float = 0.0

func _process(delta: float) -> void:
	time_passed += delta
	# Subtle breathing animation for the giant mech
	$MechBody.position.y = 4.0 + sin(time_passed * 1.5) * 0.1