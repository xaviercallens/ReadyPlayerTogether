# Mixamo to Godot 4 Animation Controller
# Plays named Mixamo actions on a target Skeleton3D / AnimationPlayer.
class_name MixamoGodot4Controller
extends Node

var _anim_player: AnimationPlayer
var _current_action: String = ""

func _ready() -> void:
	# Try to find the AnimationPlayer on the parent or sibling node
	var parent := get_parent()
	if parent:
		_anim_player = parent.get_node_or_null("AnimationPlayer") as AnimationPlayer
		if _anim_player == null:
			# Try deeper search
			var players := parent.find_children("*", "AnimationPlayer", true, false)
			if players.size() > 0:
				_anim_player = players[0] as AnimationPlayer

func play_action(action_name: String) -> void:
	if action_name == _current_action:
		return
	_current_action = action_name

	if _anim_player == null:
		return
	if _anim_player.has_animation(action_name):
		_anim_player.play(action_name)
	else:
		print("[MixamoController] Animation '", action_name, "' not found. Available: ", _anim_player.get_animation_list())

func stop_action() -> void:
	_current_action = ""
	if _anim_player:
		_anim_player.stop()
