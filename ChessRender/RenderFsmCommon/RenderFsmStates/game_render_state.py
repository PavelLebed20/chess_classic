from cmath import cos, sin, sqrt, acos, atan, pi

#import numpy
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import BitMask32, LPoint3

from ChessRender.RenderFsmCommon.button_fsm import ButtonFsm
from ChessRender.RenderFsmCommon.screen_states import ScreenState
from ChessRender.UIPrimitives.object_manage import ObjectMngr

BLACK = (0, 0, 0, 1)
WHITE = (1, 1, 1, 1)


class SpherePosition:
    def __init__(self, r=0, theta=0, phi=0):
        self.r = r
        self.theta = theta
        self.phi = phi

    def to_decart(self):
        return DecartPosition(
            abs(self.r * sin(self.theta) * cos(self.phi)),
            abs(self.r * sin(self.theta) * sin(self.phi)),
            abs(self.r * cos(self.theta))
        )


class DecartPosition:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def to_sphere(self):
        r = abs((sqrt(self.x ** 2 + self.y ** 2, self.z ** 2)))

        return SpherePosition(
            r,
            atan(sqrt(self.x**2 + self.y**2) / z),
            atan(self.y / self.x)
        )


class FsmStateGameState(ScreenState):
    def __init__(self, render_fsm):
        ScreenState.__init__(self)
        self.render_fsm_ref = render_fsm
        self.objMngr = ObjectMngr()

        self.squares = [None for i in range(64)]
        self.init_nodes_to_chsess_board()

        self.str_board = "rnbqkbnr" \
                         "pppppppp" \
                         "........" \
                         "........" \
                         "........" \
                         "........" \
                         "PPPPPPPP" \
                         "RNBQKBNR"
        self.figures = [None for i in range(64)]
        self.init_nodes_to_figures()


        self.init_camera()
        decart_camera_pos = self.camera_pos.to_decart()
        base.camera.setPos(decart_camera_pos.x, decart_camera_pos.y, decart_camera_pos.z)
        base.camera.lookAt(0, 0, 0)
        base.disableMouse()

        # camera debug god mode
        #base.oobe()
        self.screen_atributes.buttons["but:Exit"] = ButtonFsm("Exit", (-1, 0, 0))
        self.initialize_button_links()

    def clear_state(self):
        #for figure in self.figures:
        #    figure.removeNode()
        for square in self.squares:
            square.removeNode()

    def initialize_button_links(self):
        self.screen_atributes.buttons["but:Exit"].add_command(self.clear_state)
        self.screen_atributes.buttons["but:Exit"].add_link("fsm:MainMenu")

    def init_camera(self):
        self.camera_radius = 20
        self.camera_pos = SpherePosition(self.camera_radius, 0, 0)
        self.new_mouse_x = 0
        self.new_mouse_y = 0
        self.prev_mouse_x = 0
        self.prev_mouse_y = 0

    def mouse_task(self):
        mouse_watcher = base.mouseWatcherNode
        if mouse_watcher.hasMouse():
            self.new_mouse_x = mouse_watcher.getMouseX()
            self.new_mouse_y = mouse_watcher.getMouseY()

            self.delta_mouse_x = self.new_mouse_x - self.prev_mouse_x
            self.delta_mouse_y = self.new_mouse_y - self.prev_mouse_y


            self.camera_pos.phi += self.delta_mouse_x* 5
            self.camera_pos.phi = self.camera_pos.phi % pi

            #if not (self.camera_pos.theta >= pi and self.delta_mouse_y > 0):
            self.camera_pos.theta += self.delta_mouse_y * 5
            #self.camera_pos.theta = self.camera_pos.theta % pi

            decart_camera_pos = self.camera_pos.to_decart()
            base.camera.setPos(decart_camera_pos.x, decart_camera_pos.y, decart_camera_pos.z)
            base.camera.lookAt(0, 0, 0)
            print("phi:")
            print(self.camera_pos.phi)
            print("theta:")
            print(self.camera_pos.theta)

            self.prev_mouse_x = mouse_watcher.getMouseX()
            self.prev_mouse_y = mouse_watcher.getMouseY()


    def init_nodes_to_figures(self):
        """
        Creation of figues on the board (visual interpretation)
        :param str_board: chess board in string format
        :return: figues: array of objects.
        """
        key = 0
        self.board_info = self.str_board

        for i in range(0, 8):
            for j in range(0, 8):
                if self.str_board[i + j * 8] != ".":
                    texture = loader.loadTexture("kek.png")
                    self.figures[key] = loader.loadModel("ChessRender/data/chess_figures/plane.egg")
                    self.figures[key].set_texture(texture)
                    self.figures[key].reparentTo(self.render_fsm_ref.render)
                    self.figures[key].setPos(self.SquarePosFig(i + j * 8))

                    self.figures[key].setTag("figue_tag", str(key))
                    key += 1

    def init_nodes_to_chsess_board(self):
        self.squareRoot = self.render_fsm_ref.render.attachNewNode("squareRoot")

        # For each square
        self.pieces = [None for i in range(64)]
        for i in range(64):
            # Load, parent, color, and position the model (a single square
            # polygon)
            self.squares[i] = loader.loadModel("ChessRender/data/chess_board/square")
            self.squares[i].reparentTo(self.squareRoot)
            self.squares[i].setPos(self.SquarePos(i))
            self.squares[i].setColor(self.SquareColor(i))
            # Set the model itself to be collideable with the ray. If this model was
            # any more complex than a single polygon, you should set up a collision
            # sphere around it instead. But for single polygons this works
            # fine.
            self.squares[i].find("**/polygon").node().setIntoCollideMask(
                BitMask32.bit(1))
            # Set a tag on the square's node so we can look up what square this is
            # later during the collision pass
            self.squares[i].find("**/polygon").node().setTag('square', str(i))

    def SquareColor(self, i):
        if (i + ((i // 8) % 2)) % 2:
            return BLACK
        else:
            return WHITE

    def SquarePos(self, i):
        return LPoint3((i % 8) - 3.5, int(i // 8) - 3.5, 0)

    def SquarePosFig(self, i):
        return LPoint3((i % 8) - 3.5, int(i // 8) - 3.5, 0.5)
