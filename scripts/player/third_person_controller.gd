# Fallback Third-Person Controller for Desktop Testing
# Based on emirthab's architecture, adapted for Ready Player Me Avatars
class_name AvatarThirdPersonController
extends CharacterBody3D

@export var speed: float = 5.0
@export var jump_velocity: float = 4.5
var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")

@onready var spring_arm: SpringArm3D = get_node_or_null("SpringArm3D")
@onready var avatar_mesh: Node3D = get_node_or_null("MeshPivot")
@onready var anim_tree: AnimationTree = get_node_or_null("MeshPivot/Avatar_RPM/AnimationTree")

func _ready() -> void:
    print("[TPC] Controleur 3e Personne initialise pour test bureau.")

func _physics_process(delta: float) -> void:
    if not is_on_floor():
        velocity.y -= gravity * delta

    if Input.is_action_just_pressed("ui_accept") and is_on_floor():
        velocity.y = jump_velocity

    # Entrees clavier ZQSD
    var input_dir := Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
    
    # Mouvement relatif a la camera si le SpringArm existe
    var direction := Vector3.ZERO
    if spring_arm:
        direction = (spring_arm.global_transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
    else:
        direction = (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
    
    if direction:
        velocity.x = direction.x * speed
        velocity.z = direction.z * speed
        
        if avatar_mesh:
            # Rotation fluide du mesh vers la direction (Lerp)
            var target_rotation = atan2(-direction.x, -direction.z)
            avatar_mesh.rotation.y = lerp_angle(avatar_mesh.rotation.y, target_rotation, 10.0 * delta)
    else:
        velocity.x = move_toward(velocity.x, 0, speed)
        velocity.z = move_toward(velocity.z, 0, speed)

    # Transmission a l'AnimationTree Mixamo
    if anim_tree:
        var current_speed = Vector2(velocity.x, velocity.z).length()
        anim_tree.set("parameters/BlendSpace1D/blend_position", current_speed)

    move_and_slide()
