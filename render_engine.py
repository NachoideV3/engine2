from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import QTimer
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image

class Model3DWidget(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # ~60 FPS
        self.model = None
        self.materials = {}
        self.current_material = None
        self.camera_distance = 20.0  # Distancia inicial de la cámara
        self.scale_factor = 1.0  # Factor de escala inicial

    def initializeGL(self):
        glutInit()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_NORMALIZE)

        # Configurar la luz
        light_pos = [5, 5, 5, 1]
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
        light_color = [1, 1, 1, 1]
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_color)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_color)

        glClearColor(0.0, 0.0, 0.0, 1.0)  # Fondo negro

    def load_texture(self, material_name, filename):
        try:
            image = Image.open(filename)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            image_data = np.array(image.convert("RGBA"), dtype=np.uint8)

            if material_name in self.materials:
                if 'texture_id' in self.materials[material_name]:
                    glDeleteTextures(self.materials[material_name]['texture_id'])
                self.materials[material_name]['texture_id'] = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, self.materials[material_name]['texture_id'])
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_data.shape[1], image_data.shape[0], 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                print(f"Textura cargada para el material {material_name}")
            else:
                print(f"Material {material_name} no encontrado para cargar la textura.")
        except Exception as e:
            print(f"Error al cargar la textura: {e}")

    def load_model(self, filename):
        print(f"Intentando abrir: {filename}")
        self.model = []
        vertices = []
        uvs = []
        faces = []
        self.current_material = None

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
                            faces.append((face_indices, face_uvs, self.current_material))
                        elif len(face_indices) > 3:
                            # Divide la cara en triángulos
                            for i in range(1, len(face_indices) - 1):
                                faces.append(([face_indices[0], face_indices[i], face_indices[i + 1]], 
                                            [face_uvs[0], face_uvs[i], face_uvs[i + 1]], 
                                            self.current_material))
                    elif line.startswith('usemtl '):  # Material
                        self.current_material = line.strip().split()[1]
                        if self.current_material not in self.materials:
                            self.materials[self.current_material] = {}
            self.model = (vertices, uvs, faces)
            print(f"Modelo cargado: {len(vertices)} vértices, {len(faces)} caras")
            print(f"Materiales: {self.materials.keys()}")
            self.update_materials()
        except Exception as e:
            print(f"Error al cargar el modelo: {e}")

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 3, self.camera_distance, 0, 0, 0, 0, 1, 0)  # Usar la distancia de la cámara

        # Dibujar el modelo 3D
        if self.model:
            vertices, uvs, faces = self.model
            glPushMatrix()
            glScalef(self.scale_factor, self.scale_factor, self.scale_factor)  # Aplicar escala
            for face, face_uvs, material_name in faces:
                if material_name and material_name in self.materials:
                    material = self.materials[material_name]
                    if 'texture_id' in material:
                        glEnable(GL_TEXTURE_2D)
                        glBindTexture(GL_TEXTURE_2D, material['texture_id'])
                    else:
                        glDisable(GL_TEXTURE_2D)
                else:
                    glDisable(GL_TEXTURE_2D)  # Desactivar textura por defecto

                glBegin(GL_TRIANGLES)
                for vertex_index, uv_index in zip(face, face_uvs):
                    vertex = vertices[vertex_index]
                    if uv_index is not None:
                        uv = uvs[uv_index]
                        glTexCoord2f(uv[0], uv[1])
                    else:
                        glTexCoord2f(0, 0)  # Valor predeterminado si no hay UV
                    glVertex3f(*vertex)
                glEnd()
            glPopMatrix()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0:  # Scroll hacia arriba
            self.camera_distance -= 0.5
        else:  # Scroll hacia abajo
            self.camera_distance += 0.5
        self.camera_distance = max(1.0, self.camera_distance)  # Evitar acercarse demasiado
        self.update()  # Redibujar la escena

    def update_animation(self):
        self.update()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (w / h), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def update_materials(self):
        # Actualiza la lista de materiales en la ventana de texturas
        if self.parent() and hasattr(self.parent(), 'texture_window'):
            self.parent().texture_window.update_material_list()

    def set_scale(self, scale):
        self.scale_factor = scale
        self.update()
