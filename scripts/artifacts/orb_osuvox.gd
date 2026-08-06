extends Area3D

var time_passed: float = 0.0

func _process(delta: float) -> void:
	time_passed += delta
	rotation.y += delta * 2.0
	position.y = 1.2 + sin(time_passed * 3.0) * 0.1
	$ShieldMesh.scale = Vector3.ONE * (1.0 + sin(time_passed * 5.0) * 0.05)