extends SceneTree

# ==============================================================================
# PROJET OASIS - Godot Lightweight Test Runner
# Verifies that all 10 demo scenes and the PC player instantiate without errors.
# Run with: godot --headless -s tests/godot/test_scenes.gd
# ==============================================================================

func _init():
	print("=======================================")
	print("[OASIS QA] Starting Godot Test Runner...")
	print("=======================================")
	
	var scenes_to_test = [
		"res://scenes/player_vr/pc_player.tscn",
		"res://scenes/player_vr/vr_player.tscn",
		"res://scenes/hub/oasis_hub.tscn",
		"res://scenes/key_copper/copper_key_level.tscn",
		"res://scenes/demos/scene_01_the_stacks.tscn",
		"res://scenes/demos/scene_02_hallidays_journal.tscn",
		"res://scenes/demos/scene_03_copper_race.tscn",
		"res://scenes/demos/scene_04_distracted_globe.tscn",
		"res://scenes/demos/scene_05_arcade_retro.tscn",
		"res://scenes/demos/scene_06_planet_doom.tscn",
		"res://scenes/demos/scene_07_overlook_hotel.tscn",
		"res://scenes/demos/scene_08_ioi_citadel.tscn",
		"res://scenes/demos/scene_09_crystal_castle.tscn",
		"res://scenes/demos/scene_10_easter_egg.tscn",
		"res://scenes/demos/scene_11_xr_dojo.tscn",
		"res://scenes/artifacts/zemeckis_cube.tscn",
		"res://scenes/artifacts/holy_hand_grenade.tscn",
		"res://scenes/characters/iron_giant_companion.tscn",
		"res://scenes/demos/scene_12_library_showroom.tscn",
		"res://scenes/ui/scene_navigator.tscn",
		"res://scenes/vehicles/delorean_car.tscn",
		"res://scenes/characters/rpo_mannequin_male.tscn",
		"res://scenes/ui/command_menu.tscn"
	]
	
	var all_passed = true
	var loaded_count = 0
	
	for scene_path in scenes_to_test:
		if not FileAccess.file_exists(scene_path):
			print("❌ FAIL: File not found -> ", scene_path)
			all_passed = false
			continue
			
		var packed_scene = load(scene_path)
		if packed_scene:
			var instance = packed_scene.instantiate()
			if instance:
				print("✅ PASS: Successfully instantiated -> ", scene_path)
				loaded_count += 1
				instance.free()
			else:
				print("❌ FAIL: Could not instantiate -> ", scene_path)
				all_passed = false
		else:
			print("❌ FAIL: Could not load -> ", scene_path)
			all_passed = false

	print("=======================================")
	if all_passed and loaded_count == scenes_to_test.size():
		print("[OASIS QA] All ", loaded_count, " scenes passed instantiation tests! 🚀")
		quit(0)
	else:
		print("[OASIS QA] Tests failed. Please check the logs.")
		quit(1)
