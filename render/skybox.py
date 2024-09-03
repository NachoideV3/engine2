from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from .loader.texture_loader import TextureLoader

class Skybox:
    def __init__(self):
        self.texture_id = None
        self.texture_loader = TextureLoader()

    def initialize(self):
        pass  # No se necesita una lista de visualización para un cubo

    def load_texture(self, texture_path):
        material_name = 'skybox_texture'
        self.texture_loader.load_texture(material_name, texture_path)
        self.texture_id = self.texture_loader.get_texture(material_name)

    def draw(self):
        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

        # Dibujar un cubo
        glPushMatrix()
        glDisable(GL_LIGHTING)  # Desactivar iluminación para el skybox
        glColor3f(1.0, 1.0, 1.0)  # Color blanco para el skybox

        # Definir las caras del cubo
        size = 20  # Tamaño del cubo
        vertices = [
            [-size, -size, -size], [size, -size, -size], [size, size, -size], [-size, size, -size],  # Frente
            [-size, -size, size], [size, -size, size], [size, size, size], [-size, size, size],  # Atrás
            [-size, -size, -size], [size, -size, -size], [size, -size, size], [-size, -size, size],  # Abajo
            [-size, size, -size], [size, size, -size], [size, size, size], [-size, size, size],  # Arriba
            [-size, -size, -size], [-size, size, -size], [-size, size, size], [-size, -size, size],  # Izquierda
            [size, -size, -size], [size, size, -size], [size, size, size], [size, -size, size]   # Derecha
        ]

        # Coordenadas de textura para el cubo (ajustar según sea necesario)
        tex_coords = [
            [0, 0], [1, 0], [1, 1], [0, 1],  # Frente
            [0, 0], [1, 0], [1, 1], [0, 1],  # Atrás
            [0, 0], [1, 0], [1, 1], [0, 1],  # Abajo
            [0, 0], [1, 0], [1, 1], [0, 1],  # Arriba
            [0, 0], [1, 0], [1, 1], [0, 1],  # Izquierda
            [0, 0], [1, 0], [1, 1], [0, 1]   # Derecha
        ]

        # Dibujar las caras del cubo
        faces = [
            [0, 1, 2, 3],  # Frente
            [4, 5, 6, 7],  # Atrás
            [8, 9, 10, 11],  # Abajo
            [12, 13, 14, 15],  # Arriba
            [16, 17, 18, 19],  # Izquierda
            [20, 21, 22, 23]  # Derecha
        ]

        for i, face in enumerate(faces):
            glBegin(GL_QUADS)
            for j, vertex_index in enumerate(face):
                glTexCoord2f(*tex_coords[i * 4 + j])
                glVertex3f(*vertices[vertex_index])
            glEnd()

        glEnable(GL_LIGHTING)  # Reactivar iluminación después del skybox
        glPopMatrix()

        if self.texture_id:
            glDisable(GL_TEXTURE_2D)
