shader_type spatial;
render_mode cull_disabled, blend_mix;

uniform float construction_progress : hint_range(0.0, 1.0) = 0.0;
uniform vec4 neon_color : source_color = vec4(0.0, 0.9, 1.0, 1.0);
uniform float grid_frequency = 25.0;

varying vec3 local_vertex;

void vertex() {
	local_vertex = VERTEX;
}

void fragment() {
	// Bottom-to-top sweep on Y-axis (height: -1.0 to 1.5)
	float height_norm = (local_vertex.y + 1.0) / 2.5;
	
	if (height_norm > construction_progress) {
		discard; // Hide unconstructed geometry
	}
	
	// Holographic Neon Grid Pattern
	float grid_x = abs(sin(local_vertex.x * grid_frequency));
	float grid_z = abs(sin(local_vertex.z * grid_frequency));
	float grid_line = step(0.92, max(grid_x, grid_z));
	
	// Frontline edge scan effect
	float edge = smoothstep(construction_progress - 0.08, construction_progress, height_norm);
	
	ALBEDO = mix(vec3(0.1, 0.15, 0.25), neon_color.rgb, edge + grid_line * 0.5);
	METALLIC = 0.8;
	ROUGHNESS = 0.2;
	EMISSION = neon_color.rgb * (edge * 4.0 + grid_line * 2.0);
	ALPHA = mix(0.95, 1.0, edge);
}