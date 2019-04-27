


class Camera:
    def __init__(self, camera):
        self.camera = camera
        self.camera_radius = 20
        self.x = 0
        self.y = 0

    def update_pos(self, new_x, new_y):
        self.x = new_x
        self.y = new_y