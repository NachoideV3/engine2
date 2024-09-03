from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from .loader.texture_loader import TextureLoader

class Skybox:
    def __init__(self):
        self.texture_id = None
        self.sphere_list = None
        self.texture_loader = TextureLoader()

    def initialize(self):
        # Generar una lista de visualización para la esfera del skybox
        self.sphere_list = glGenLists(1)
        glNewList(self.sphere_list, GL_COMPILE)
        #self.create_sphere(radius=50, lats=40, longs=40)
        glEndList()

    def load_texture(self, texture_path):
        # Usar un nombre genérico para el skybox como 'skybox_texture'
        material_name = 'skybox_texture'
        self.texture_loader.load_texture(material_name, texture_path)
        self.texture_id = self.texture_loader.get_texture(material_name)


    def create_sphere(self, radius, lats, longs):
        """ Crea una esfera para usarla como skybox """
        for i in range(lats):
            lat0 = np.pi * (-0.5 + float(i) / lats)
            z0 = np.sin(lat0)
            zr0 = np.cos(lat0)

            lat1 = np.pi * (-0.5 + float(i + 1) / lats)
            z1 = np.sin(lat1)
            zr1 = np.cos(lat1)

            glBegin(GL_QUAD_STRIP)
            for j in range(longs + 1):
                lng = 2 * np.pi * float(j) / longs
                x = np.cos(lng)
                y = np.sin(lng)

                glTexCoord2f(float(j) / longs, float(i) / lats)
                glVertex3f(x * zr0 * radius, y * zr0 * radius, z0 * radius)

                glTexCoord2f(float(j) / longs, float(i + 1) / lats)
                glVertex3f(x * zr1 * radius, y * zr1 * radius, z1 * radius)
            glEnd()

    def draw(self):
        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

        # Renderizar la esfera como skybox
        glPushMatrix()
        glDisable(GL_LIGHTING)  # Desactivar iluminación para el skybox
        glColor3f(1.0, 1.0, 1.0)  # Color blanco para el skybox
        glCallList(self.sphere_list)
        glEnable(GL_LIGHTING)  # Reactivar iluminación después del skybox
        glPopMatrix()

        if self.texture_id:
            glDisable(GL_TEXTURE_2D)
