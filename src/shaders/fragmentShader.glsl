#version 330 core

in vec3 f_color;
in vec2 f_uvcoord;

out vec4 fragColor;

uniform sampler2D my_texture;

void main() {
    fragColor = vec4(f_color, 1.0) * texture(my_texture, fragment_tex_coord);
}