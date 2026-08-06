extends CanvasLayer

# ==============================================================================
# PROJET OASIS - Controls & Commands Overlay HUD
# ==============================================================================

@onready var panel: Control = $Control

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_TAB or event.keycode == KEY_ESCAPE:
			panel.visible = not panel.visible