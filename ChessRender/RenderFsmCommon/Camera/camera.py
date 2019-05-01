###############################
# MODULE: Chess main class    #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 27/04/2019     #
###############################
from math import cos, sin, pi


class Camera:
    WHITE_ANGLE = pi / 2
    BLACK_ANGLE = -pi / 2

    MAX_FOV = 45
    MIN_FOV = 20


    def __init__(self, camera, lens, default_angle=WHITE_ANGLE):
        self.default_angle = default_angle
        self.lens = lens
        self.camera = camera
        self.radius = 15
        self.angle = self.default_angle
        self.z = 18
        self.old_x = 0
        self.old_y = 0
        self.x = cos(self.angle) * self.radius
        self.y = sin(self.angle) * self.radius

        self.fov_angle = (self.MAX_FOV + self.MIN_FOV) / 2

        self.lens.setFov(self.fov_angle)
        self._set_pos()

    def set_default(self):
        self.radius = 15
        self.angle = self.default_angle
        self.z = 18
        self.old_x = 0
        self.old_y = 0
        self.x = cos(self.angle) * self.radius
        self.y = sin(self.angle) * self.radius

        self.fov_angle = (self.MAX_FOV + self.MIN_FOV) / 2

        self.lens.setFov(self.fov_angle)
        self._set_pos()


    def update_pos(self, new_x, new_y):
        self.angle += (new_x - self.old_x) * 2

        self.x = cos(self.angle) * self.radius
        self.y = sin(self.angle) * self.radius

        self.old_y = new_y
        self.old_x = new_x

        self._set_pos()

    def update_on_mouse_wheel(self, mouse_wheel):
        #self.x += mouse_wheel
        if (self.fov_angle < self.MIN_FOV and mouse_wheel > 0 or
            self.fov_angle > self.MAX_FOV and mouse_wheel < 0):
            return
        self.fov_angle -= mouse_wheel
        self._set_pos()

    def _set_pos(self):
        self.camera.setPos(self.x, self.y, self.z)
        self.camera.lookAt(0, 0, 0)
        self.lens.setFov(self.fov_angle)

    def start_rotating(self, new_x, new_y):
        self.old_x = new_x
        self.old_y = new_y