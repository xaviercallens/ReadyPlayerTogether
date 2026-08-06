extends CharacterBody3D

@export var speed: float = 6.0
@export var jump_velocity: float = 4.5

var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")
var delorean_scene = preload("res://scenes/vehicles/delorean_car.tscn")

func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity.y -= gravity * delta

	if Input.is_action_just_pressed("ui_accept") and is_on_floor():
		velocity.y = jump_velocity

	var input_dir := Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	var direction := (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
	if direction:
		velocity.x = direction.x * speed
		velocity.z = direction.z * speed
	else:
		velocity.x = move_toward(velocity.x, 0, speed)
		velocity.z = move_toward(velocity.z, 0, speed)

	move_and_slide()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_F:
			spawn_delorean_in_front()

func spawn_delorean_in_front() -> void:
	var camera = $Camera3D
	var spawn_pos = camera.global_position - (camera.global_transform.basis.z * 4.0)
	spawn_pos.y -= 1.0
	
	var car = delorean_scene.instantiate()
	get_tree().current_scene.add_child(car)
	car.global_position = spawn_pos
	print("🏎️ [SPAWNER] DeLorean Materialized 4m in front of Player (Key: F)!")