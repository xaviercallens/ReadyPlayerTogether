@tool
extends EditorScript

# Dossier où le script Python a déposé les fichiers
const SOURCE_DIR = "D:/xdev/Oasis/GodotToImport/"
# Dossier de destination dans le projet Godot
const TARGET_DIR = "res://assets/oasis_mechas/"

func _run():
	print("🚀 Début de la conversion brute (Bypass .import)...")
	DirAccess.make_dir_recursive_absolute(TARGET_DIR)
	
	var dir = DirAccess.open(SOURCE_DIR)
	if dir:
		dir.list_dir_begin()
		var file_name = dir.get_next()
		while file_name != "":
			if not dir.current_is_dir() and file_name.get_extension().to_lower() == "glb":
				_convert_raw_glb_to_tscn(file_name)
			file_name = dir.get_next()
	
	EditorInterface.get_resource_filesystem().scan()
	print("✅ Toutes les conversions sont terminées !")

func _convert_raw_glb_to_tscn(file_name: String):
	var absolute_path = SOURCE_DIR + file_name
	print("Traitement de : ", file_name)
	
	# 1. Utilisation de GLTFDocument (comme pour vos avatars RPM)
	var gltf = GLTFDocument.new()
	var state = GLTFState.new()
	
	# On lit le fichier directement depuis le disque dur Windows !
	var err = gltf.append_from_file(absolute_path, state)
	if err != OK:
		printerr("❌ Impossible de parser le GLB brut : ", absolute_path)
		return
	
	# 2. Génération de l'arbre de nœuds en mémoire
	var root_node = gltf.generate_scene(state)
	
	# 3. Empaquetage dans une scène native Godot (.tscn)
	var packed_scene = PackedScene.new()
	packed_scene.pack(root_node)
	
	var save_path = TARGET_DIR + file_name.get_basename() + "_OASIS.tscn"
	ResourceSaver.save(packed_scene, save_path)
	print("✨ Sauvegardé avec succès : ", save_path)
