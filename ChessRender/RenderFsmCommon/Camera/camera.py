###############################
# MODULE: Chess main class    #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 27/04/2019     #
###############################
from math import cos, sin, pi


class Camera:
    WHITE_ANGLE = pi / 2
    BLACK_ANGLE = -pi / 2

    def __init__(self, camera, default_angle=WHITE_ANGLE):
        self.camera = camera
        self.radius = 15
        self.angle = default_angle
        self.mouse_wheel = self.z = 20
        self.old_x = 0
        self.old_y = 0
        self.x = 0
        self.y = 0

        self._set_pos()

    def update_pos(self, new_x, new_y):
        self.x += new_x - self.old_x
        self.old_x = new_x

        self.angle = self.x * 2

        self.y += new_y - self.old_y
        self.old_y = new_y

        self._set_pos()

    def update_on_mouse_wheel(self, mouse_wheel):
        self.mouse_wheel += mouse_wheel
        self.z = mouse_wheel * 10

        self._set_pos()

    def _set_pos(self):
        self.camera.setPos(cos(self.angle) * self.radius,
                           sin(self.angle) * self.radius, self.z)
        self.camera.lookAt(0, 0, 0)
