#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texCoord;

out vec2 TexCoord;

void main()
{
    gl_Position = vec4(position, 0.6); // Transformar el vértice en espacio de clip
    TexCoord = texCoord;  // Pasar las coordenadas de la textura al fragment shader
}
