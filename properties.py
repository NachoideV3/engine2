from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QComboBox, QAction, QSlider, QHBoxLayout

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

        self.albedo_button = QPushButton('Cargar Albedo')
        self.albedo_button.clicked.connect(self.load_albedo_texture)
        layout.addWidget(self.albedo_button)

        self.normal_button = QPushButton('Cargar Normal')
        self.normal_button.clicked.connect(self.load_normal_texture)
        layout.addWidget(self.normal_button)

        # Botones adicionales para nuevas texturas
        self.roughness_button = QPushButton('Cargar Roughness')
        self.roughness_button.clicked.connect(self.load_roughness_texture)
        layout.addWidget(self.roughness_button)

        self.metalness_button = QPushButton('Cargar Metalness')
        self.metalness_button.clicked.connect(self.load_metalness_texture)
        layout.addWidget(self.metalness_button)

        self.ao_button = QPushButton('Cargar Ambient Occlusion')
        self.ao_button.clicked.connect(self.load_ao_texture)
        layout.addWidget(self.ao_button)

        # Añadir control de escala
        scale_layout = QHBoxLayout()
        self.scale_label = QLabel('Escala:')
        self.scale_slider = QSlider(Qt.Horizontal)
        self.scale_slider.setMinimum(1)
        self.scale_slider.setMaximum(2600)
        self.scale_slider.setValue(100)  # Valor inicial
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

    def load_albedo_texture(self):
        material_name = self.material_combo.currentText()
        filename, _ = QFileDialog.getOpenFileName(self, 'Cargar Textura Albedo', '', 'Imágenes (*.png *.jpg *.bmp)')
        if filename:
            print(f"Albedo para {material_name}: {filename}")
            self.model_widget.load_texture(material_name, filename)

    def load_normal_texture(self):
        material_name = self.material_combo.currentText()
        filename, _ = QFileDialog.getOpenFileName(self, 'Cargar Textura Normal', '', 'Imágenes (*.png *.jpg *.bmp)')
        if filename:
            print(f"Normal para {material_name}: {filename}")
            self.model_widget.load_texture(material_name, filename)

    def load_roughness_texture(self):
        material_name = self.material_combo.currentText()
        filename, _ = QFileDialog.getOpenFileName(self, 'Cargar Textura Roughness', '', 'Imágenes (*.png *.jpg *.bmp)')
        if filename:
            print(f"Roughness para {material_name}: {filename}")
            self.model_widget.load_texture(material_name, filename)

    def load_metalness_texture(self):
        material_name = self.material_combo.currentText()
        filename, _ = QFileDialog.getOpenFileName(self, 'Cargar Textura Metalness', '', 'Imágenes (*.png *.jpg *.bmp)')
        if filename:
            print(f"Metalness para {material_name}: {filename}")
            self.model_widget.load_texture(material_name, filename)

    def load_ao_texture(self):
        material_name = self.material_combo.currentText()
        filename, _ = QFileDialog.getOpenFileName(self, 'Cargar Textura Ambient Occlusion', '', 'Imágenes (*.png *.jpg *.bmp)')
        if filename:
            print(f"Ambient Occlusion para {material_name}: {filename}")
            self.model_widget.load_texture(material_name, filename)

    def update_scale(self):
        scale_value = self.scale_slider.value() / 100  # Ajusta el valor
        print(f"Factor de escala: {scale_value}")
        self.model_widget.set_scale(scale_value)
