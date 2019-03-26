from ChessAI.GameController.game_board import GameBoard
import pickle

from ChessAI.GameController.game_controller import GameController


"""
@:param game_id
@:param player_num number of player whos won the game (0 or 1)
"""

def game_stop(self, game_id, winner_player_num):
    #call game_stop procedure

    #send stop_game messages to clients
    None

def update_board(self, game_id, move):
    #get previous board from data base

    #covert char[64] to board

    #call check_move(board, move)

    #if is good move -> call update_field_procedure

    #send update msg to clients (send new board)
    None

def start_find_game(self, user_id):
    #call start_find_game procedure

    #if game was started -> send start_game messages to clients
    None

def stop_find_game(self, user_id):
    #call stop_find_game procedure
    None