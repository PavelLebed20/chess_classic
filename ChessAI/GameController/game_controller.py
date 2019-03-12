############################################
# MODULE: Chess Game Controller class      #
# AUTHOR: Fedorov Dmitrii                  #
# LAST UPDATE: 03/03/2019                  #
############################################
import sys
from enum import Enum
from Vector2d.Vector2d import Vector2d
import copy

from ChessBoard.chess_board import Board
from ChessBoard.chess_figure import Side, Figure, FigureType


class MoveResult(Enum):
    MATE = 0,
    CHECK = 1,
    STALEMATE = 2,
    DEFAULT = 3,
    INCORRECT = 4


class Move:
    def __init__(self, point_from, point_to):
        self.point_from = point_from
        self.point_to = point_to


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
        super().__init__(FigureType.KING, side, position)
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

        return correct_cells

    def print(self):
        sys.stdout.write('k')


class Queen(Figure):
    def __init__(self, side, position):
        super().__init__(FigureType.QUEEN, side, position)

    def generate_moves(self, chess_board):
        correct_cells = []
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, LineType.VERTICAL)
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, LineType.HORIZONTAL)
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, LineType.LIKE_Y_EQUALS_X)
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, LineType.LIKE_Y_EQUALS_MINUS_X)

    def print(self):
        sys.stdout.write('q')


class Bishop(Figure):
    def __init__(self, side, position):
        super().__init__(FigureType.BISHOP, side, position)

    def generate_moves(self, chess_board):
        correct_cells = []
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, LineType.LIKE_Y_EQUALS_X)
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, LineType.LIKE_Y_EQUALS_MINUS_X)


    def print(self):
        sys.stdout.write('b')


class Knight(Figure):
    def __init__(self, side, position):
        super().__init__(FigureType.KNIGHT, side, position)

    def generate_moves(self, chess_board):
        maybe_moves = [Vector2d(1, 2), Vector2d(-1, 2), Vector2d(2, 1), Vector2d(-2, 1), Vector2d(1, -2),
                       Vector2d(-1, -2), Vector2d(2, -1), Vector2d(-2, -1)]

        correct_moves = []

        for i in range(len(maybe_moves)):
            if _is_none_or_enemy(chess_board.get(self.position + maybe_moves.get(i))) is True:
                correct_moves.append(maybe_moves[i])

    def print(self):
        sys.stdout.write('n')


class Rook(Figure):
    def __init__(self, side, position):
        super().__init__(FigureType.ROOK, side, position)

    def generate_moves(self, chess_board):
        correct_cells = []
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, -1, 0)
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, 1, 0)
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, 0, -1)
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, 0, 1)

    def print(self):
        sys.stdout.write('r')


class Pawn(Figure):
    def __init__(self, side, position):
        super().__init__(FigureType.PAWN, side, position)
        self.was_moved = False

    def generate_moves(self, chess_board):
        correct_cells = []

        if self.side == Side.WHITE:
            delta_y = -1
        elif self.side == Side.BLACK:
            delta_y = 1
        else:
            assert (False, "generate moves: Pawn")
            return None

        # pawn attack figure
        if self.position.x > 0:
            x = self.position.x - 1
            y = self.position.y + delta_y
            attack_cell = chess_board.get_by_pos(x, y)
            if attack_cell is not None and attack_cell.Side != self.side:
                correct_cells.append(Vector2d(x, y))

        if self.position.x < Board.ROW_SIZE:
            x = self.position.x + 1
            y = self.position.y + delta_y
            attack_cell = chess_board.get_by_pos(x, y)
            if attack_cell is not None and attack_cell.side != self.side:
                correct_cells.append(Vector2d(x, y))

        # pawn go forward
        if self.was_moved is False:
            _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, 0, delta_y, 2)
        else:
            _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, 0, delta_y, 1)

        return correct_cells

    def print(self):
        sys.stdout.write('r')


class GameBoard:
    COLUMN_SIZE = 8
    ROW_SIZE = 8
    FULL_SIZE = COLUMN_SIZE * ROW_SIZE

    def __init__(self, chess_board):
        self.board = [[None for j in range(0, Board.ROW_SIZE)]
                      for i in range(0, Board.COLUMN_SIZE)]
        for i in range(0, Board.COLUMN_SIZE):
            for j in range(0, Board.ROW_SIZE):
                if chess_board.board[j][i] is None:
                    continue
                figure_type = chess_board.board[j][i].figure_type
                side = chess_board.board[j][i].side
                if figure_type == FigureType.KING:
                    self.board[j][i] = King(side, Vector2d(j, i))
                elif figure_type == FigureType.QUEEN:
                    self.board[j][i] = Queen(side, Vector2d(j, i))
                elif figure_type == FigureType.BISHOP:
                    self.board[j][i] = Bishop(side, Vector2d(j, i))
                elif figure_type == FigureType.KNIGHT:
                    self.board[j][i] = Knight(side, Vector2d(j, i))
                elif figure_type == FigureType.ROOK:
                    self.board[j][i] = Rook(side, Vector2d(j, i))
                elif figure_type == FigureType.PAWN:
                    self.board[j][i] = Pawn(side, Vector2d(j, i))
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

    def get_by_pos(self, x, y):
        return self.board[x][y]

    def get(self, position):
        return self.board[position.x][position.y]

    def set(self, position, game_object):
        self.board[position.x][position.y] = game_object

    def get_king_cell(self, side):
        for i in range(0, Board.COLUMN_SIZE):
            for j in range(0, Board.ROW_SIZE):
                if self.board[j][i] is not None:
                    if isinstance(self.board[j][i], King) and self.board[j][i].side == side:
                        return Vector2d(i, j)

    def get_figures_list(self, side):
        figures = []
        for i in range(0, Board.COLUMN_SIZE):
            for j in range(0, Board.ROW_SIZE):
                if self.board[j][i] is not None:
                    if isinstance(self.board[j][i], King) and self.board[j][i].side == side:
                        figures.append(self.board[j][i])
        return figures

    def make_move(self, move):
        self.set(move.point_to, self.get(move.point_from))
        self.set(move.point_from, None)


class GameController:

    @staticmethod
    def check_move(move, chess_board):
        """
        Check current position state function
        :param move: move figure sructure (Vector2d)
        :param chess_board: chess board class (see ChessBoard.Board)
        :return: MoveResult
        """
        game_board = GameBoard(chess_board)

        result = MoveResult.INCORRECT

        figure_in_src = game_board.get(move.point_from)

        if figure_in_src is None:
            return result

        my_side = figure_in_src.side
        correct_moves = figure_in_src.generate_moves(game_board)

        if move.point_to in correct_moves:
            result = MoveResult.DEFAULT

        if result is not MoveResult.DEFAULT:
            return result

        if GameController._is_that_check(game_board, my_side):
            result = MoveResult.CHECK
            if GameController._is_that_mate(game_board, my_side):
                result = MoveResult.MATE
        else:
            if GameController._is_that_stalemate(game_board, my_side):
                result = MoveResult.STALEMATE

        return result

    @staticmethod
    def _summary_attacked_cells(chess_board, side):
        attacked_cells = []
        for j in range(Board.ROW_SIZE):
            for i in range(Board.COLUMN_SIZE):
                if chess_board.get(j, i) is None or chess_board.get(j, i).side == side:
                    attacked_cells = attacked_cells + chess_board.get(j, i).generate_moves()
        return attacked_cells

    @staticmethod
    def _is_that_check(chess_board, my_side):
        attacked_cells = GameController._summary_attacked_cells(chess_board, my_side)
        enemy_king_cell = chess_board.get_king_cell()
        if enemy_king_cell in attacked_cells:
            return True

    @staticmethod
    def _is_that_mate(chess_board, my_side):
        enemy_figures = chess_board.get_figures_list(Side.get_oposite(my_side))
        for i in range(len(enemy_figures)):
            cur_figure = enemy_figures[i]
            available_moves = cur_figure.generate_moves(chess_board)
            for j in range(len(available_moves)):
                new_chess_board = copy.deepcopy(chess_board)
                new_chess_board.make_move(available_moves[j])
                if GameController._is_that_check(chess_board, my_side) is False:
                    return False

        return True

    @staticmethod
    def _is_that_stalemate(chess_board, my_side):
        enemy_figures = chess_board.get_figures_list(Side.get_oposite(my_side))
        for i in range(len(enemy_figures)):
            cur_figure = enemy_figures[i]
            if isinstance(cur_figure, King) is not True:
                available_moves = cur_figure.generate_moves(chess_board)
                if len(available_moves) != 0:
                    return False
            else:
                available_moves = cur_figure.generate_moves(chess_board)
                for j in range(len(available_moves)):
                    new_chess_board = copy.deepcopy(chess_board)
                    new_chess_board.make_move(available_moves[j])
                    if GameController._is_that_check(chess_board, my_side) is False:
                        return False
        return True
