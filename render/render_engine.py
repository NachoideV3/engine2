import pyopencl as cl
import numpy as np
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import QTimer, QElapsedTimer
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileShader, compileProgram
from .skybox import Skybox
from .loader.texture_loader import TextureLoader
from .loader.model_loader import load_model
from input.input_handler import InputHandler
import os

class Render(QOpenGLWidget):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # ~60 FPS
        self.model = None
        self.materials = {}
        self.current_material = None
        self.camera_distance = 120.0  # Distancia inicial de la cámara
        self.scale_factor = 1.0  # Factor de escala inicial
        self.texture_loader = TextureLoader()  # Instanciar TextureLoader
        self.skybox = Skybox()
        self.input_handler = InputHandler(self)  # Instanciar InputHandler
        # Para calcular FPS y tiempo por cuadro
        self.elapsed_timer = QElapsedTimer()
        self.elapsed_timer.start()
        self.frame_count = 0
        self.fps = 0
        self.ms_per_frame = 0

        # Configuración para shaders
        self.shader_program = None

        # Configurar OpenCL
        self.cl_context = None
        self.cl_queue = None
        self.init_opencl()

    def init_opencl(self):
        try:
            platforms = cl.get_platforms()
            if not platforms:
                print("No OpenCL platforms found.")
                return
            devices = platforms[0].get_devices(device_type=cl.device_type.GPU)
            if not devices:
                print("No GPU devices found.")
                return
            self.cl_context = cl.Context([devices[0]])
            self.cl_queue = cl.CommandQueue(self.cl_context)
            print(f"OpenCL initialized with device: {devices[0].name}")
        except cl.Error as e:
            print(f"Error initializing OpenCL: {e}")

    def initializeGL(self):
        glutInit()
        glEnable(GL_DEPTH_TEST)

        # Cargar y compilar los shaders
        self.shader_program = self.create_shader_program("glsl/vertex_shader.glsl", "glsl/fragment_shader.glsl")

        # Configurar la textura del skybox
        self.skybox.initialize()
        self.skybox.load_texture('hdri/brown_photostudio_01.jpg')
        self.skybox.set_rotation(90, 180)

    def create_shader_program(self, vertex_file_path, fragment_file_path):
        """Función para cargar, compilar y enlazar shaders."""
        with open(vertex_file_path, 'r') as f:
            vertex_shader_source = f.read()
        with open(fragment_file_path, 'r') as f:
            fragment_shader_source = f.read()

        vertex_shader = compileShader(vertex_shader_source, GL_VERTEX_SHADER)
        fragment_shader = compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
        return compileProgram(vertex_shader, fragment_shader)

    def load_texture(self, material_name, filename):
        self.texture_loader.load_texture(material_name, filename)
        #self.use_texture = texture_loaded

    def load_model(self, filename):
        self.model, self.materials = load_model(filename)
        self.update_materials()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 3, self.camera_distance, 0, 0, 0, 0, 1, 0)  # Usar la distancia de la cámara

        # Usar el shader program
        glUseProgram(self.shader_program)


        # Dibujar el skybox
        #self.skybox.draw()

        # Realizar cálculos con OpenCL (ejemplo)
        self.perform_opencl_computation()

        # Dibujar el modelo 3D
        if self.model:
            vertices, uvs, faces = self.model
            glPushMatrix()
            glScalef(self.scale_factor, self.scale_factor, self.scale_factor)  # Aplicar escala
            for face, face_uvs, material_name in faces:
                texture_id = self.texture_loader.get_texture(material_name)
                if texture_id:
                    glActiveTexture(GL_TEXTURE0)
                    glBindTexture(GL_TEXTURE_2D, texture_id)

                glBegin(GL_TRIANGLES)
                for vertex_index, uv_index in zip(face, face_uvs):
                    vertex = vertices[vertex_index]
                    if uv_index is not None:
                        uv = uvs[uv_index]
                        glVertexAttrib2f(1, uv[0], uv[1])  # Pasar las coordenadas UV
                    glVertex3f(*vertex)
                glEnd()
            glPopMatrix()

        glUseProgram(0)  # Desactivar el programa de shader después de renderizar

        # Actualizar contador de cuadros y calcular FPS y ms por cuadro
        self.frame_count += 1
        elapsed = self.elapsed_timer.elapsed()  # Tiempo en milisegundos
        if elapsed > 1000:  # Calcular FPS y ms por cuadro cada segundo
            self.fps = self.frame_count / (elapsed / 1000.0)
            self.ms_per_frame = elapsed / self.frame_count
            self.frame_count = 0
            self.elapsed_timer.restart()

    def perform_opencl_computation(self):
        if self.cl_context and self.cl_queue:
            # Ejemplo de código OpenCL para realizar cálculos
            # Crea un buffer y un programa OpenCL aquí
            pass
        else:
            print("OpenCL not initialized. Skipping computation.")

    def wheelEvent(self, event):
        self.input_handler.handle_wheel_event(event)

    def keyPressEvent(self, event):
        self.input_handler.handle_key_press_event(event)

    def keyReleaseEvent(self, event):
        self.input_handler.handle_key_release_event(event)

    def update_animation(self):
        self.update()

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (w / h), 0.1, 100000.0)
        glMatrixMode(GL_MODELVIEW)

    def update_materials(self):
        # Actualiza la lista de materiales en la ventana de texturas
        if self.parent() and hasattr(self.parent(), 'texture_window'):
            self.parent().texture_window.update_material_list()

    def remove_texture(self, material_name, texture_type):
        if material_name in self.materials and texture_type in self.materials[material_name]:
            self.materials[material_name][texture_type] = None
            print(f"Textura {texture_type} eliminada del material {material_name}.")
        else:
            print(f"Error: No se puede eliminar la textura {texture_type} del material {material_name}.")

    def set_scale(self, scale):
        self.scale_factor = scale
        self.update()

    def get_fps(self):
        return self.fps

    def get_ms_per_frame(self):
        return self.ms_per_frame
