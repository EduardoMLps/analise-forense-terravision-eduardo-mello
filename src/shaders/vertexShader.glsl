#version 330 core

layout(location = 0) in vec3 a_pos;
layout(location = 1) in vec3 a_col;
layout(location = 2) in vec2 a_uvcoord;

out vec3 f_color;
out vec2 f_uvcoord;

uniform float rotationY;
uniform float rotationX;

void main() {
    mat4 rotY = mat4(
        cos(rotationY), 0.0, sin(rotationY), 0.0,
        0.0,            1.0, 0.0,            0.0,
        -sin(rotationY),0.0, cos(rotationY), 0.0,
        0.0,            0.0, 0.0,            1.0
    );

    mat4 rotX = mat4(
        1.0, 0.0,             0.0,            0.0,
        0.0, cos(rotationX), -sin(rotationX), 0.0,
        0.0, sin(rotationX),  cos(rotationX), 0.0,
        0.0, 0.0,             0.0,            1.0
    );


    f_color = a_col;
    f_uvcoord = a_uvcoord;
    gl_Position = rotX * rotY * vec4(a_pos, 1.0);
}