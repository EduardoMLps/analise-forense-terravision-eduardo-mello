#version 330 core

in vec3 f_color;
in vec2 f_uvcoord;

out vec4 fragColor;

uniform sampler2D uTexture;

void main() {
    fragColor = texture(uTexture, f_uvcoord);
}