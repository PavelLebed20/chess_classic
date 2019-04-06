###############################
# MODULE: Chess Player class  #
# AUTHOR: Pavel Lebed         #
# LAST UPDATE: 23/03/2019     #
###############################
import copy
from random import randint
from ChessAI.ChessPlayer.chess_player import Player
from ChessAI.GameController.game_controller import MoveResult
from ChessBoard.chess_figure import Side
from random import shuffle


def evaluate_board(game_board):
    pass


class MinmaxBot(Player):

    def __init__(self, side):
        """
        Initialize bot class function
        """
        self.side = Side(side)
        self.move = None

    def get_move(self, game_controller=None):
        """
        Try get move calculation results
        :return: NONE - player don't make move yet,
                 move - otherwise
        """
        value, move = self.calc_best_move(2, game_controller, self.side)
        return move

    def set_move(self, move):
        """
        Render obtain player move function
        :param move: move to obtain
        :return: NONE.
        """
        return

    def calculate_rand_move(self, game_controller):
        all_moves = game_controller.game_board.summary_moves(self.side)
        return all_moves[randint(0, len(all_moves) - 1)]

    def calc_best_move(self, depth, game, player_color,
                       alpha=-99999999,
                       beta=99999999,
                       is_maximizing_player=True):
        # Base case: evaluate board
        if depth == 0:
            value = game.game_board.evaluate(self.side)
            return value, None

        # Recursive case: search possible moves
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
            if game.check_move(possible_moves[i], player_color) is not MoveResult.INCORRECT:
                move = possible_moves[i]
                # Make the move, but undo before exiting loop
                new_game = copy.deepcopy(game)
                new_game.update(possible_moves[i])

                # Recursively get the value from this move
                value, move_side_effect = self.calc_best_move(depth - 1, new_game, Side.get_oposite(player_color), alpha, beta, not is_maximizing_player)

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
                    beta = min(beta, value);

                # Check for alpha beta pruning
                if beta <= alpha:
                    # print('Prune', alpha, beta)
                    return best_move_value, best_move

        return best_move_value, best_move
