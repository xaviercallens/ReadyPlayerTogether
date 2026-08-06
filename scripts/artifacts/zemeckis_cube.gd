extends Area3D

@export var rotation_speed: float = 2.0
var time_passed: float = 0.0

func _process(delta: float) -> void:
	time_passed += delta
	rotation.y += delta * rotation_speed
	position.y = 1.2 + sin(time_passed * 3.0) * 0.1

func _on_body_entered(body: Node3D) -> void:
	if body.is_in_group("player"):
		print("[ARTIFACT] Zemeckis Cube Activated! Reversing Time 60 seconds...")