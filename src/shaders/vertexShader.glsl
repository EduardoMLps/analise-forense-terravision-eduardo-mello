#version 330 core

layout(location = 0) in vec2 a_pos;
layout(location = 1) in vec3 a_col;
layout(location = 2) in vec2 a_uvcoord;

out vec3 f_color;
out vec2 f_uvcoord;

void main() {
    f_color = a_col;
    f_uvcoord = a_uvcoord;
    gl_Position = vec4(a_pos, 0.0, 1.0);
}