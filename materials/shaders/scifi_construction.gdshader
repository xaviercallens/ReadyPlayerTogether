// Ready Player One DeLorean Construction Shader
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
