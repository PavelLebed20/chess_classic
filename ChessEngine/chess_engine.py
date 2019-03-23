###############################
# MODULE: Chess engine class  #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 23/03/2019     #
###############################
from ChessAI.ChessPlayer.LocalPlayer.local_player import LocalPlayer
from ChessAI.GameController.game_controller import GameController, MoveResult
from ChessBoard.chess_board import Board
from ChessBoard.chess_figure import Side
from ChessRender.chess_render import Render


class Engine:

    def __init__(self):
        """
        Initialize Engine class function
        """
        self.render = Render()
        self.player_turn = 0
        self.players = [LocalPlayer(Side.WHITE), LocalPlayer(Side.BLACK)]
        self.players[0].make_move()
        self.chess_board = Board()
        self.game_controller = GameController(self.chess_board)

    def run(self):
        """
        Main loop function
        :return: NONE.
        """
        while True:
            move = self.players[self.player_turn].get_move()
            if move is not None:
                if self.game_controller.check_move(move, self.players[self.player_turn].side) != MoveResult.INCORRECT:
                    self.game_controller.update(move)
                    self.player_turn = (self.player_turn + 1) % 2
                    self.chess_board = Board(self.game_controller.export_to_chess_board_str())
                    self.render.set_game_state(self.chess_board, self.players[self.player_turn].set_move,
                                               None, None, None)
            self.render.step()
