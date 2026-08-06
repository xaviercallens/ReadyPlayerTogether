extends CanvasLayer

# ==============================================================================
# PROJET OASIS - Interactive VR Artifact Inventory System
# Press 'I' or Menu Button to view gathered Ready Player One Keys & Artifacts
# ==============================================================================

@onready var panel: Control = $Control
@onready var item_list: ItemList = $Control/Panel/VBoxContainer/ItemList
@onready var desc_label: Label = $Control/Panel/VBoxContainer/DescLabel

var artifacts = [
	{"name": "🔑 Copper Key", "desc": "The First Key of Halliday's Easter Egg Hunt. Unlocks the Jade Gate."},
	{"name": "🎲 Zemeckis Cube", "desc": "Reverses time in a 60-meter radius by 50 seconds."},
	{"name": "💣 Holy Hand Grenade", "desc": "Obliterates all enemies within impact range after a 3-second countdown."},
	{"name": "🛹 Cyberpunk Hoverboard", "desc": "Provides anti-gravity flight across OASIS plazas."},
	{"name": "🔮 Orb of Osuvox", "desc": "Creates a level-90 impenetrable forcefield sphere."}
]

func _ready() -> void:
	panel.visible = false
	item_list.item_selected.connect(_on_item_selected)
	_populate_items()

func _populate_items() -> void:
	item_list.clear()
	for item in artifacts:
		item_list.add_item(item["name"])

func toggle_inventory() -> void:
	panel.visible = not panel.visible
	if panel.visible:
		Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
	else:
		Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode == KEY_I:
			toggle_inventory()

func _on_item_selected(index: int) -> void:
	if index >= 0 and index < artifacts.size():
		desc_label.text = artifacts[index]["desc"]