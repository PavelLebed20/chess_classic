from cmath import cos, sin, sqrt, acos, atan, pi

#import numpy
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import BitMask32, LPoint3

from ChessRender.RenderFsmCommon.Camera.camera import Camera
from ChessRender.RenderFsmCommon.button_fsm import ButtonFsm
from ChessRender.RenderFsmCommon.screen_states import ScreenState
from ChessRender.UIPrimitives.object_manage import ObjectMngr

BLACK = (0, 0, 0, 1)
WHITE = (1, 1, 1, 1)


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


        self.camera_p = Camera(base.camera)
        base.disableMouse()

        # camera debug god mode
        #base.oobe()
        self.screen_atributes.buttons["but:Exit"] = ButtonFsm("Exit", (-1, 0, 0))
        self.initialize_button_links()

    def clear_state(self):
        for figure in self.figures:
            if figure is not None:
                figure.removeNode()
        for square in self.squares:
            square.removeNode()

    def initialize_button_links(self):
        self.screen_atributes.buttons["but:Exit"].add_command(self.clear_state)
        self.screen_atributes.buttons["but:Exit"].add_link("fsm:MainMenu")

    def mouse_task(self):
        mouse_watcher = base.mouseWatcherNode
        if mouse_watcher.hasMouse():
            self.camera_p.update_pos(mouse_watcher.getMouseX(), mouse_watcher.getMouseY())

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
                    #texture = loader.loadTexture("kek.png")
                    self.figures[key] = self.objMngr.load_figure_model(self.str_board[i + j * 8])
                    #self.figures[key].set_texture(texture)
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
