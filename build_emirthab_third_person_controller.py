import os
import sys

def build_demo_features():
    print("=== Building DeLorean Spawner & Third-Person Controller Demo ===")
    
    os.makedirs("scripts/player", exist_ok=True)
    os.makedirs("scripts/vehicles", exist_ok=True)
    os.makedirs("materials/shaders", exist_ok=True)
    
    # 1. Sci-Fi Construction Shader (Godot 4 Shader)
    construction_shader = """// Ready Player One DeLorean Construction Shader
shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back, diffuse_burley, specular_schlick_ggx;

uniform vec4 base_color : source_color = vec4(0.8, 0.8, 0.8, 1.0);
uniform vec4 neon_color : source_color = vec4(0.0, 1.0, 1.0, 1.0);
uniform float construction_progress : hint_range(0.0, 1.0) = 0.0;
uniform float scanline_width : hint_range(0.0, 0.5) = 0.05;
uniform float object_height = 2.0;

void fragment() {
    // Local Y position (normalized roughly between 0 and 1)
    float local_y = (VERTEX.y / object_height) + 0.5;
    
    // Check if the current pixel is below the construction line
    if (local_y > construction_progress) {
        discard; // Transparent / Not yet constructed
    }
    
    // Glowing edge effect at the construction line
    if (local_y > construction_progress - scanline_width) {
        ALBEDO = neon_color.rgb;
        EMISSION = neon_color.rgb * 3.0; // Glowing Neon
    } else {
        // Solid fully constructed car
        ALBEDO = base_color.rgb;
        EMISSION = vec3(0.0);
    }
}
"""
    with open("materials/shaders/scifi_construction.gdshader", "w", encoding="utf-8") as f:
        f.write(construction_shader)
    print("-> Wrote materials/shaders/scifi_construction.gdshader")

    # 2. DeLorean Spawner Script (Action Button "F" or VR Trigger)
    delorean_spawner_gd = """# DeLorean Sci-Fi Spawner for Projet OASIS
class_name DeLoreanSpawner
extends Node3D

@export var delorean_scene: PackedScene
@onready var camera = get_viewport().get_camera_3d()

func _input(event: InputEvent) -> void:
    # "spawn_car" doit etre mappe sur la touche 'F' ou le trigger VR dans l'Input Map
    if event.is_action_pressed("spawn_car"):
        spawn_delorean()

func spawn_delorean() -> void:
    if not delorean_scene:
        print("[DeLoreanSpawner] Erreur: Aucune scene DeLorean assignee!")
        return
        
    var delorean = delorean_scene.instantiate()
    get_tree().current_scene.add_child(delorean)
    
    # 3 metres devant la camera, 1 metre plus bas
    var spawn_position = camera.global_position - (camera.global_transform.basis.z * 3.0)
    spawn_position.y -= 1.0
    
    delorean.global_position = spawn_position
    
    # Lancement du shader de construction (Visual Effect)
    # Assumons que le modele a une MeshInstance3D nommée 'CarMesh'
    if delorean.has_node("CarMesh"):
        var mesh = delorean.get_node("CarMesh") as MeshInstance3D
        var material = mesh.get_surface_override_material(0)
        
        if material and material is ShaderMaterial:
            # Animation fluide (Tween) de 0 à 1 en 2.5 secondes
            var tween = get_tree().create_tween()
            tween.tween_property(material, "shader_parameter/construction_progress", 1.0, 2.5)
            print("[DeLoreanSpawner] Materialisation lancee...")
    else:
        print("[DeLoreanSpawner] Voiture placee avec succes!")
"""
    with open("scripts/vehicles/delorean_spawner.gd", "w", encoding="utf-8") as f:
        f.write(delorean_spawner_gd)
    print("-> Wrote scripts/vehicles/delorean_spawner.gd")

    # 3. Third-Person Controller (Emirthab Style for Desktop VR Fallback)
    tpc_gd = """# Fallback Third-Person Controller for Desktop Testing
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
"""
    with open("scripts/player/third_person_controller.gd", "w", encoding="utf-8") as f:
        f.write(tpc_gd)
    print("-> Wrote scripts/player/third_person_controller.gd")

    print("\n[SUCCESS] Demo features for your son have been built!")

if __name__ == "__main__":
    build_demo_features()
