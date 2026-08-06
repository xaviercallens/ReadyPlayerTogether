extends Area3D

var time_passed: float = 0.0

func _process(delta: float) -> void:
	time_passed += delta
	rotation.y += delta * 1.5
	position.y = 1.2 + sin(time_passed * 2.5) * 0.08

func _on_body_entered(body: Node3D) -> void:
	if body.is_in_group("player"):
		print("[ARTIFACT] Holy Hand Grenade acquired! Massive AOE Blast Ready!")