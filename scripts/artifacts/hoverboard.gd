extends Area3D

@export var levitation_speed: float = 3.0
var time_passed: float = 0.0

func _process(delta: float) -> void:
	time_passed += delta
	rotation.y += delta * levitation_speed
	position.y = 1.0 + sin(time_passed * 4.0) * 0.12
	$ThrusterLight.light_energy = 3.0 + sin(time_passed * 10.0) * 1.5

func _on_body_entered(body: Node3D) -> void:
	if body.is_in_group("player"):
		print("[ARTIFACT] Cyberpunk Hoverboard Equipped! Anti-Gravity Flight Active!")