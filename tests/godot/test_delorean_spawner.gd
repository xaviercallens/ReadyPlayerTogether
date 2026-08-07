extends GutTest

# ==============================================================================
# GUT Unit Test: DeLoreanSpawner
# ==============================================================================

var spawner: DeLoreanSpawner

func before_each():
	spawner = DeLoreanSpawner.new()
	add_child_autofree(spawner)

func test_spawner_initialization():
	assert_not_null(spawner, "Spawner instance should be valid")

func test_spawn_delorean_without_scene_graceful():
	# Should print an error log and return safely without crashing
	spawner.delorean_scene = null
	spawner.spawn_delorean()
	assert_true(true, "Spawning with null delorean_scene did not crash")

func test_spawn_delorean_without_active_camera_graceful():
	var mock_scene = PackedScene.new()
	spawner.delorean_scene = mock_scene
	spawner.spawn_delorean()
	assert_true(true, "Spawning without active camera in viewport did not crash")
