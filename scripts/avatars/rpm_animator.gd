# Ready Player Me Avatar Animator
# Manages animation states for RPM avatars (Idle, Wave, Walk, Run, etc.)
class_name RPMAnimator
extends Node

enum AnimState { IDLE, WAVE, WALK, RUN, JUMP, DANCE }

@export var target_avatar_node: Node3D

var current_state: AnimState = AnimState.IDLE
var _anim_player: AnimationPlayer

func _ready() -> void:
	if target_avatar_node:
		_anim_player = target_avatar_node.get_node_or_null("AnimationPlayer") as AnimationPlayer

func set_state(new_state: AnimState) -> void:
	if new_state == current_state:
		return
	current_state = new_state
	_play_animation_for_state(new_state)

func _play_animation_for_state(state: AnimState) -> void:
	if _anim_player == null:
		return
	match state:
		AnimState.IDLE:
			if _anim_player.has_animation("Idle"):
				_anim_player.play("Idle")
		AnimState.WAVE:
			if _anim_player.has_animation("WaveGreeting"):
				_anim_player.play("WaveGreeting")
		AnimState.WALK:
			if _anim_player.has_animation("Walk"):
				_anim_player.play("Walk")
		AnimState.RUN:
			if _anim_player.has_animation("Run"):
				_anim_player.play("Run")
		AnimState.JUMP:
			if _anim_player.has_animation("Jump"):
				_anim_player.play("Jump")
		AnimState.DANCE:
			if _anim_player.has_animation("Dance"):
				_anim_player.play("Dance")