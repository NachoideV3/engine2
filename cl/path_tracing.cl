__kernel void path_tracing(__global float4* output_image, 
                           __global const float3* vertices,
                           __global const float3* normals,
                           __global const float4* materials,
                           const int width, const int height, 
                           const float3 camera_position,
                           const float3 light_position) {
    // Obtener la posición del píxel actual
    int x = get_global_id(0);
    int y = get_global_id(1);
    
    // Inicializar el color del píxel
    float4 color = (float4)(0.0f, 0.0f, 0.0f, 1.0f);

    // Generar rayos primarios desde la cámara hacia los píxeles de la imagen
    Ray ray = generate_ray(x, y, width, height, camera_position);
    
    // Verificar intersecciones y calcular la iluminación (sombras y rebotes)
    if(intersect(ray, vertices, normals, materials)) {
        color += compute_lighting(ray, light_position, vertices, normals);
    }

    // Escribir el color calculado en la imagen de salida
    output_image[y * width + x] = color;
}
