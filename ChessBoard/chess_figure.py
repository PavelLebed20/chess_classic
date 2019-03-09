###############################
# MODULE: Chess figure class  #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 03/03/2019     #
###############################
import copy
from enum import Enum
import Vector2d
from ChessBoard.chess_board import Board


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

    @staticmethod
    def get_oposite(side):
        if side == Side.WHITE:
            return Side.BLACK
        else:
            return Side.WHITE

class Figure:

    def __init__(self, side, position):
        """
        Initialize ChessFigure class instance
        :param figure_type: type of chess figure (ChessFigureType)
        :param side: player side (ChessSide)
        :param position: board position (Vector2d)
        """
        self.side = Side(side)
        self.position = Vector2d(position)

    def print(self):
        pass

    def generate_moves(self, chess_board):
        return None


class LineType(Enum):
    VERTICAL = 0,
    HORIZONTAL = 1
    LIKE_Y_EQUALS_X = 2
    LIKE_Y_EQUALS_MINUS_X = 3


def _is_none_or_enemy(chess_board, position, figure_side):
    if chess_board.get(position) is None or \
            chess_board.get(position).Side != figure_side:
        return True
    return False


def _add_correct_cells_by_ray(position, correct_cells, chess_board, figure_side, dx, dy, step_len=Board.COLUMN_SIZE):
    delta = Vector2d(dx, dy)
    cur_step_len = 0

    while cur_step_len < step_len and \
            Board.ROW_SIZE > position.x + delta.x > 0 and \
            0 < position.y + delta.y < Board.COLUMN_SIZE and \
            _is_none_or_enemy(chess_board, position + delta, figure_side):
        correct_cells.append(position + delta)

        if chess_board.get(position + delta) is not None \
                and chess_board.get(position + delta).Side != figure_side:
            break

        delta.x = delta.x + dx
        delta.y = delta.y + dy
        cur_step_len = cur_step_len + 1


def _add_correct_cells_by_line(position, correct_cells, chess_board, figure_side, line_type):
    if line_type == LineType.VERTICAL:
        _add_correct_cells_by_ray(position, correct_cells, chess_board, figure_side, 0, 1)
        _add_correct_cells_by_ray(position, correct_cells, chess_board, figure_side, 0, -1)
    elif line_type == LineType.HORIZONTAL:
        _add_correct_cells_by_ray(position, correct_cells, chess_board, figure_side, 1, 0)
        _add_correct_cells_by_ray(position, correct_cells, chess_board, figure_side, -1, 0)
    elif line_type == LineType.LIKE_Y_EQUALS_X:
        _add_correct_cells_by_ray(position, correct_cells, chess_board, figure_side, 1, 1)
        _add_correct_cells_by_ray(position, correct_cells, chess_board, figure_side, -1, -1)
    elif line_type == LineType.LIKE_Y_EQUALS_MINUS_X:
        _add_correct_cells_by_ray(position, correct_cells, chess_board, figure_side, -1, 1)
        _add_correct_cells_by_ray(position, correct_cells, chess_board, figure_side, 1, -1)


class King(Figure):
    def __init__(self, side, position):
        super().__init__(side, position)
        self.was_moved = False

    def generate_moves(self, chess_board):
        correct_cells = []
        _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, 0, 1, 1)
        _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, 0, -1, 1)
        _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, 1, 1, 1)
        _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, -1, -1, 1)
        _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, 1, 0, 1)
        _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, -1, 0, 1)
        _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, 1, -1, 1)
        _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, -1, 1, 1)


class Queen(Figure):
    def __init__(self, side, position):
        super().__init__(side, position)

    def generate_moves(self, chess_board):
        correct_cells = []
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, LineType.VERTICAL)
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, LineType.HORIZONTAL)
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, LineType.LIKE_Y_EQUALS_X)
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, LineType.LIKE_Y_EQUALS_MINUS_X)


class Bishop(Figure):
    def __init__(self, side, position):
        super().__init__(side, position)

    def generate_moves(self, chess_board):
        correct_cells = []
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, LineType.LIKE_Y_EQUALS_X)
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, LineType.LIKE_Y_EQUALS_MINUS_X)


class Knight(Figure):
    def __init__(self, side, position):
        super().__init__(side, position)

    def generate_moves(self, chess_board):
        maybe_moves = [Vector2d(1, 2), Vector2d(-1, 2), Vector2d(2, 1), Vector2d(-2, 1), Vector2d(1, -2),
                       Vector2d(-1, -2), Vector2d(2, -1), Vector2d(-2, -1)]

        correct_moves = []

        for i in range(len(maybe_moves)):
            if _is_none_or_enemy(chess_board.get(self.position + maybe_moves.get(i))) is True:
                correct_moves.append(maybe_moves[i])


class Rook(Figure):
    def __init__(self, side, position):
        super().__init__(side, position)

    def generate_moves(self, chess_board):
        correct_cells = []
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, -1, 0)
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, 1, 0)
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, 0, -1)
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, 0, 1)


class Pawn(Figure):
    def __init__(self, side, position):
        super().__init__(side, position)
        self.was_moved = False

    def generate_moves(self, chess_board):
        correct_cells = []

        if self.side == Side.WHITE:
            delta_y = 1
        elif self.side == Side.BLACK:
            delta_y = -1
        else:
            assert (False, "generate moves: Pawn")
            return None

        # pawn attack figure
        if self.position.x > 0:
            x = self.position.x - 1
            y = self.position.y + delta_y
            attack_cell = chess_board.get(x, y)
            if attack_cell is not None and attack_cell.Side != self.side:
                correct_cells.append(Vector2d(x, y))

        if self.position.x < Board.ROW_SIZE:
            x = self.position.x + 1
            y = self.position.y + delta_y
            attack_cell = chess_board.get(x, y)
            if attack_cell is not None and attack_cell.Side != self.side:
                correct_cells.append(Vector2d(x, y))

        # pawn go forward
        if self.was_moved is False:
            _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, 0, delta_y, 2)
        else:
            _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, 0, delta_y, 1)

        return correct_cells
