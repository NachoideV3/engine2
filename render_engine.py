# render.py

from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import QTimer
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from skybox import Skybox
from texture_loader import TextureLoader
from model_loader import load_model  # Importar la función load_model

class Render(QOpenGLWidget):
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
        self.texture_loader = TextureLoader()  # Instanciar TextureLoader
        self.skybox = Skybox() 

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
        # Inicializar el skybox
        self.skybox.initialize()
        self.skybox.load_texture('hdri/meadow_2.jpg')

    def load_texture(self, material_name, filename):
        self.texture_loader.load_texture(material_name, filename)

    def load_model(self, filename):
        self.model, self.materials = load_model(filename)
        self.update_materials()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 3, self.camera_distance, 0, 0, 0, 0, 1, 0)  # Usar la distancia de la cámara

        # Dibujar el skybox
        self.skybox.draw()

        # Dibujar el modelo 3D
        if self.model:
            vertices, uvs, faces = self.model
            glPushMatrix()
            glScalef(self.scale_factor, self.scale_factor, self.scale_factor)  # Aplicar escala
            for face, face_uvs, material_name in faces:
                if material_name and material_name in self.materials:
                    texture_id = self.texture_loader.get_texture(material_name)
                    if texture_id:
                        glEnable(GL_TEXTURE_2D)
                        glBindTexture(GL_TEXTURE_2D, texture_id)
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
