# main.py
import sys
import os
os.environ['QT_QPA_PLATFORM'] = 'xcb'
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QComboBox, QAction, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt
from render_engine import Model3DWidget  # Importa desde render_engine.py

class TextureWindow(QWidget):
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

        # Añadir control de escala
        scale_layout = QHBoxLayout()
        self.scale_label = QLabel('Escala:')
        self.scale_slider = QSlider(Qt.Horizontal)
        self.scale_slider.setMinimum(1)
        self.scale_slider.setMaximum(200)
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

    def update_scale(self):
        scale_value = self.scale_slider.value() / 100  # Ajusta el valor
        print(f"Factor de escala: {scale_value}")
        self.model_widget.set_scale(scale_value)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Darkmoon Engine')
        self.setGeometry(100, 100, 1280, 720)

        self.model_widget = Model3DWidget()
        self.setCentralWidget(self.model_widget)

        # Inicializa la ventana de propiedades pero no la muestra
        self.texture_window = TextureWindow(self.model_widget)
        self.texture_window.setWindowTitle('Editor de Texturas')
        self.texture_window.setGeometry(900, 100, 300, 200)

        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')

        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # Añadir opción para mostrar la ventana de propiedades
        properties_action = QAction('Propiedades', self)
        properties_action.triggered.connect(self.toggle_properties_window)
        file_menu.addAction(properties_action)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Abrir Modelo 3D', '', 'Modelos (*.obj)')
        if filename:
            self.model_widget.load_model(filename)
            self.texture_window.update_material_list()

    def toggle_properties_window(self):
        if self.texture_window.isVisible():
            self.texture_window.hide()
        else:
            self.texture_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
