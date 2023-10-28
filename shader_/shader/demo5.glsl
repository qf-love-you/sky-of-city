#version 330 core

uniform float time;

uniform mat4 u_projectionMatrix;

uniform mat4 u_viewMatrix;

uniform int u_particleCount;

in vec4 a_position;
in float a_lifetime;

out vec4 v_color;

void main()
{

    float size = a_lifetime * 0.05;
    float alpha = max(0.0, 1.0 - a_lifetime);

    mat4 modelViewProjectionMatrix = u_projectionMatrix * u_viewMatrix;

    gl_PointSize = size;
    gl_Position = modelViewProjectionMatrix * a_position;

    v_color = vec4(1.0, 1.0, 1.0, alpha);
}
