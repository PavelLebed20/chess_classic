###############################
# MODULE: Chess figure class  #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 03/03/2019     #
###############################
import copy
from enum import Enum


class FigureType(Enum):
    KING = 0,
    QUEEN = 1,
    BISHOP = 2,
    KNIGHT = 3,
    ROOK = 4,
    PAWN = 5


class Side(Enum):
    WHITE = 0,
    BLACK = 1


class Figure:

    def __init__(self, figure_type, side, position):
        """
        Initialize ChessFigure class instance
        :param figure_type: type of chess figure (ChessFigureType)
        :param side: player side (ChessSide)
        :param position: board position (Vector2d)
        """
        self.figure_type = FigureType(figure_type)
        self.side = Side(side)
        self.position = copy.deepcopy(position)


