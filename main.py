from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QFileDialog, QVBoxLayout, QWidget, QSlider, QLabel
from PyQt5.QtCore import Qt
from render_engine import Model3DWidget, TextureWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.model_widget = Model3DWidget()
        self.texture_window = TextureWindow(self.model_widget)

        self.setCentralWidget(self.model_widget)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Darkmoon Engine')
        self.setGeometry(100, 100, 1280, 720)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        open_action = QAction('Open Model', self)
        open_action.triggered.connect(self.open_model)
        file_menu.addAction(open_action)

        self.show()

    def open_model(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open Model File', '', 'OBJ Files (*.obj)')
        if filename:
            self.model_widget.load_model(filename)
            self.texture_window.update_material_list()
            self.texture_window.show()

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec_()
