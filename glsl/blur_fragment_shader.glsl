#version 330 core

in vec2 TexCoords;
out vec4 FragColor;

uniform sampler2D skyboxTexture;

void main()
{
    // Kernel básico de desenfoque de 3x3
    float offset = 1.0 / 300.0;  // Ajusta según el tamaño de la textura

    vec3 result = texture(skyboxTexture, TexCoords).rgb * 0.36;  // Centro del kernel
    result += texture(skyboxTexture, TexCoords + vec2(-offset,  offset)).rgb * 0.08;
    result += texture(skyboxTexture, TexCoords + vec2( offset,  offset)).rgb * 0.08;
    result += texture(skyboxTexture, TexCoords + vec2(-offset, -offset)).rgb * 0.08;
    result += texture(skyboxTexture, TexCoords + vec2( offset, -offset)).rgb * 0.08;
    result += texture(skyboxTexture, TexCoords + vec2(-offset,  0.0f)).rgb * 0.12;
    result += texture(skyboxTexture, TexCoords + vec2( offset,  0.0f)).rgb * 0.12;
    result += texture(skyboxTexture, TexCoords + vec2( 0.0f,   offset)).rgb * 0.12;
    result += texture(skyboxTexture, TexCoords + vec2( 0.0f,  -offset)).rgb * 0.12;

    FragColor = vec4(result, 1.0);
}
