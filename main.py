import sys
import os
os.environ['QT_QPA_PLATFORM'] = 'xcb'
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QComboBox, QAction, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt
from render_engine import Model3DWidget  # Importa desde render_engine.py
from properties import TextureWindow

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
