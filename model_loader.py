import numpy as np

def load_model(filename):
    print(f"Intentando abrir: {filename}")
    model = []
    vertices = []
    uvs = []
    faces = []
    current_material = None
    materials = {}

    try:
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('v '):  # Vértices
                    vertex = list(map(float, line.strip().split()[1:]))
                    vertices.append(vertex)
                elif line.startswith('vt '):  # Coordenadas UV
                    uv = list(map(float, line.strip().split()[1:]))
                    uvs.append(uv)
                elif line.startswith('f '):  # Caras
                    face = line.strip().split()[1:]
                    face_indices = []
                    face_uvs = []
                    for part in face:
                        indices = part.split('/')
                        vertex_index = int(indices[0]) - 1
                        face_indices.append(vertex_index)
                        if len(indices) > 1 and indices[1]:
                            uv_index = int(indices[1]) - 1
                            face_uvs.append(uv_index)
                        else:
                            face_uvs.append(None)  # No hay coordenada UV
                    # Convertir la cara en triángulos
                    if len(face_indices) == 3:
                        faces.append((face_indices, face_uvs, current_material))
                    elif len(face_indices) > 3:
                        # Divide la cara en triángulos
                        for i in range(1, len(face_indices) - 1):
                            faces.append(([face_indices[0], face_indices[i], face_indices[i + 1]], 
                                        [face_uvs[0], face_uvs[i], face_uvs[i + 1]], 
                                        current_material))
                elif line.startswith('usemtl '):  # Material
                    current_material = line.strip().split()[1]
                    if current_material not in materials:
                        materials[current_material] = {}
        model = (vertices, uvs, faces)
        print(f"Modelo cargado: {len(vertices)} vértices, {len(faces)} caras")
        print(f"Materiales: {materials.keys()}")
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")
    
    return model, materials
