############################################
# MODULE: Chess Game Controller class      #
# AUTHOR: Fedorov Dmitrii                  #
# LAST UPDATE: 03/03/2019                  #
############################################

from enum import Enum
import Vector2d
import copy

from ChessBoard.chess_board import Board
from ChessBoard.chess_figure import Side, King


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


class GameController:

    @staticmethod
    def check_move(move, chess_board):
        """
        Check current position state function
        :param move: move figure sructure (Vector2d)
        :param chess_board: chess board class (see ChessBoard.Board)
        :return: MoveResult
        """
        result = MoveResult.INCORRECT

        figure_in_src = chess_board.get(move.point_from)

        if figure_in_src is None:
            return result

        my_side = figure_in_src.side
        correct_moves = figure_in_src.generate_moves(chess_board)

        if move.point_to in correct_moves:
            result = MoveResult.DEFAULT

        if result is not MoveResult.DEFAULT:
            return result

        if GameController._is_that_check(chess_board, my_side):
            result = MoveResult.CHECK
            if GameController._is_that_mate(chess_board, my_side):
                result = MoveResult.MATE
        else:
            if GameController._is_that_stalemate(chess_board, my_side):
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
        attacked_cells = GameController.summary_attacked_cells(chess_board, my_side)
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

