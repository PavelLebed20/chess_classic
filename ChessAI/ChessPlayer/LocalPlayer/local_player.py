###############################
# MODULE: Chess Player class  #
# AUTHOR: Pavel Lebed         #
# LAST UPDATE: 23/03/2019     #
###############################
import copy

from ChessAI.ChessPlayer.chess_player import Player
from ChessBoard.chess_figure import Side


class LocalPlayer(Player):

    def __init__(self, side):
        """
        Initialize player class function
        """
        self.side = Side(side)
        self.move = None

    def get_move(self):
        """
        Try get move calculation results
        :return: NONE - player don't make move yet,
                 move - otherwise
        """
        yield self.move
        self.move = None

    def set_move(self, move):
        """
        Render obtain player move function
        :param move: move to obtain
        :return: NONE.
        """
        self.move = copy.deepcopy(move)
