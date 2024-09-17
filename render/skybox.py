from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from .loader.texture_loader import TextureLoader

class Skybox:
    def __init__(self):
        self.texture_id = None
        self.texture_loader = TextureLoader()
        self.rotation_angle_x = 0.0  # Ángulo de rotación en el eje X
        self.rotation_angle_y = 0.0  # Ángulo de rotación en el eje Y

    def initialize(self):
        pass  # No se necesita una lista de visualización para la esfera

    def load_texture(self, texture_path):
        material_name = 'skybox_texture'
        self.texture_loader.load_texture(material_name, texture_path, apply_blur=True, blur_radius=5)
        self.texture_id = self.texture_loader.get_texture(material_name)

    def draw(self):
        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glPushMatrix()
        # Desactivar iluminación para el skybox
        glDisable(GL_LIGHTING)
        glColor3f(1.0, 1.0, 1.0)  # Color blanco para la esfera

        # Aplicar rotación
        glRotatef(self.rotation_angle_x, 1.0, 0.0, 0.0)  # Rotar en el eje X
        glRotatef(self.rotation_angle_y, 0.0, 1.0, 0.0)  # Rotar en el eje Y

        # Dibujar una esfera en lugar del cubo
        size = 120  # Radio de la esfera
        quadric = gluNewQuadric()
        gluQuadricTexture(quadric, GL_TRUE)  # Activar coordenadas de textura en la esfera
        gluQuadricNormals(quadric, GL_NONE)
        gluSphere(quadric, size, 50, 50)  # Crear la esfera con textura

        glPopMatrix()

        if self.texture_id:
            glDisable(GL_TEXTURE_2D)

    def set_rotation(self, angle_x, angle_y):
        self.rotation_angle_x = angle_x
        self.rotation_angle_y = angle_y
