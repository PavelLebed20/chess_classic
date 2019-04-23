import copy
import sys

import ChessAI.GameController.game_figures as Figures
from ChessBoard.chess_board import Board
from ChessBoard.chess_figure import FigureType, Side
from Vector2d.Vector2d import Vector2d, Move


class GameBoard:
    default_white_king_pos = Vector2d(4, 7)
    default_black_king_pos = Vector2d(4, 0)

    default_white_pawn_row = 6
    default_black_pawn_row = 1

    default_white_rook_right_pos = Vector2d(7, 7)
    default_white_rook_left_pos = Vector2d(0, 7)

    default_black_rook_right_pos = Vector2d(7, 0)
    default_black_rook_left_pos = Vector2d(0, 0)

    def __init__(self, chess_board):
        self.board = [[None for j in range(0, Board.ROW_SIZE)]
                      for i in range(0, Board.COLUMN_SIZE)]

        for i in range(0, Board.COLUMN_SIZE):
            for j in range(0, Board.ROW_SIZE):
                if chess_board.board[j][i] is None:
                    continue

                figure_type = chess_board.board[j][i].figure_type
                side = chess_board.board[j][i].side
                cur_pos = Vector2d(j, i)

                if figure_type == FigureType.KING:
                    was_moved = True
                    if side == Side.WHITE:
                        if cur_pos == GameBoard.default_white_king_pos:
                            was_moved = False
                    elif side == Side.BLACK:
                        if cur_pos == GameBoard.default_black_king_pos:
                            was_moved = False
                    self.board[j][i] = Figures.King(side, cur_pos, was_moved)

                elif figure_type == FigureType.QUEEN:
                    self.board[j][i] = Figures.Queen(side, cur_pos)

                elif figure_type == FigureType.ROOK:
                    was_moved = True
                    if side == Side.WHITE:
                        if cur_pos == GameBoard.default_white_rook_left_pos or cur_pos == GameBoard.default_white_rook_right_pos:
                            was_moved = False
                    elif side == Side.BLACK:
                        if cur_pos == GameBoard.default_black_rook_left_pos or cur_pos == GameBoard.default_black_rook_right_pos:
                            was_moved = False
                    self.board[j][i] = Figures.Rook(side, cur_pos, was_moved)

                elif figure_type == FigureType.KNIGHT:
                    self.board[j][i] = Figures.Knight(side, cur_pos)

                elif figure_type == FigureType.BISHOP:
                    self.board[j][i] = Figures.Bishop(side, cur_pos)

                elif figure_type == FigureType.PAWN:
                    was_moved = True
                    if side == Side.WHITE:
                        if i == GameBoard.default_white_pawn_row:
                            was_moved = False
                    elif side == Side.BLACK:
                        if i == GameBoard.default_black_pawn_row:
                            was_moved = False
                    self.board[j][i] = Figures.Pawn(side, cur_pos, was_moved)

                else:
                    continue

    def serialize_to_str(self):
        str_board = ['.' for j in range(0, Board.ROW_SIZE)
                        for i in range(0, Board.COLUMN_SIZE)]

        for i in range(0, Board.COLUMN_SIZE):
            for j in range(0, Board.ROW_SIZE):
                if self.board[j][i] is None:
                    continue
                str_board[i * Board.ROW_SIZE + j] = self.board[j][i].serialized_letter()
        return str_board

    def deserialize_from_str(self, str_board):
        self.board = [[None for j in range(0, Board.ROW_SIZE)]
                      for i in range(0, Board.COLUMN_SIZE)]

        for i in range(0, Board.COLUMN_SIZE):
            for j in range(0, Board.ROW_SIZE):
                letter = str_board[i * Board.ROW_SIZE + j]
                if letter.isupper():
                    side = Side.WHITE
                else:
                    side = Side.BLACK
                letter = letter.lower()
                cur_pos = Vector2d(j, i)

                if letter == 'k':
                    self.board[j][i] = Figures.King(side, cur_pos, False)
                elif letter == 'i':
                    self.board[j][i] = Figures.King(side, cur_pos, True)
                elif letter == 'b':
                    self.board[j][i] = Figures.Bishop(side, cur_pos)
                elif letter == 'r':
                    self.board[j][i] = Figures.Rook(side, cur_pos, False)
                elif letter == 'o':
                    self.board[j][i] = Figures.Rook(side, cur_pos, True)
                elif letter == 'n':
                    self.board[j][i] = Figures.Knight(side, cur_pos)
                elif letter == 'q':
                    self.board[j][i] = Figures.Queen(side, cur_pos)
                elif letter == 'p':
                    self.board[j][i] = Figures.Pawn(side, cur_pos)
                elif letter == 'a':
                    self.board[j][i] = Figures.Pawn(side, cur_pos, True)
                elif letter == 'w':
                    self.board[j][i] = Figures.Pawn(side, cur_pos, False, True)

    def export_chess_board(self):
        export_board = ['.' for j in range(0, Board.ROW_SIZE)
                        for i in range(0, Board.COLUMN_SIZE)]

        for i in range(0, Board.COLUMN_SIZE):
            for j in range(0, Board.ROW_SIZE):
                if self.board[j][i] is None:
                    continue
                figure_type = self.board[j][i].figure_type
                side = self.board[j][i].side

                if figure_type == FigureType.KING:
                    latter = 'k'
                elif figure_type == FigureType.QUEEN:
                    latter = 'q'
                elif figure_type == FigureType.ROOK:
                    latter = 'r'
                elif figure_type == FigureType.KNIGHT:
                    latter = 'n'
                elif figure_type == FigureType.BISHOP:
                    latter = 'b'
                elif figure_type == FigureType.PAWN:
                    latter = 'p'

                if side == Side.WHITE:
                    latter = latter.upper()
                export_board[i * Board.ROW_SIZE + j] = latter

        return export_board

    def print(self):
        sys.stdout.write(" ")
        sys.stdout.write(" ")
        sys.stdout.write(" ")
        for i in range(0, Board.ROW_SIZE):
            sys.stdout.write(i.__str__())
            sys.stdout.write(" ")
        print()
        print()

        for i in range(0, Board.COLUMN_SIZE):
            sys.stdout.write(i.__str__())
            sys.stdout.write(" ")
            sys.stdout.write(" ")
            for j in range(0, Board.ROW_SIZE):
                if self.board[j][i] is not None:
                    self.board[j][i].print()
                    sys.stdout.write(" ")
                else:
                    sys.stdout.write("*")
                    sys.stdout.write(" ")
            print()

    def print_attacked_cells(self):
        for i in range(0, Board.COLUMN_SIZE):
            for j in range(0, Board.ROW_SIZE):
                if self.board[j][i] is not None:
                    attack_cells = self.board[j][i].generate_moves(self)
                    self.board[j][i].print()
                    sys.stdout.write(": ")
                    for k in range(len(attack_cells)):
                        sys.stdout.write(attack_cells[k].x.__str__())
                        sys.stdout.write(" ")
                        sys.stdout.write(attack_cells[k].y.__str__())
                        sys.stdout.write("; ")
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
                    if isinstance(self.board[j][i], Figures.King) and self.board[j][i].side == side:
                        return Vector2d(j, i)

    def get_figures_list(self, side):
        figures = []
        for i in range(0, Board.COLUMN_SIZE):
            for j in range(0, Board.ROW_SIZE):
                if self.board[j][i] is not None:
                    if self.board[j][i].side == side:
                        figures.append(self.board[j][i])
        return figures

    def make_move(self, move):
        self.get(move.point_from).make_move(self, move.point_to)

    def summary_attacked_cells(self, side):
        attacked_cells = []
        for j in range(Board.ROW_SIZE):
            for i in range(Board.COLUMN_SIZE):
                figure = self.get_by_pos(j, i)
                if figure is not None and figure.side == side:
                    if isinstance(figure, Figures.King):
                        attacked_cells = attacked_cells + figure.generate_moves(self, False)
                    elif isinstance(figure, Figures.Pawn):
                        attacked_cells = attacked_cells + figure.generate_moves(self, True)
                    else:
                        attacked_cells = attacked_cells + figure.generate_moves(self)
        return attacked_cells

    def summary_moves(self, side, my_turn=True):
        summary_moves = []
        attacked_cells = []
        for j in range(Board.ROW_SIZE):
            for i in range(Board.COLUMN_SIZE):
                attacked_cells.clear()
                figure = self.get_by_pos(j, i)
                if figure is not None and figure.side == side:
                    if isinstance(figure, Figures.King):
                        attacked_cells = attacked_cells + figure.generate_moves(self, my_turn)
                    else:
                        attacked_cells = attacked_cells + figure.generate_moves(self)
                    for k in range(len(attacked_cells)):
                        summary_moves.append(Move(Vector2d(j, i), attacked_cells[k]))
        return summary_moves

    def is_that_check(self, my_side):
        attacked_cells = self.summary_attacked_cells(my_side)
        enemy_king_cell = self.get_king_cell(Side.get_oposite(my_side))
        return enemy_king_cell in attacked_cells

    def is_that_mate(self, my_side):
        enemy_figures = self.get_figures_list(Side.get_oposite(my_side))
        for i in range(len(enemy_figures)):
            cur_figure = enemy_figures[i]
            available_moves = cur_figure.generate_moves(self)
            for j in range(len(available_moves)):
                new_chess_board = copy.deepcopy(self)
                if new_chess_board.get(cur_figure.position) is None:
                    print(cur_figure.position.x)
                    print(cur_figure.position.y)
                new_chess_board.make_move(Move(cur_figure.position, available_moves[j]))
                if new_chess_board.is_that_check(my_side) is False:
                    return False
        return True

    def is_that_stalemate(self, my_side):
        enemy_figures = self.get_figures_list(Side.get_oposite(my_side))
        for i in range(len(enemy_figures)):
            cur_figure = enemy_figures[i]
            if isinstance(cur_figure, Figures.King) is not True:
                available_moves = cur_figure.generate_moves(self)
                if len(available_moves) != 0:
                    return False
            else:
                available_moves = cur_figure.generate_moves(self)
                for j in range(len(available_moves)):
                    new_chess_board = copy.deepcopy(self)
                    if new_chess_board.get(cur_figure.position) is None:
                        print(cur_figure.position.x)
                        print(cur_figure.position.y)

                    new_chess_board.make_move(Move(cur_figure.position, available_moves[j]))
                    if new_chess_board.is_that_check(my_side) is False:
                        return False
        return True

    def evaluate(self, side):
        total = 0
        for j in range(Board.ROW_SIZE):
            for i in range(Board.COLUMN_SIZE):
                pos = Vector2d(j, i)
                figure = self.get(pos)
                if figure is not None:
                    if figure.side is side:
                        sign = 1
                    else:
                        sign = -1
                    total = total + (figure.evaluate(j, i) * sign)
        return total
