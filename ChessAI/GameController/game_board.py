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

    def export_chess_board(self):
        export_board = [['.' for j in range(0, Board.ROW_SIZE)]
                      for i in range(0, Board.COLUMN_SIZE)]

        for i in range(0, Board.COLUMN_SIZE):
            for j in range(0, Board.ROW_SIZE):
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
                else:
                    continue

                if side == Side.WHITE:
                    latter = latter.upper()
                export_board[j][i] = latter

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
                    else:
                        attacked_cells = attacked_cells + figure.generate_moves(self)
        return attacked_cells

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
                new_chess_board.make_move(Move(Vector2d(cur_figure.position.x, cur_figure.position.y),
                                               Vector2d(available_moves[j].x, available_moves[j].y)))
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
                    new_chess_board.make_move(available_moves[j])
                    if new_chess_board.is_that_check(my_side) is False:
                        return False
        return True
