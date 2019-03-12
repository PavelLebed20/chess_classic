###############################
# MODULE: Chess ChessAI class #
# AUTHOR: Fedorov Dmitrii     #
# LAST UPDATE: 03/03/2019     #
###############################

from ChessAI.ChessPlayer.chess_player import Player


class ChessAI(Player):

    def __init__(self, chess_board):
        """
        Initialize ChessAI class function
        :param chess_board: chess board to obtain
        """
        self.chess_board = chess_board

    def make_move(self):
        """
        Make player start calculate his move
        :return:
        """
        pass

    def get_move(self):
        """
        Try get move calculation results
        :return: NONE - player don't make move yet,
                 move - otherwise
        """
        pass
