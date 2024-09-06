import sys
import os
os.environ['QT_QPA_PLATFORM'] = 'xcb'
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QComboBox, QAction, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from render.render_engine import Render  # Importa desde render_engine.py
from properties import Properties

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Darkmoon Engine')
        self.setGeometry(100, 100, 1280, 720)

        self.render_widget = Render()
        self.setCentralWidget(self.render_widget)

        # Crear un QLabel para mostrar FPS
        self.fps_label = QLabel(self)
        self.fps_label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 0.7); padding: 5px;")
        self.fps_label.move(10, 10)  # Posición inicial en la esquina superior izquierda
        self.fps_label.setMinimumSize(170, 40)
        #self.fps_label.hide()  # Ocultar inicialmente

        # Timer para actualizar FPS
        self.fps_timer = QTimer(self)
        self.fps_timer.timeout.connect(self.update_fps)
        self.fps_timer.start(1000)  # Actualiza cada segundo

        self.show_fps = True

        # Inicializa la ventana de propiedades pero no la muestra
        self.properties_widget = Properties(self.render_widget)
        self.properties_widget.setWindowTitle('Properties')
        self.properties_widget.setGeometry(900, 100, 300, 200)

        self.create_menu()

    def create_menu(self):
        self.menuBar().clear()
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        view_menu = menu_bar.addMenu('View')
        about_menu = menu_bar.addMenu('About')

        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        fps_action = QAction('Toggle FPS Overlay', self)
        fps_action.triggered.connect(self.toggle_fps_overlay)
        view_menu.addAction(fps_action)

        # Añadir opción para mostrar la ventana de propiedades
        properties_action = QAction('Properties', self)
        properties_action.triggered.connect(self.toggle_properties_window)
        file_menu.addAction(properties_action)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Abrir Modelo 3D', '', 'Modelos (*.obj)')
        if filename:
            self.render_widget.load_model(filename)
            self.properties_widget.update_material_list()
            self.create_menu()
        else:
            self.create_menu()

    def toggle_properties_window(self):
        if self.properties_widget.isVisible():
            self.properties_widget.hide()
        else:
            self.properties_widget.show()

    def toggle_fps_overlay(self):
        self.show_fps = not self.show_fps
        if self.show_fps:
            self.fps_label.show()
        else:
            self.fps_label.hide()

    def update_fps(self):
        if self.show_fps:
            fps = self.render_widget.get_fps()
            ms_per_frame = self.render_widget.get_ms_per_frame()
            self.fps_label.setText(f'FPS: {fps:.2f}, ms: {ms_per_frame:.2f}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
