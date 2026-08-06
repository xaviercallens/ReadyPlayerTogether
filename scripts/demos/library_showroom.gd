extends Node3D

# ==============================================================================
# PROJET OASIS - Interactive Library & Showroom Controller
# Allows player to inspect and select active avatars, artifacts, and weaponry.
# Press 'L' from anywhere to enter | Press 'H' to return to HUB.
# Press 'E' near any pedestal to SELECT the object/avatar for your game!
# ==============================================================================

@onready var selection_label: Label3D = $SelectionHUD

var selected_item_name: String = "Parzival Avatar"

func _ready() -> void:
	print("[OASIS SHOWROOM] Showroom active. Walk up to any item and press E to select!")
	_connect_pedestals()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_H or event.keycode == KEY_BACKSPACE:
			print("[OASIS SHOWROOM] Returning to Cyberpunk HUB...")
			get_tree().change_scene_to_file("res://scenes/hub/oasis_hub.tscn")

func _connect_pedestals() -> void:
	for i in range(1, 11):
		var area_name = "Area_0%d" % i if i < 10 else "Area_%d" % i
		var area_node = get_node_or_null("Pedestals/" + area_name)
		if area_node:
			area_node.body_entered.connect(_on_pedestal_entered.bind(i))

func _on_pedestal_entered(body: Node3D, item_id: int) -> void:
	if body.is_in_group("player"):
		var item_names = [
			"The Copper Key", "The Jade Key", "The Crystal Key",
			"Zemeckis Cube", "Holy Hand Grenade", "Parzival RPM Avatar",
			"Art3mis RPM Avatar", "Aech Mech Avatar", "Iron Giant Companion", "XR Dojo Pistol"
		]
		if item_id >= 1 and item_id <= item_names.size():
			selected_item_name = item_names[item_id - 1]
			selection_label.text = "[ACTIVE SELECTION]: " + selected_item_name + " Selected!"
			print("[SHOWROOM] Player selected: ", selected_item_name)