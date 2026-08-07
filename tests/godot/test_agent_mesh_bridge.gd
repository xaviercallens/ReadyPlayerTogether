extends GutTest

# ==============================================================================
# GUT Unit Test: AgentMeshBridge & AIDialogueManager
# ==============================================================================

var bridge: AgentMeshBridge
var manager: AIDialogueManager

func before_each():
	bridge = AgentMeshBridge.new()
	add_child_autofree(bridge)

	manager = AIDialogueManager.new()
	manager.mesh_bridge = bridge
	add_child_autofree(manager)

func test_bridge_initialization():
	assert_not_null(bridge, "Bridge instance created")
	assert_gt(bridge._request_pool.size(), 0, "HTTP request pool should be initialized")
	assert_ne(bridge._session_id, "", "Session ID should be non-empty")

func test_dialogue_manager_send_player_speech():
	var signal_emitted := false
	manager.dialogue_started.connect(func(npc): signal_emitted = true)
	manager.send_player_speech("Hello guardian")
	assert_true(signal_emitted, "dialogue_started signal should be emitted on non-empty speech")

func test_dialogue_manager_empty_speech_ignored():
	var signal_emitted := false
	manager.dialogue_started.connect(func(npc): signal_emitted = true)
	manager.send_player_speech("   ")
	assert_false(signal_emitted, "Empty speech should be ignored")
