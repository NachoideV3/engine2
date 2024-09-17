# texture_loader.py
from OpenGL.GL import *
import numpy as np
from PIL import Image, ImageFilter

class TextureLoader:
    def __init__(self):
        self.textures = {}

    def load_texture(self, material_name, filename, apply_blur=False, blur_radius=5):
        try:
            image = Image.open(filename)
            #blur
            if apply_blur:
                image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            image_data = np.array(image.convert("RGBA"), dtype=np.uint8)

            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_data.shape[1], image_data.shape[0], 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            if material_name in self.textures:
                glDeleteTextures(self.textures[material_name])
            self.textures[material_name] = texture_id
            print(f"Textura cargada para el material {material_name}")
        except Exception as e:
            print(f"Error al cargar la textura: {e}")

    def get_texture(self, material_name):
        return self.textures.get(material_name)
