###############################
# MODULE: Chess main class    #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 27/04/2019     #
###############################
from direct.task import Task
from math import cos, sin, pi

from ChessBoard.chess_figure import Side


class Camera3D:
    WHITE_ANGLE = pi / 2
    BLACK_ANGLE = -pi / 2

    MAX_FOV = 45
    MIN_FOV = 20

    def __init__(self, camera, lens, win_w, win_h, default_angle=WHITE_ANGLE):
        self.MAX_FOV = pow(win_w / win_h, 0.5) * 45
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

        # for task_to_player_side_position
        self.need_to_change = 0
        self.change_step = 0
        self.steps = 0

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
        if self.fov_angle <= self.MIN_FOV and mouse_wheel > 0 or \
           self.fov_angle >= self.MAX_FOV and mouse_wheel < 0:
            return
        self.fov_angle -= mouse_wheel * 3 * pow(self.fov_angle / self.MAX_FOV, 2)
        # check angle right
        if self.fov_angle < self.MIN_FOV:
            self.fov_angle = self.MIN_FOV
        elif self.fov_angle > self.MAX_FOV:
            self.fov_angle = self.MAX_FOV
        self._set_pos()

    def _set_pos(self):
        self.camera.setPos(self.x, self.y, self.z)
        self.camera.lookAt(0, 0, 0)
        self.lens.setFov(self.fov_angle)

    def start_rotating(self, new_x, new_y):
        self.old_x = new_x
        self.old_y = new_y

    def prepare_task_goto_player_side_position(self, side, steps=60):
        if side is Side.WHITE:
            self.need_to_change = self.WHITE_ANGLE - self.angle
        else:
            self.need_to_change = self.BLACK_ANGLE - self.angle
        self.steps = steps
        self.change_step = self.need_to_change / self.steps

    def task_goto_player_side_position(self, task):
        self.angle += self.change_step
        self.steps -= 1
        self.x = cos(self.angle) * self.radius
        self.y = sin(self.angle) * self.radius
        self._set_pos()
        if self.steps == 0:
            return Task.done
        return Task.cont


class Camera2D:
    MAX_FOV = 45
    MIN_FOV = 20

    WHITE_ANGLE = 180
    BLACK_ANGLE = 0

    def __init__(self, camera, lens, win_w, win_h, angle=WHITE_ANGLE):
        self.angle = angle
        self.MAX_FOV = pow(win_w / win_h, 0.5) * 55
        self.lens = lens
        self.camera = camera
        self.z = 25
        self.x = 0
        if angle == 180: #WHITE_ANGLE
            self.y = -0.4
        else:
            self.y = 0.4

        self.fov_angle = (self.MAX_FOV + self.MIN_FOV) / 2

        self.lens.setFov(self.fov_angle)
        self._set_pos()
        self.camera.setH(angle)

    def set_default(self):
        pass

    def update_pos(self, new_x, new_y):
        pass

    def _set_pos(self):
        self.camera.setPos(self.x, self.y, self.z)
        self.camera.lookAt(0, 0, 0)
        self.lens.setFov(self.fov_angle)
        self.camera.setH(self.angle)

    def start_rotating(self, new_x, new_y):
        pass

    def update_on_mouse_wheel(self, mouse_wheel):
        if True:
            return
        if self.fov_angle <= self.MIN_FOV and mouse_wheel > 0 or \
           self.fov_angle >= self.MAX_FOV and mouse_wheel < 0:
            return
        self.fov_angle -= mouse_wheel * 3 * pow(self.fov_angle / self.MAX_FOV, 2)
        # check angle right
        if self.fov_angle < self.MIN_FOV:
            self.fov_angle = self.MIN_FOV
        elif self.fov_angle > self.MAX_FOV:
            self.fov_angle = self.MAX_FOV
        self._set_pos()


class CameraMenu:
    def __init__(self, camera, lens):
        self.lens = lens
        self.camera = camera
        self.radius = 15
        self.z = 0
        self.x = 0
        self.y = 0

        self.lookat_angle = 0

    def update_on_task_rotate(self, task):
        self.lookat_angle += 0.001
        self._set_pos()
        return Task.cont

    def _set_pos(self):
        self.camera.setPos(self.x, self.y, self.z)
        self.camera.lookAt(cos(self.lookat_angle), sin(self.lookat_angle), sin(self.lookat_angle))
        #self.lens.setFov(self.fov_angle)
