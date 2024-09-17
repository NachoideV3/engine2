from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QFileDialog, QComboBox, QWidget
from PyQt5.QtGui import QPixmap, QIcon

class ImagePreviewButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("background-color: #333333; color: cyan; border: 1px solid #555555;")  # Color oscuro
        self.setFixedSize(100, 100)  # Tamaño más pequeño para los botones de vista previa
        self.image = None

    def set_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.image = pixmap
        self.set_icon(pixmap)

    def clear_image(self):
        self.setIcon(QIcon())  # Limpia la imagen del botón
        self.image = None

    def set_icon(self, pixmap):
        icon = QIcon(pixmap)
        self.setIcon(icon)
        self.setIconSize(pixmap.size())

class Properties(QWidget):
    def __init__(self, model_widget):
        super().__init__()
        self.model_widget = model_widget
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.material_combo = QComboBox()
        self.material_combo.currentIndexChanged.connect(self.on_material_changed)
        layout.addWidget(self.material_combo)

        # Layout para Albedo
        albedo_layout = QHBoxLayout()
        self.albedo_button = ImagePreviewButton('Albedo')
        self.albedo_button.clicked.connect(self.load_albedo_texture)
        albedo_layout.addWidget(self.albedo_button)
        remove_albedo_button = QPushButton("Delete Albedo")
        remove_albedo_button.clicked.connect(self.remove_albedo_texture)
        albedo_layout.addWidget(remove_albedo_button)
        layout.addLayout(albedo_layout)

        # Layout para Normal
        normal_layout = QHBoxLayout()
        self.normal_button = ImagePreviewButton('Normal')
        self.normal_button.clicked.connect(self.load_normal_texture)
        normal_layout.addWidget(self.normal_button)
        remove_normal_button = QPushButton("Delete Normal")
        remove_normal_button.clicked.connect(self.remove_normal_texture)
        normal_layout.addWidget(remove_normal_button)
        layout.addLayout(normal_layout)

        # Layout para Roughness
        roughness_layout = QHBoxLayout()
        self.roughness_button = ImagePreviewButton('Roughness')
        self.roughness_button.clicked.connect(self.load_roughness_texture)
        roughness_layout.addWidget(self.roughness_button)
        remove_roughness_button = QPushButton("Delete Roughness")
        remove_roughness_button.clicked.connect(self.remove_roughness_texture)
        roughness_layout.addWidget(remove_roughness_button)
        layout.addLayout(roughness_layout)

        # Layout para Metalness
        metalness_layout = QHBoxLayout()
        self.metalness_button = ImagePreviewButton('Metalness')
        self.metalness_button.clicked.connect(self.load_metalness_texture)
        metalness_layout.addWidget(self.metalness_button)
        remove_metalness_button = QPushButton("Delete Metalness")
        remove_metalness_button.clicked.connect(self.remove_metalness_texture)
        metalness_layout.addWidget(remove_metalness_button)
        layout.addLayout(metalness_layout)

        # Layout para Ambient Occlusion
        ao_layout = QHBoxLayout()
        self.ao_button = ImagePreviewButton('Ambient Occlusion')
        self.ao_button.clicked.connect(self.load_ao_texture)
        ao_layout.addWidget(self.ao_button)
        remove_ao_button = QPushButton("Delete AO")
        remove_ao_button.clicked.connect(self.remove_ao_texture)
        ao_layout.addWidget(remove_ao_button)
        layout.addLayout(ao_layout)

        # Añadir control de escala
        scale_layout = QHBoxLayout()
        self.scale_label = QLabel('Scale:')
        self.scale_slider = QSlider(Qt.Horizontal)
        self.scale_slider.setMinimum(1)
        self.scale_slider.setMaximum(100000)
        self.scale_slider.setValue(1000)  # Valor inicial
        self.scale_slider.valueChanged.connect(self.update_scale)
        scale_layout.addWidget(self.scale_label)
        scale_layout.addWidget(self.scale_slider)
        layout.addLayout(scale_layout)

        self.setLayout(layout)

    def update_material_list(self):
        self.material_combo.clear()
        if self.model_widget:
            self.material_combo.addItems(self.model_widget.materials.keys())

    def on_material_changed(self, index):
        material_name = self.material_combo.currentText()
        print(f"Material seleccionado: {material_name}")
        # Actualizar los botones de vista previa de las texturas
        self.update_texture_buttons(material_name)

    def update_texture_buttons(self, material_name):
        if material_name in self.model_widget.materials:
            material = self.model_widget.materials[material_name]
            if 'albedo' in material:
                self.albedo_button.set_image(material['albedo'])
            else:
                self.albedo_button.clear_image()
            if 'normal' in material:
                self.normal_button.set_image(material['normal'])
            else:
                self.normal_button.clear_image()
            if 'roughness' in material:
                self.roughness_button.set_image(material['roughness'])
            else:
                self.roughness_button.clear_image()
            if 'metalness' in material:
                self.metalness_button.set_image(material['metalness'])
            else:
                self.metalness_button.clear_image()
            if 'ao' in material:
                self.ao_button.set_image(material['ao'])
            else:
                self.ao_button.clear_image()

    def load_albedo_texture(self):
        material_name = self.material_combo.currentText()
        filename, _ = QFileDialog.getOpenFileName(self, 'Cargar Textura Albedo', '', 'Imágenes (*.png *.jpg *.bmp)')
        if filename:
            print(f"Albedo para {material_name}: {filename}")
            self.model_widget.load_texture(material_name, filename)
            self.albedo_button.set_image(filename)

    def load_normal_texture(self):
        material_name = self.material_combo.currentText()
        filename, _ = QFileDialog.getOpenFileName(self, 'Cargar Textura Normal', '', 'Imágenes (*.png *.jpg *.bmp)')
        if filename:
            print(f"Normal para {material_name}: {filename}")
            self.model_widget.load_texture(material_name, filename)
            self.normal_button.set_image(filename)

    def load_roughness_texture(self):
        material_name = self.material_combo.currentText()
        filename, _ = QFileDialog.getOpenFileName(self, 'Cargar Textura Roughness', '', 'Imágenes (*.png *.jpg *.bmp)')
        if filename:
            print(f"Roughness para {material_name}: {filename}")
            self.model_widget.load_texture(material_name, filename)
            self.roughness_button.set_image(filename)

    def load_metalness_texture(self):
        material_name = self.material_combo.currentText()
        filename, _ = QFileDialog.getOpenFileName(self, 'Cargar Textura Metalness', '', 'Imágenes (*.png *.jpg *.bmp)')
        if filename:
            print(f"Metalness para {material_name}: {filename}")
            self.model_widget.load_texture(material_name, filename)
            self.metalness_button.set_image(filename)

    def load_ao_texture(self):
        material_name = self.material_combo.currentText()
        filename, _ = QFileDialog.getOpenFileName(self, 'Cargar Textura Ambient Occlusion', '', 'Imágenes (*.png *.jpg *.bmp)')
        if filename:
            print(f"Ambient Occlusion para {material_name}: {filename}")
            self.model_widget.load_texture(material_name, filename)
            self.ao_button.set_image(filename)

    # Métodos para Delete texturas individuales
    def remove_albedo_texture(self):
        material_name = self.material_combo.currentText()
        self.model_widget.remove_texture(material_name, 'albedo')
        self.albedo_button.clear_image()

    def remove_normal_texture(self):
        material_name = self.material_combo.currentText()
        self.model_widget.remove_texture(material_name, 'normal')
        self.normal_button.clear_image()

    def remove_roughness_texture(self):
        material_name = self.material_combo.currentText()
        self.model_widget.remove_texture(material_name, 'roughness')
        self.roughness_button.clear_image()

    def remove_metalness_texture(self):
        material_name = self.material_combo.currentText()
        self.model_widget.remove_texture(material_name, 'metalness')
        self.metalness_button.clear_image()

    def remove_ao_texture(self):
        material_name = self.material_combo.currentText()
        self.model_widget.remove_texture(material_name, 'ao')
        self.ao_button.clear_image()

    def update_scale(self):
        scale_value = self.scale_slider.value() / 100  # Ajusta el valor
        print(f"Scale: {scale_value}")
        self.model_widget.set_scale(scale_value)
