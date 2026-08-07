extends GutTest

# ==============================================================================
# GUT Unit Test: AvatarThirdPersonController
# ==============================================================================

var controller: AvatarThirdPersonController

func before_each():
	controller = AvatarThirdPersonController.new()
	add_child_autofree(controller)

func test_controller_initialization():
	assert_not_null(controller, "Controller instance should be created")
	assert_eq(controller.speed, 5.0, "Default movement speed should be 5.0")
	assert_eq(controller.sprint_speed, 8.0, "Sprint speed should be 8.0")
	assert_gt(controller.jump_velocity, 0.0, "Jump velocity should be positive")

func test_physics_process_gravity_pull():
	controller.global_position = Vector3(0, 10, 0)
	controller.velocity = Vector3.ZERO
	controller._physics_process(0.016)
	assert_lt(controller.velocity.y, 0.0, "Gravity should decrease velocity.y when in air")

func test_movement_direction_zero_when_no_input():
	controller.velocity = Vector3.ZERO
	controller._physics_process(0.016)
	assert_eq(controller.velocity.x, 0.0, "Velocity.x should be 0 without input")
	assert_eq(controller.velocity.z, 0.0, "Velocity.z should be 0 without input")
