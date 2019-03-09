###############################
# MODULE: Chess board class   #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 03/03/2019     #
###############################

# BOARD FORMAT DESCRIPTION
# uppercase letters - for white
# lowercase letters - for black
# K\k - king
# Q\q - queen
# B\b - bishop
# N\n - knight
# R\r - rook
# P\p - pawn
import copy
from typing import List

from vectormath import Vector2

from ChessBoard.chess_figure import Side, King, Queen, Bishop, Knight, Rook, Pawn


class Board:
    _DEFAULT_BOARD_POSITION = "rnbqkbkr" \
                              "pppppppp" \
                              "........" \
                              "........" \
                              "........" \
                              "........" \
                              "PPPPPPPP" \
                              "RNBQKBNR"

    COLUMN_SIZE = 8
    ROW_SIZE = 8
    FULL_SIZE = COLUMN_SIZE * ROW_SIZE

    def __init__(self, board_position=_DEFAULT_BOARD_POSITION):
        """
        Initialize ChessBoard class function
        :param board_position: board position in special format (str),
         see: BOARD_FORMAT_DESCRIPTION
        """
        assert len(board_position) == Board.FULL_SIZE
        self.board = [[None for j in range(0, Board.ROW_SIZE)]
                      for i in range(0, Board.COLUMN_SIZE)]
        for i in range(0, Board.COLUMN_SIZE):
            for j in range(0, Board.ROW_SIZE):
                figure_letter = board_position[i * Board.COLUMN_SIZE + j]
                if figure_letter.isupper():
                    side = Side.WHITE
                    figure_letter = figure_letter.lower()
                else:
                    side = Side.BLACK
                if figure_letter == 'k':
                    self.board[j][i] = King(side, Vector2(i, j))
                elif figure_letter == 'q':
                    self.board[j][i] = Queen(side, Vector2(i, j))
                elif figure_letter == 'b':
                    self.board[j][i] = Bishop(side, Vector2(i, j))
                elif figure_letter == 'n':
                    self.board[j][i] = Knight(side, Vector2(i, j))
                elif figure_letter == 'r':
                    self.board[j][i] = Rook(side, Vector2(i, j))
                elif figure_letter == 'p':
                    self.board[j][i] = Pawn(side, Vector2(i, j))
                else:
                    continue

    def print(self):
        for i in range(0, Board.COLUMN_SIZE):
            for j in range(0, Board.ROW_SIZE):
                if self.board[j][i] is not None:
                    self.board[j][i].print()
                else:
                    print(' ', end='')
            print()

    def get(self, x, y):
        return self.board[x][y]

    def get(self, position):
        return self.board[position.x][position.y]

    def get_king_cell(self, side):
        for i in range(0, Board.COLUMN_SIZE):
            for j in range(0, Board.ROW_SIZE):
                if (self.board[j][i] is not None):
                    if isinstance(self.board[j][i], King) and self.board[j][i].side == side:
                        return Vector2(i, j)

    def get_figures_list(self, side):
        figures = []
        for i in range(0, Board.COLUMN_SIZE):
            for j in range(0, Board.ROW_SIZE):
                if (self.board[j][i] is not None):
                    if isinstance(self.board[j][i], King) and self.board[j][i].side == side:
                        figures.append(self.board[j][i])
        return figures

    def make_move(self, move):
        cell_to = self.get(move.point_to)
        cell_from = self.get(move.point_from)
        cell_to = copy.deepcopy(cell_from)
        cell_from = None
