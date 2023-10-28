#version 330 core

uniform float time;

in vec4 v_color;

void main()
{
    gl_FragColor = v_color;
}
