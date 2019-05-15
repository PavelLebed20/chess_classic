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
        super().__init__(side)
        self.side = Side(side)
        self.move = None
        self.pawn_swaped_figure = None

    def get_move(self):
        """
        Try get move calculation results
        :return: NONE - player don't make move yet,
                 move - otherwise
        """
        res = self.move
        self.move = None
        return res

    def get_pawn_swaped_figure(self):
        return self.pawn_swaped_figure

    def set_move(self, move, pawn_swaped_figure=None):
        """
        Render obtain player move function
        :param move: move to obtain
        :return: NONE.
        """
        self.move = copy.deepcopy(move)
        self.pawn_swaped_figure = pawn_swaped_figure
