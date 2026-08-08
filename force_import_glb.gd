#!/usr/bin/env -S godot --headless --script
# Force import the Iron Giant GLB by using Godot's import API

extends Node

func _ready() -> void:
	print("=" * 60)
	print("Forcing Iron Giant GLB Import")
	print("=" * 60)
	
	var glb_path = "res://assets/iron_giant/3d_iron_giant_assignment.glb"
	
	# Get the import system
	var importer = EditorImportPlugin.new()
	
	# Force reimport of the GLB
	print("\n▶ Triggering GLB reimport...")
	
	# Use ResourceImporter to force the import
	if ResourceLoader.exists(glb_path):
		print("✓ GLB file found")
		
		# Try to load it - this should trigger the import
		var resource = load(glb_path)
		if resource != null:
			print("✓ GLB loaded successfully!")
			print(f"  Resource type: {resource.get_class()}")
		else:
			print("✗ Failed to load GLB")
	else:
		print("✗ GLB file not found at: " + glb_path)
	
	print("\n" + "=" * 60)
	print("Import process complete")
	print("=" * 60)
	
	get_tree().quit()
