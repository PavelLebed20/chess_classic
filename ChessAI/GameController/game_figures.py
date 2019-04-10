import copy
import sys
from enum import Enum

import ChessAI.GameController.game_board as gb
from ChessAI.ChessPlayer.BotPlayer.figure_cost import pawn_cost, rook_cost, knight_cost, bishop_cost, queen_cost, \
    king_cost
from ChessBoard.chess_board import Board
from ChessBoard.chess_figure import Figure, FigureType, Side
from Vector2d.Vector2d import Vector2d, Move


class LineType(Enum):
    VERTICAL = 0,
    HORIZONTAL = 1
    LIKE_Y_EQUALS_X = 2
    LIKE_Y_EQUALS_MINUS_X = 3


def _is_none_or_enemy(chess_board, position, figure_side):
    if chess_board.get(position) is None or \
            chess_board.get(position).side != figure_side:
        return True
    return False


def _is_enemy(chess_board, position, figure_side):
    if chess_board.get(position) is not None and \
            chess_board.get(position).side != figure_side:
        return True
    return False


def _add_correct_cells_by_ray(position, correct_cells, chess_board, figure_side, dx, dy, step_len=Board.COLUMN_SIZE,
                              can_step_on_figure=True):
    delta = Vector2d(dx, dy)
    cur_step_len = 0

    while cur_step_len < step_len and \
            Board.ROW_SIZE > position.x + delta.x >= 0 and \
            0 <= position.y + delta.y < Board.COLUMN_SIZE and \
            _is_none_or_enemy(chess_board, position + delta, figure_side):

        if _is_enemy(chess_board, position + delta, figure_side):
            if can_step_on_figure:
                correct_cells.append(position + delta)
                break
            else:
                break
        elif _is_enemy(chess_board, position + delta, Side.get_oposite(figure_side)):
            break

        correct_cells.append(position + delta)
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


class FigureBase(Figure):
    def __init__(self, figure_type, side, position):
        super().__init__(figure_type, side, position)

    def make_move(self, chess_board, point_to):
        chess_board.set(point_to, self)
        chess_board.set(self.position, None)
        self.position = copy.deepcopy(point_to)


class King(FigureBase):
    def __init__(self, side, position, was_moved):
        super().__init__(FigureType.KING, side, position)
        self.was_moved = was_moved

    def roque_right(self, chess_board, correct_cells):

        # self does not move
        if self.was_moved is True:
            return

        # self not on check
        attack_cells = chess_board.summary_attacked_cells(Side.get_oposite(self.side))

        if self.position in attack_cells:
            return

        if self.side == Side.WHITE:
            default_rook_right_pos = gb.GameBoard.default_white_rook_right_pos
        else:
            default_rook_right_pos = gb.GameBoard.default_black_rook_right_pos

        right_rook = chess_board.get(default_rook_right_pos)

        # rook does not move
        if not (right_rook is not None and isinstance(right_rook, Rook) and right_rook.was_moved is False):
            return

        # not on attack cell
        if self.position + Vector2d(1, 0) in attack_cells:
            return

        ray_to_rook = []
        _add_correct_cells_by_ray(self.position, ray_to_rook, chess_board, Side.get_oposite(self.side), 1, 0)
        if len(ray_to_rook) == 0:
            return
        if chess_board.get(ray_to_rook[len(ray_to_rook) - 1]).position != default_rook_right_pos:
            return

        correct_cells.append(self.position + Vector2d(2, 0))

    def roque_left(self, chess_board, correct_cells):

        # self does not move
        if self.was_moved is True:
            return

        # self not on check
        attack_cells = chess_board.summary_attacked_cells(Side.get_oposite(self.side))

        if self.position in attack_cells:
            return

        if self.side == Side.WHITE:
            default_rook_right_pos = gb.GameBoard.default_white_rook_left_pos
        else:
            default_rook_right_pos = gb.GameBoard.default_black_rook_left_pos

        right_rook = chess_board.get(default_rook_right_pos)

        if not (right_rook is not None and isinstance(right_rook, Rook) and right_rook.was_moved is False):
            return

        if self.position + Vector2d(-1, 0) in attack_cells:
            return

        ray_to_rook = []
        _add_correct_cells_by_ray(self.position, ray_to_rook, chess_board, Side.get_oposite(self.side), -1, 0)
        if len(ray_to_rook) == 0:
            return
        if chess_board.get(ray_to_rook[len(ray_to_rook) - 1]).position != default_rook_right_pos:
            return

        correct_cells.append(self.position - Vector2d(2, 0))

    def generate_moves(self, chess_board, its_my_turn=True):
        correct_cells = []

        if its_my_turn is True:
            self.roque_right(chess_board, correct_cells)
            self.roque_left(chess_board, correct_cells)

        _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, 0, 1, 1)
        _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, 0, -1, 1)
        _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, 1, 1, 1)
        _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, -1, -1, 1)
        _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, 1, 0, 1)
        _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, -1, 0, 1)
        _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, 1, -1, 1)
        _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, -1, 1, 1)

        if its_my_turn is True:
            summary_attacked_cells = chess_board.summary_attacked_cells(Side.get_oposite(self.side))

            for i in range(len(summary_attacked_cells)):
                try:
                    correct_cells.remove(summary_attacked_cells[i])
                except ValueError:
                    pass
        return correct_cells

    def make_move(self, chess_board, point_to):
        self.was_moved = True
        # roque check
        if abs(point_to.x - self.position.x) > 1:
            chess_board.set(point_to, self)
            chess_board.set(self.position, None)

            if self.side is Side.WHITE:
                if point_to.x - self.position.x > 0:
                    rook_pos = gb.GameBoard.default_white_rook_right_pos
                    delta_rook = Vector2d(-1, 0)
                else:
                    rook_pos = gb.GameBoard.default_white_rook_left_pos
                    delta_rook = Vector2d(1, 0)
            else:
                if point_to.x - self.position.x > 0:
                    rook_pos = gb.GameBoard.default_black_rook_right_pos
                    delta_rook = Vector2d(-1, 0)
                else:
                    rook_pos = gb.GameBoard.default_black_rook_left_pos
                    delta_rook = Vector2d(1, 0)

            chess_board.make_move(Move(Vector2d(rook_pos.x, rook_pos.y), Vector2d((point_to + delta_rook).x, (point_to + delta_rook).y)))
            return
        super().make_move(chess_board, point_to)

    def print(self):
        if self.side == Side.WHITE:
            sys.stdout.write('K')
        else:
            sys.stdout.write('k')

    def evaluate(self, x, y):
        cost = king_cost
        if self.side == Side.BLACK:
            cost.reverse()
        return 900 + cost[y][x]


class Queen(FigureBase):
    def __init__(self, side, position):
        super().__init__(FigureType.QUEEN, side, position)

    def generate_moves(self, chess_board):
        correct_cells = []
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, LineType.VERTICAL)
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, LineType.HORIZONTAL)
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, LineType.LIKE_Y_EQUALS_X)
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, LineType.LIKE_Y_EQUALS_MINUS_X)

        return correct_cells

    def print(self):
        if self.side == Side.WHITE:
            sys.stdout.write('Q')
        else:
            sys.stdout.write('q')

    def evaluate(self, x, y):
        cost = queen_cost
        if self.side == Side.BLACK:
            cost.reverse()
        return 90 + queen_cost[y][x]


class Bishop(FigureBase):
    def __init__(self, side, position):
        super().__init__(FigureType.BISHOP, side, position)

    def generate_moves(self, chess_board):
        correct_cells = []
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, LineType.LIKE_Y_EQUALS_X)
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, LineType.LIKE_Y_EQUALS_MINUS_X)

        return correct_cells

    def print(self):
        if self.side == Side.WHITE:
            sys.stdout.write('B')
        else:
            sys.stdout.write('b')

    def evaluate(self, x, y):
        cost = bishop_cost
        if self.side == Side.BLACK:
            cost.reverse()
        return 30 + cost[y][x]


class Knight(FigureBase):
    def __init__(self, side, position):
        super().__init__(FigureType.KNIGHT, side, position)

    def generate_moves(self, chess_board):
        maybe_moves = [Vector2d(1, 2), Vector2d(-1, 2), Vector2d(2, 1), Vector2d(-2, 1), Vector2d(1, -2),
                       Vector2d(-1, -2), Vector2d(2, -1), Vector2d(-2, -1)]

        correct_cells = []

        for i in range(len(maybe_moves)):

            maybe_move = self.position + maybe_moves[i]
            if maybe_move.x >= Board.ROW_SIZE or maybe_move.x < 0:
                continue
            elif maybe_move.y >= Board.COLUMN_SIZE or maybe_move.y < 0:
                continue

            if _is_none_or_enemy(chess_board, self.position + maybe_moves[i], self.side) is True:
                correct_cells.append(self.position + maybe_moves[i])

        return correct_cells

    def print(self):
        if self.side == Side.WHITE:
            sys.stdout.write('N')
        else:
            sys.stdout.write('n')

    def evaluate(self, x, y):
        cost = knight_cost
        if self.side == Side.BLACK:
            cost.reverse()
        return 30 + cost[y][x]


class Rook(FigureBase):
    def __init__(self, side, position, was_moved):
        super().__init__(FigureType.ROOK, side, position)
        self.was_moved = was_moved

    def generate_moves(self, chess_board):
        correct_cells = []
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, LineType.VERTICAL)
        _add_correct_cells_by_line(self.position, correct_cells, chess_board, self.side, LineType.HORIZONTAL)

        return correct_cells

    def make_move(self, chess_board, point_to):
        self.was_moved = False
        super().make_move(chess_board, point_to)

    def print(self):
        if self.side == Side.WHITE:
            sys.stdout.write('R')
        else:
            sys.stdout.write('r')

    def evaluate(self, x, y):
        cost = rook_cost
        if self.side == Side.BLACK:
            cost.reverse()
        return 50 + cost[y][x]


class Pawn(FigureBase):
    def __init__(self, side, position, was_moved):
        super().__init__(FigureType.PAWN, side, position)
        self.prev_move = None

    def en_passant(self, chess_board, correct_cells, dx, dy):
        enemy_pawn = chess_board.get(self.position + Vector2d(dx, 0))
        if enemy_pawn is not None:
            if isinstance(enemy_pawn, Pawn) and enemy_pawn.side != self.side:
                if enemy_pawn.prev_move is not None and abs(enemy_pawn.prev_move.y - enemy_pawn.position.y) > 1:
                    correct_cells.append(self.position + Vector2d(dx, dy))

    def generate_moves(self, chess_board, is_attack=False):
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
            # en passent attack
            self.en_passant(chess_board, correct_cells, -1, delta_y)

            x = self.position.x - 1
            y = self.position.y + delta_y
            attack_cell = chess_board.get_by_pos(x, y)
            if attack_cell is not None and attack_cell.side != self.side or is_attack:
                correct_cells.append(Vector2d(x, y))

        if self.position.x < Board.ROW_SIZE - 1:
            # en passent attack
            self.en_passant(chess_board, correct_cells, 1, delta_y)

            x = self.position.x + 1
            y = self.position.y + delta_y
            attack_cell = chess_board.get_by_pos(x, y)
            if attack_cell is not None and attack_cell.side != self.side or is_attack:
                correct_cells.append(Vector2d(x, y))

        # pawn go forward
        if self.prev_move is None and not is_attack:
            _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, 0, delta_y, 2, False)
        else:
            _add_correct_cells_by_ray(self.position, correct_cells, chess_board, self.side, 0, delta_y, 1, False)

        return correct_cells

    def make_move(self, chess_board, point_to):
        self.prev_move = self.position
        passent_cells = []

        if self.side == Side.WHITE:
            delta_y = -1
        else:
            delta_y = 1

        if self.position.x < Board.ROW_SIZE - 1:
            self.en_passant(chess_board, passent_cells, 1, delta_y)
        if self.position.x > 0:
            self.en_passant(chess_board, passent_cells, -1, delta_y)

        if point_to in passent_cells:
            chess_board.set(point_to - Vector2d(0, delta_y), None)
            super().make_move(chess_board, point_to)
        else:
            super().make_move(chess_board, point_to)

    def print(self):
        if self.side == Side.WHITE:
            sys.stdout.write('P')
        else:
            sys.stdout.write('p')

    def evaluate(self, x, y):
        cost = pawn_cost
        if self.side == Side.BLACK:
            cost.reverse()
        return 10 + cost[y][x]

