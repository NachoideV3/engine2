from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def check_opengl_info():
    # Inicializa GLUT para poder usar OpenGL
    glutInit()
    
    # Crea una ventana invisible para obtener la información
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1, 1)
    glutCreateWindow(b"OpenGL Info")
    
    # Obtén información sobre OpenGL
    gl_version = glGetString(GL_VERSION)
    gl_renderer = glGetString(GL_RENDERER)
    gl_vendor = glGetString(GL_VENDOR)
    gl_shading_language_version = glGetString(GL_SHADING_LANGUAGE_VERSION)
    
    # Imprime la información
    print(f"OpenGL Version: {gl_version.decode('utf-8')}")
    print(f"Renderer: {gl_renderer.decode('utf-8')}")
    print(f"Vendor: {gl_vendor.decode('utf-8')}")
    print(f"Shading Language Version: {gl_shading_language_version.decode('utf-8')}")

if __name__ == "__main__":
    check_opengl_info()
