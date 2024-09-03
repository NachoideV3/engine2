class CameraController:
    def __init__(self):
        self.distance = 20.0  # Distancia inicial de la cámara
        self.position = [0, 3, 20]  # Posición de la cámara
        self.target = [0, 0, 0]  # Punto de enfoque de la cámara
        self.up_vector = [0, 1, 0]  # Vector hacia arriba de la cámara

    def zoom(self, amount):
        self.distance = max(1.0, self.distance + amount)
        self.update_position()

    def update_position(self):
        self.position = [0, 3, self.distance]

    def apply_view(self):
        gluLookAt(*self.position, *self.target, *self.up_vector)
