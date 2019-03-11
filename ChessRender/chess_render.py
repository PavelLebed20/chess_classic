###############################
# MODULE: Chess render class  #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 03/03/2019     #
###############################

from enum import Enum
from direct.showbase.ShowBase import ShowBase

from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import WindowProperties
from panda3d.core import TransparencyAttrib
from panda3d.core import LPoint3, LVector3
import sys

class RenderState(Enum):
    INPUT = 0,
    MENU = 1,
    GAME = 2

WIDTH = 480
HEIGHT = 480

CENTER_X = 3.5
CENTER_Y = 3.5
STEP_X = 3.7
STEP_Y = -3.7
DEPTH = 55

def trLiter(simbol):
    if (simbol.isupper()):
        return "w" + simbol
    else:
        return "b" + simbol.upper()

def posOfIndex(i, j):
    return LPoint3((i-CENTER_X)*STEP_X, (j-CENTER_Y)*STEP_Y, 0)

def loadObject(text=None, pos=LPoint3(0, 0), depth=DEPTH, scale=3,
               transparency=True):
    obj = loader.loadModel("ChessRender/data/chess_figues/plane")
    obj.reparentTo(camera)

    texture = loader.loadTexture(text)
    obj.set_texture(texture, 1)

    obj.setPos(pos.getX(), depth, pos.getY())
    obj.set_scale(scale)

    obj.setBin("unsorted", 0)
    obj.setDepthTest(False)
    if transparency:
        obj.setTransparency(TransparencyAttrib.MAlpha)
    return obj

class Render(ShowBase):

    def __init__(self):
        """
        Initialize render function
        """
        ShowBase.__init__(self)

        props = WindowProperties()
        props.clearSize()
        props.setSize(WIDTH, HEIGHT)
        self.win.requestProperties(props)

        self.chess_board = loadObject("ChessRender/data/chess_board.png", scale=29.5)

        for i in range(0, 8):
            for j in range(0, 8):
                if (i != 0)*(j != 0):
                    self.obj = loadObject("ChessRender/data/chess_figues/"+trLiter("k")+".png", posOfIndex(i, j))
                else:
                    self.obj = loadObject("ChessRender/data/chess_figues/"+trLiter("q")+".png", posOfIndex(i, j))

        print("Render initialize")

    def set_menu_state(self, buttons, text_fields, text_fields_obtainer_func):
        """
        Set render state to menu mode
        :param buttons: array buttons (see. UIPrimitives.button)
        :param text_fields: text fields array (see. TO DO)
        :param text_fields_obtainer_func: text fields result obtainer
        :return: NONE.
        """
        print("Set state to input")

    def set_game_state(self, chess_board, chess_board_obtainer_func,
                       buttons, text_fields, text_fields_obtainer_func):
        """
        Set render state to game mode
        :param chess_board: chess board class (see ChessBoard.Board)
        :param chess_board_obtainer_func: chess move result obtainer function
        :param buttons: array buttons (see. UIPrimitives.button)
        :param text_fields: text fields array (see. TO DO)
        :param text_fields_obtainer_func: text fields result obtainer
        :return: NONE.
        """
        print("Set state to game")

    def render(self):
        """
        Render scene function
        :return: NONE.
        """
        self.taskMgr.step()
