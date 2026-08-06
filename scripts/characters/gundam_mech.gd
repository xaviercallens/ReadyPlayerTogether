extends CharacterBody3D

var time_passed: float = 0.0

func _process(delta: float) -> void:
	time_passed += delta
	# Gundam eye reactor pulse
	$EyeLight.light_energy = 4.0 + sin(time_passed * 6.0) * 1.5