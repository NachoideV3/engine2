from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QFileDialog, QComboBox, QWidget, QDoubleSpinBox
from PyQt5.QtGui import QPixmap, QIcon
import os

class ImagePreviewButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("background-color: #333333; color: cyan; border: 1px solid #555555;")
        self.setFixedSize(100, 100)
        self.image = None

    def set_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.image = pixmap
        self.set_icon(pixmap)

    def clear_image(self):
        self.setIcon(QIcon())
        self.image = None

    def set_icon(self, pixmap):
        icon = QIcon(pixmap)
        self.setIcon(icon)
        self.setIconSize(pixmap.size())

class Properties(QWidget):
    def __init__(self, model_widget):
        super().__init__()
        self.model_widget = model_widget
        self.scale_locked = False  # Bandera para saber si la escala está bloqueada
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Sección de Materials
        layout.addWidget(QLabel("Materials"))
        
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

        # Sección de Transform
        layout.addWidget(QLabel("Transform"))

        # Layout para Position
        position_layout = QHBoxLayout()
        self.position_x = self.create_transform_spinbox('X:')
        self.position_y = self.create_transform_spinbox('Y:')
        self.position_z = self.create_transform_spinbox('Z:')
        position_layout.addWidget(QLabel('Position:'))
        position_layout.addWidget(self.position_x)
        position_layout.addWidget(self.position_y)
        position_layout.addWidget(self.position_z)
        layout.addLayout(position_layout)

        # Layout para Rotation
        rotation_layout = QHBoxLayout()
        self.rotation_x = self.create_transform_spinbox('X:')
        self.rotation_y = self.create_transform_spinbox('Y:')
        self.rotation_z = self.create_transform_spinbox('Z:')
        rotation_layout.addWidget(QLabel('Rotation:'))
        rotation_layout.addWidget(self.rotation_x)
        rotation_layout.addWidget(self.rotation_y)
        rotation_layout.addWidget(self.rotation_z)
        layout.addLayout(rotation_layout)

        # Layout para Scale con botón de bloqueo
        scale_layout = QHBoxLayout()
        self.scale_x = self.create_transform_spinbox('X:', min_val=0.1)
        self.scale_y = self.create_transform_spinbox('Y:', min_val=0.1)
        self.scale_z = self.create_transform_spinbox('Z:', min_val=0.1)

        self.scale_lock_button = QPushButton()
        self.update_scale_lock_icon()
        self.scale_lock_button.setCheckable(True)
        self.scale_lock_button.clicked.connect(self.toggle_scale_lock)

        scale_layout.addWidget(QLabel('Scale:'))
        scale_layout.addWidget(self.scale_x)
        scale_layout.addWidget(self.scale_y)
        scale_layout.addWidget(self.scale_z)
        scale_layout.addWidget(self.scale_lock_button)

        layout.addLayout(scale_layout)

        # Conectar los spinboxes de escala para sincronización
        self.scale_x.valueChanged.connect(self.sync_scale_if_locked)
        self.scale_y.valueChanged.connect(self.sync_scale_if_locked)
        self.scale_z.valueChanged.connect(self.sync_scale_if_locked)

        self.setLayout(layout)

    def create_transform_spinbox(self, label_text, min_val=-1000, max_val=1000):
        spinbox = QDoubleSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setSingleStep(0.1)
        return spinbox

    def update_material_list(self):
        self.material_combo.clear()
        if self.model_widget:
            self.material_combo.addItems(self.model_widget.materials.keys())

    def on_material_changed(self, index):
        material_name = self.material_combo.currentText()
        print(f"Material seleccionado: {material_name}")
        self.update_texture_buttons(material_name)

    def update_texture_buttons(self, material_name):
        if material_name in self.model_widget.materials:
            material = self.model_widget.materials[material_name]
            self.albedo_button.set_image(material.get('albedo', ''))
            self.normal_button.set_image(material.get('normal', ''))
            self.roughness_button.set_image(material.get('roughness', ''))
            self.metalness_button.set_image(material.get('metalness', ''))
            self.ao_button.set_image(material.get('ao', ''))

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

    # Bloquear la escala uniformemente
    def toggle_scale_lock(self):
        self.scale_locked = not self.scale_locked
        self.update_scale_lock_icon()

    def update_scale_lock_icon(self):
        if self.scale_locked:
            pass
            self.scale_lock_button.setIcon(QIcon(QIcon.fromTheme("lock")))
        else:
            pass
            self.scale_lock_button.setIcon(QIcon(QIcon.fromTheme("unlock")))

    def sync_scale_if_locked(self):
        if self.scale_locked:
            sender = self.sender()
            scale_value = sender.value()
            self.scale_x.setValue(scale_value)
            self.scale_y.setValue(scale_value)
            self.scale_z.setValue(scale_value)
            
            # Actualizar el motor de renderizado
            self.model_widget.scale_factor = scale_value
            self.model_widget.update()
