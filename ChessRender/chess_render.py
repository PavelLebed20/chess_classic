###############################
# MODULE: Chess render class  #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 03/03/2019     #
###############################

from enum import Enum

from direct.showbase.ShowBase import ShowBase


class RenderState(Enum):
    INPUT = 0,
    MENU = 1,
    GAME = 2


class Render(ShowBase):

    def __init__(self):
        """
        Initialize render function
        """
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
