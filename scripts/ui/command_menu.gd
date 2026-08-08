extends CanvasLayer

# ==============================================================================
# PROJET OASIS - Controls & Commands Overlay HUD
# ==============================================================================

@onready var overlay: Control = $Overlay

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_TAB or event.keycode == KEY_ESCAPE:
			if overlay != null:
				overlay.visible = not overlay.visible