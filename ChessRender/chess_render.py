###############################
# MODULE: Chess render class  #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 03/03/2019     #
###############################

from enum import Enum
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import WindowProperties
import ChessBoard

class RenderState(Enum):
    INPUT = 0,
    MENU = 1,
    GAME = 2

WIDTH = 480
HEIGHT = 480

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

        self.myImage = OnscreenImage(image = 'ChessRender/data/chess_board.png', pos = (0, 0, 0))
        
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
        print("rendering")
