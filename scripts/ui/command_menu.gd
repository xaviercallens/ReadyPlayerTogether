extends CanvasLayer

# ==============================================================================
# PROJET OASIS - Controls & Commands Overlay HUD
# ==============================================================================

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_TAB or event.keycode == KEY_ESCAPE:
			var overlay = get_node_or_null("Overlay")
			if overlay == null:
				overlay = get_node_or_null("Control")
			if overlay != null:
				overlay.visible = not overlay.visible