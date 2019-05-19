###############################
# MODULE: Chess Player class  #
# AUTHOR: Pavel Lebed         #
# LAST UPDATE: 07/04/2019     #
###############################
import copy
import threading
from random import randint
from ChessAI.ChessPlayer.chess_player import Player
from ChessAI.GameController.game_controller import MoveResult
from ChessBoard.chess_figure import Side
from random import shuffle
import ChessAI.GameController.game_figures as Figures

def evaluate_board(game_board):
    pass


class MinmaxBot(Player):

    def __init__(self, side, game_controller):
        """
        Initialize bot class function
        """
        super().__init__(side)
        self.side = Side(side)
        self.move = None
        self.game_controller = game_controller
        self.is_move_calculating = False
        self.value = None
        self.depth = 2
        self.pawn_swaped_figure = None
        self.pawn_swaped_latters = None
        if self.side is Side.WHITE:
            self.pawn_swaped_latters = ["Q", "N", "R", "B"]
        else:
            self.pawn_swaped_latters = ["q", "n", "r", "b"]

    def get_move(self):
        """
        Try get move calculation results
        :return: NONE - player don't make move yet,
                 move - otherwise
        """
        if not self.is_move_calculating:
            self.is_move_calculating = True

            self.move_calc_thread = threading.Thread(target=self.calc_best_move,
                                                     args=(self.depth, self.game_controller, self.side))
            self.move_calc_thread.start()
            return None
        if self.move_calc_thread.is_alive():
            return None
        self.is_move_calculating = False
        return self.move

    def set_move(self, move):
        """
        Render obtain player move function
        :param move: move to obtain
        :return: NONE.
        """
        return

    def get_pawn_swaped_figure(self):
        return self.pawn_swaped_figure

    def calculate_rand_move(self, game_controller):
        all_moves = game_controller.game_board.summary_moves(self.side)
        return all_moves[randint(0, len(all_moves) - 1)]

    def calc_best_move(self, depth, game, player_color,
                       alpha=-999999999,
                       beta=999999999,
                       is_maximizing_player=True):
        # Base case: evaluate board
        if depth == 0:
            value = game.game_board.evaluate(self.side)
            return value, None

        # Recursive case: search possible moves
        best_swaped_figure = None
        best_move = None  # best move not set yet
        possible_moves = game.game_board.summary_moves(player_color)

        # Set random order for possible moves
        shuffle(possible_moves)

        # Set a default best move value
        if is_maximizing_player:
            best_move_value = -99999999
        else:
            best_move_value = 99999999

        # Search through all possible moves
        for i in range(len(possible_moves)):
            move_res = game.check_move(possible_moves[i], player_color)
            if move_res is not MoveResult.INCORRECT:
                move = possible_moves[i]

                # Make the move, but undo before exiting loop
                new_game = copy.deepcopy(game)
                new_game.update(possible_moves[i], player_color)

                # pawn swaped check
                expected_pawn = new_game.game_board.get(move.point_to)
                if isinstance(expected_pawn, Figures.Pawn):
                    assert (self.pawn_swaped_latters is not None)
                    if expected_pawn.side is Side.WHITE:
                        if move.point_to.y == 0:
                            for figure_lat in self.pawn_swaped_latters:
                                new_game.swap_pawn(move.point_to, figure_lat)
                                value, move_side_effect = self.calc_best_move(depth - 1, new_game,
                                                                              Side.get_oposite(player_color),
                                                                              alpha, beta, not is_maximizing_player)
                                if is_maximizing_player:
                                    # Look for moves that maximize position
                                    if value > best_move_value:
                                        best_move_value = value
                                        best_move = move
                                        best_swaped_figure = figure_lat
                                    alpha = max(alpha, value)
                                else:
                                    # Look for moves that minimize position
                                    if value < best_move_value:
                                        best_move_value = value
                                        best_move = move
                                        best_swaped_figure = figure_lat
                                    beta = min(beta, value)

                                # Check for alpha beta pruning
                                if beta <= alpha:
                                    # print('Prune', alpha, beta)
                                    return best_move_value, best_move
                        else:
                            # Recursively get the value from this move
                            value, move_side_effect = self.calc_best_move(depth - 1, new_game,
                                                                          Side.get_oposite(player_color),
                                                                          alpha, beta, not is_maximizing_player)
                            if is_maximizing_player:
                                # Look for moves that maximize position
                                if value > best_move_value:
                                    best_move_value = value
                                    best_move = move
                                alpha = max(alpha, value)
                            else:
                                # Look for moves that minimize position
                                if value < best_move_value:
                                    best_move_value = value
                                    best_move = move
                                beta = min(beta, value)

                            # Check for alpha beta pruning
                            if beta <= alpha:
                                # print('Prune', alpha, beta)
                                return best_move_value, best_move

                    if expected_pawn.side is Side.BLACK:
                        if move.point_to.y == 7:
                            for figure_lat in self.pawn_swaped_latters:
                                new_game.swap_pawn(move.point_to, figure_lat)
                                value, move_side_effect = self.calc_best_move(depth - 1, new_game,
                                                                              Side.get_oposite(player_color),
                                                                              alpha, beta, not is_maximizing_player)
                                if is_maximizing_player:
                                    # Look for moves that maximize position
                                    if value > best_move_value:
                                        best_move_value = value
                                        best_move = move
                                        best_swaped_figure = figure_lat
                                    alpha = max(alpha, value)
                                else:
                                    # Look for moves that minimize position
                                    if value < best_move_value:
                                        best_move_value = value
                                        best_move = move
                                        best_swaped_figure = figure_lat
                                    beta = min(beta, value)

                                # Check for alpha beta pruning
                                if beta <= alpha:
                                    # print('Prune', alpha, beta)
                                    return best_move_value, best_move
                        else:
                            # Recursively get the value from this move
                            value, move_side_effect = self.calc_best_move(depth - 1, new_game,
                                                                          Side.get_oposite(player_color),
                                                                          alpha, beta, not is_maximizing_player)
                            if is_maximizing_player:
                                # Look for moves that maximize position
                                if value > best_move_value:
                                    best_move_value = value
                                    best_move = move
                                alpha = max(alpha, value)
                            else:
                                # Look for moves that minimize position
                                if value < best_move_value:
                                    best_move_value = value
                                    best_move = move
                                beta = min(beta, value)

                            # Check for alpha beta pruning
                            if beta <= alpha:
                                # print('Prune', alpha, beta)
                                return best_move_value, best_move
                else:
                    # Recursively get the value from this move
                    value, move_side_effect = self.calc_best_move(depth - 1, new_game, Side.get_oposite(player_color),
                                                                  alpha, beta, not is_maximizing_player)

                    if is_maximizing_player:
                        # Look for moves that maximize position
                        if value > best_move_value:
                            best_move_value = value
                            best_move = move
                        alpha = max(alpha, value)
                    else:
                        # Look for moves that minimize position
                        if value < best_move_value:
                            best_move_value = value
                            best_move = move
                        beta = min(beta, value)

                    # Check for alpha beta pruning
                    if beta <= alpha:
                        # print('Prune', alpha, beta)
                        return best_move_value, best_move

        if depth == self.depth:
            self.move = best_move
            self.value = best_move_value
            self.pawn_swaped_figure = best_swaped_figure

        return best_move_value, best_move
