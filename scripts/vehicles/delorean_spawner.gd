# DeLorean Sci-Fi Spawner for Projet OASIS
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
