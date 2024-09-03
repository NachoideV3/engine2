from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image

class Skybox:
    def __init__(self):
        self.skybox_texture = None

    def load_texture(self, filename):
        try:
            # Cargar la imagen y convertirla a formato adecuado para OpenGL
            image = Image.open(filename)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            image_data = np.array(image.convert("RGBA"), dtype=np.uint8)
            internal_format = GL_RGBA
            format = GL_RGBA
            type = GL_UNSIGNED_BYTE

            if self.skybox_texture:
                glDeleteTextures(self.skybox_texture)

            self.skybox_texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.skybox_texture)

            # Cargar la textura en OpenGL
            glTexImage2D(GL_TEXTURE_2D, 0, internal_format, image_data.shape[1], image_data.shape[0], 0, format, type, image_data)

            # Establecer parámetros de textura
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

            print(f"Textura del skybox cargada desde {filename}")
        except Exception as e:
            print(f"Error al cargar la textura del skybox: {e}")

    def initialize(self):
        # Cargar una textura predeterminada aquí, si lo deseas
        #self.load_texture('path/to/your/default_image.jpg')
        pass

    def draw(self):
        if self.skybox_texture:
            glDisable(GL_DEPTH_TEST)  # Desactiva el test de profundidad para el skybox
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.skybox_texture)
            glPushMatrix()

            size = 100.0  # Tamaño del skybox, ajusta según sea necesario

            # Dibujar un quad en lugar del cubo para representar el skybox
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0); glVertex3f(-size, -size, -size)
            glTexCoord2f(1, 0); glVertex3f(size, -size, -size)
            glTexCoord2f(1, 1); glVertex3f(size, size, -size)
            glTexCoord2f(0, 1); glVertex3f(-size, size, -size)
            glEnd()

            glPopMatrix()
            glEnable(GL_DEPTH_TEST)  # Reactiva el test de profundidad
            glDisable(GL_TEXTURE_2D)
