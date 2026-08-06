extends CharacterBody3D

@export var speed: float = 0.0
var time_passed: float = 0.0

func _process(delta: float) -> void:
	time_passed += delta
	# Flux Capacitor pulse animation
	$FluxCapacitor.light_energy = 2.0 + sin(time_passed * 10.0) * 1.5
	$RearThruster.light_energy = 3.0 + sin(time_passed * 8.0) * 1.0