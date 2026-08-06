import os

BASE_DIR = r"C:\Users\Utilisateur\.gemini\antigravity\scratch\project_oasis"

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip())

# ==============================================================================
# 1. ENHANCED CYBERPUNK HUB SCRIPT (oasis_hub.gd)
# ==============================================================================
HUB_GD = """
extends Node3D

# ==============================================================================
# PROJET OASIS - Cyberpunk Hub Central Controller
# Manages portal teleportation to the 10 Ready Player One demo scenes.
# ==============================================================================

@export var default_avatar_url: String = "https://models.readyplayer.me/64bfa15f0e72c63d7e3934a6.glb"

func _ready() -> void:
	print("[OASIS HUB] Cyberpunk Hub initialized. RTX 2070 Shaders Active.")
	_connect_portals()

func _connect_portals() -> void:
	for i in range(1, 11):
		var portal_name = "Portal_%02d" % i
		var portal_node = get_node_or_null("Portals/" + portal_name)
		if portal_node:
			portal_node.body_entered.connect(_on_portal_entered.bind(i))

func _on_portal_entered(body: Node3D, demo_index: int) -> void:
	if body.is_in_group("player"):
		print("[OASIS HUB] Player entered Portal %02d! Teleporting..." % demo_index)
		var scene_paths = [
			"res://scenes/demos/scene_01_the_stacks.tscn",
			"res://scenes/demos/scene_02_hallidays_journal.tscn",
			"res://scenes/demos/scene_03_copper_race.tscn",
			"res://scenes/demos/scene_04_distracted_globe.tscn",
			"res://scenes/demos/scene_05_arcade_retro.tscn",
			"res://scenes/demos/scene_06_planet_doom.tscn",
			"res://scenes/demos/scene_07_overlook_hotel.tscn",
			"res://scenes/demos/scene_08_ioi_citadel.tscn",
			"res://scenes/demos/scene_09_crystal_castle.tscn",
			"res://scenes/demos/scene_10_easter_egg.tscn"
		]
		if demo_index >= 1 and demo_index <= scene_paths.size():
			get_tree().change_scene_to_file(scene_paths[demo_index - 1])
"""

# ==============================================================================
# 2. ENHANCED RPM AVATAR LOADER SCRIPT (rpm_avatar_loader.gd)
# ==============================================================================
RPM_LOADER_GD = """
extends Node3D
class_name RPMAvatarLoader

# ==============================================================================
# PROJET OASIS - Ready Player Me Universal Avatar Loader
# Downloads GLB/GLTF avatars at runtime and attaches them to the player rig.
# ==============================================================================

signal avatar_loaded(avatar_node: Node3D)
signal avatar_failed(error_message: String)

@export var avatar_url: String = "https://models.readyplayer.me/64bfa15f0e72c63d7e3934a6.glb"
@export var auto_load_on_start: bool = true

var http_request: HTTPRequest

func _ready() -> void:
	http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(_on_avatar_download_completed)
	
	if auto_load_on_start and not avatar_url.is_empty():
		load_avatar_from_url(avatar_url)

func load_avatar_from_url(url: String) -> void:
	print("[RPM Loader] Fetching avatar model from: ", url)
	var err = http_request.request(url)
	if err != OK:
		print("[RPM Loader] Error initiating HTTP request: ", err)
		avatar_failed.emit("HTTP Request Failed")

func _on_avatar_download_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if result != HTTPRequest.RESULT_SUCCESS or response_code != 200:
		print("[RPM Loader] Failed to download RPM avatar. HTTP Code: ", response_code)
		avatar_failed.emit("Download Failed")
		return
		
	print("[RPM Loader] Avatar GLB downloaded (%d bytes). Parsing GLTF..." % body.size())
	
	var gltf_doc = GLTFDocument.new()
	var gltf_state = GLTFState.new()
	
	var err = gltf_doc.append_from_buffer(body, "", gltf_state)
	if err == OK:
		var avatar_scene = gltf_doc.generate_scene(gltf_state)
		if avatar_scene:
			# Remove previous avatar instances
			for child in get_children():
				if child != http_request:
					child.queue_free()
			
			add_child(avatar_scene)
			avatar_scene.name = "RPMAvatarModel"
			avatar_scene.transform.basis = Basis.from_scale(Vector3(1, 1, 1))
			print("[RPM Loader] Ready Player Me Avatar successfully attached to player!")
			avatar_loaded.emit(avatar_scene)
	else:
		print("[RPM Loader] Error parsing GLTF buffer: ", err)
		avatar_failed.emit("GLTF Parsing Error")
"""

# Write GDScript files
write_file(os.path.join(BASE_DIR, "scripts/hub/oasis_hub.gd"), HUB_GD)
write_file(os.path.join(BASE_DIR, "scripts/avatars/rpm_avatar_loader.gd"), RPM_LOADER_GD)

# ==============================================================================
# 3. CYBERPUNK HUB SCENE (oasis_hub.tscn)
# ==============================================================================
HUB_TSCN = """
[gd_scene load_steps=12 format=3 uid="uid://oasis_hub_cyberpunk"]

[ext_resource type="Script" path="res://scripts/hub/oasis_hub.gd" id="1_hub_script"]
[ext_resource type="PackedScene" uid="uid://pc_player_scene" path="res://scenes/player_vr/pc_player.tscn" id="2_player"]

[subresource type="Environment" id="Environment_cyberpunk"]
background_mode = 1
background_color = Color(0.02, 0.01, 0.05, 1)
glow_enabled = true
glow_intensity = 2.5
glow_bloom = 0.6
glow_blend_mode = 0
volumetric_fog_enabled = true
volumetric_fog_density = 0.015
volumetric_fog_albedo = Color(0.0, 0.7, 1.0, 1)
ssr_enabled = true

[subresource type="StandardMaterial3D" id="Mat_Floor"]
albedo_color = Color(0.05, 0.05, 0.08, 1)
metallic = 0.85
roughness = 0.15

[subresource type="CylinderMesh" id="Mesh_Floor"]
material = SubResource("Mat_Floor")
top_radius = 20.0
bottom_radius = 20.0
height = 0.5

[subresource type="StandardMaterial3D" id="Mat_Portal"]
albedo_color = Color(0.0, 1.0, 0.8, 1)
emission_enabled = true
emission = Color(0.0, 1.0, 0.8, 1)
emission_energy_multiplier = 4.0

[subresource type="TorusMesh" id="Mesh_Portal"]
material = SubResource("Mat_Portal")
inner_radius = 1.8
outer_radius = 2.2

[subresource type="CylinderShape3D" id="Shape_Portal"]
height = 3.0
radius = 2.0

[subresource type="BoxShape3D" id="Shape_Floor"]
size = Vector3(40, 0.5, 40)

[node name="OasisHub" type="Node3D"]
script = ExtResource("1_hub_script")

[node name="WorldEnvironment" type="WorldEnvironment" parent="."]
environment = SubResource("Environment_cyberpunk")

[node name="DirectionalLight3D" type="DirectionalLight3D" parent="."]
transform = Transform3D(0.866025, -0.353553, 0.353553, 0, 0.707107, 0.707107, -0.5, -0.612372, 0.612372, 0, 15, 0)
light_color = Color(0.4, 0.8, 1.0, 1)
light_energy = 1.5
shadow_enabled = true

[node name="CentralPlatform" type="StaticBody3D" parent="."]

[node name="MeshInstance3D" type="MeshInstance3D" parent="CentralPlatform"]
mesh = SubResource("Mesh_Floor")

[node name="CollisionShape3D" type="CollisionShape3D" parent="CentralPlatform"]
shape = SubResource("Shape_Floor")

[node name="PCPlayer" parent="." instance=ExtResource("2_player")]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0)

[node name="HubTitle" type="Label3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 6, -10)
pixel_size = 0.02
text = "WELCOME TO THE OASIS
Ready Player Together"
font_size = 72
outline_size = 16

[node name="Portals" type="Node3D" parent="."]

"""

# Append 10 portal nodes arranged in a circle
import math

portal_names = [
    "01: The Stacks", "02: Halliday's Journal", "03: Copper Race",
    "04: Distracted Globe", "05: Retro Arcade", "06: Planet Doom",
    "07: Overlook Hotel", "08: IOI Citadel", "09: Crystal Castle", "10: Easter Egg"
]

portals_tscn = ""
for i in range(1, 11):
    angle = (i - 1) * (2 * math.pi / 10)
    radius = 14.0
    x = math.cos(angle) * radius
    z = math.sin(angle) * radius
    rot_y = -angle + math.pi/2
    
    portals_tscn += f"""
[node name="Portal_{i:02d}" type="Area3D" parent="Portals"]
transform = Transform3D({math.cos(rot_y):.4f}, 0, {math.sin(rot_y):.4f}, 0, 1, 0, {-math.sin(rot_y):.4f}, 0, {math.cos(rot_y):.4f}, {x:.2f}, 2.0, {z:.2f})

[node name="MeshInstance3D" type="MeshInstance3D" parent="Portals/Portal_{i:02d}"]
transform = Transform3D(1, 0, 0, 0, -4.37114e-08, -1, 0, 1, -4.37114e-08, 0, 0, 0)
mesh = SubResource("Mesh_Portal")

[node name="CollisionShape3D" type="CollisionShape3D" parent="Portals/Portal_{i:02d}"]
shape = SubResource("Shape_Portal")

[node name="Label3D" type="Label3D" parent="Portals/Portal_{i:02d}"]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2.5, 0)
pixel_size = 0.015
text = "{portal_names[i-1]}"
font_size = 48
outline_size = 10
"""

write_file(os.path.join(BASE_DIR, "scenes/hub/oasis_hub.tscn"), HUB_TSCN + portals_tscn)

print("Cyberpunk Hub & RPM Avatar Loader built successfully.")
