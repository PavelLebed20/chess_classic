############################################
# MODULE: Chess Game Controller class      #
# AUTHOR: Fedorov Dmitrii                  #
# LAST UPDATE: 03/03/2019                  #
############################################

from enum import Enum


class MoveResult(Enum):
    MATE = 0,
    CHECK = 1,
    STALEMATE = 2,
    DEFAULT = 3,
    INCORRECT = 4


class GameController:
    
    @staticmethod
    def check_move(move, chess_board):
        """
        Check current position state function
        :param move: move figure sructure (Vector2d) 
        :param chess_board: chess board class (see ChessBoard.Board)
        :return: MoveResult 
        """
        pass
