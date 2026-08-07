# Matrix-Game Arcade Portal WebSocket Client (The Dreamer)
# Streams playable video onto a 3D Mesh (Arcade Screen or Portal) in VR.
class_name ArcadePortalClient
extends MeshInstance3D

@export var websocket_url: String = "ws://127.0.0.1:8006/ws/dream_portal"

var socket := WebSocketPeer.new()
var image := Image.new()
var image_texture := ImageTexture.new()

func _ready() -> void:
    # Appliquer la texture dynamique au materiel du Mesh (ex: un ecran d'arcade)
    var mat = StandardMaterial3D.new()
    mat.albedo_texture = image_texture
    mat.emission_enabled = true
    mat.emission_texture = image_texture
    mat.cull_mode = BaseMaterial3D.CULL_DISABLED
    set_surface_override_material(0, mat)
    
    var err = socket.connect_to_url(websocket_url)
    if err == OK:
        print("[ArcadePortal] Connecte au reve Matrix-Game sur ", websocket_url)
    else:
        print("[ArcadePortal] Echec de la connexion WebSocket.")

func _process(delta: float) -> void:
    socket.poll()
    var state = socket.get_ready_state()
    
    if state == WebSocketPeer.STATE_OPEN:
        # Lire les frames video entrantes
        while socket.get_available_packet_count() > 0:
            var packet = socket.get_packet()
            _update_portal_texture(packet)
            
        # Envoyer les inputs du joueur (WASD)
        _send_player_inputs()
        
    elif state == WebSocketPeer.STATE_CLOSED:
        pass # Handle reconnect if necessary

func _update_portal_texture(jpeg_bytes: PackedByteArray) -> void:
    var err = image.load_jpg_from_buffer(jpeg_bytes)
    if err == OK:
        if image_texture.get_size() == Vector2.ZERO:
            image_texture.set_image(image)
        else:
            image_texture.update(image)

func _send_player_inputs() -> void:
    var input_str = ""
    if Input.is_action_pressed("ui_up"): input_str += "W"
    if Input.is_action_pressed("ui_down"): input_str += "S"
    if Input.is_action_pressed("ui_left"): input_str += "A"
    if Input.is_action_pressed("ui_right"): input_str += "D"
    
    if input_str != "":
        socket.put_packet(input_str.to_utf8_buffer())
