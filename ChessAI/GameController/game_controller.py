############################################
# MODULE: Chess Game Controller class      #
# AUTHOR: Fedorov Dmitrii                  #
# LAST UPDATE: 03/03/2019                  #
############################################
import copy
import sys
from enum import Enum

from ChessAI.GameController.game_board import GameBoard
from ChessAI.GameController.game_figures import Pawn, King, Rook
from ChessBoard.chess_figure import Side
import pickle
from Vector2d.Vector2d import Vector2d, Move


class MoveResult(Enum):
    MATE = 0,
    CHECK = 1,
    STALEMATE = 2,
    DEFAULT = 3,
    INCORRECT = 4


class GameController:

    def __init__(self, chess_board, data=None):
        if chess_board is not None:
            self.game_board = GameBoard(chess_board)
        else:
            self.game_board = pickle.loads(data)

    def serialize(self):
        return pickle.dumps(self.game_board)

    def serialize_to_str(self):
        return self.game_board.serialize_to_str()

    def deserialize_from_str(self, str_board):
        self.game_board.deserialize_from_str(str_board)

    def export_to_chess_board_str(self):
        return self.game_board.export_chess_board()

    def update(self, move):
        figure = self.game_board.get(move.point_from)
        assert figure is not None
        self.game_board.make_move(move)

    def check_move(self, move, side):
        """
        Check current position state function
        :param side: player current side
        :param move: move figure sructure (Vector2d)
        :param chess_board: chess board class (see ChessBoard.Board)
        :return: MoveResult
        """
        result = MoveResult.INCORRECT

        figure_in_src = self.game_board.get(move.point_from)

        if figure_in_src is None:
            return result

        if figure_in_src.side != side:
            return result

        if figure_in_src is None:
            return result

        my_side = figure_in_src.side
        correct_moves = figure_in_src.generate_moves(self.game_board)
        if len(correct_moves) == 0:
            return result

        if move.point_to in correct_moves:
            result = MoveResult.DEFAULT

        if result == MoveResult.INCORRECT:
            return result

        new_game_board = copy.deepcopy(self.game_board)
        new_game_board.make_move(move)
        if new_game_board.is_that_check(Side.get_oposite(my_side)):
            result = MoveResult.INCORRECT

        if result == MoveResult.INCORRECT:
            return result

        if new_game_board.is_that_check(my_side):
            result = MoveResult.CHECK
            if new_game_board.is_that_mate(my_side):
                result = MoveResult.MATE
        else:
            if new_game_board.is_that_stalemate(my_side):
                result = MoveResult.STALEMATE

        return result

    def get_correct_move_for_cell(self, cell):
        """
        Return correct cells, that figure in cell make move to
        :param cell: coordinates of cell on chess board(Vector2d)
        :return: list of correct moves (Move[])
        """
        figure = self.game_board.get(cell)
        if figure is None:
            return None

        attacked_cells = []
        attacked_cells = attacked_cells + figure.generate_moves(self.game_board)
        res_cells = []
        for i in range(len(attacked_cells)):
            move = Move(cell, attacked_cells[i])
            if self.check_move(Move(cell, attacked_cells[i]), figure.side) is not MoveResult.INCORRECT:
                res_cells.append(attacked_cells[i])

        return res_cells


### USAGE EXAMPLE ###
# chess_board = Board()
# game_controller = GameController(chess_board)
# move = input_move
# if game_controller.check_move(move) != MoveResult.INCORRECT:
#    game_controller.update(move)
