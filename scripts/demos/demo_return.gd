extends Node3D

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_H or event.keycode == KEY_BACKSPACE:
			print("[OASIS DEMO] Returning to Cyberpunk HUB...")
			get_tree().change_scene_to_file("res://scenes/hub/oasis_hub.tscn")
			
	if event is InputEventJoypadButton and event.pressed:
		if event.button_index == JOY_BUTTON_START or event.button_index == JOY_BUTTON_BACK:
			get_tree().change_scene_to_file("res://scenes/hub/oasis_hub.tscn")