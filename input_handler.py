from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWheelEvent

class InputHandler:
    def __init__(self, render_widget):
        self.render_widget = render_widget

    def handle_wheel_event(self, event: QWheelEvent):
        delta = event.angleDelta().y()
        if delta > 0:  # Scroll hacia arriba
            self.render_widget.camera_distance -= 0.5
        else:  # Scroll hacia abajo
            self.render_widget.camera_distance += 0.5
        self.render_widget.camera_distance = max(1.0, self.render_widget.camera_distance)  # Evitar acercarse demasiado
        self.render_widget.update()  # Redibujar la escena

    def handle_key_press_event(self, event):
        # Puedes añadir aquí el manejo de otras teclas si es necesario
        pass

    def handle_key_release_event(self, event):
        # Puedes añadir aquí el manejo de otras teclas si es necesario
        pass
