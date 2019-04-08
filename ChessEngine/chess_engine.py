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
from ChessRender.chess_render import RenderState
import ChessRender.obtain_functions as of

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

            if self.render.state == RenderState.GAME:

                if self.render.need_init:
                    # set current state
                    self.render.set_game_state(Board.DEFAULT_BOARD_POSITION,
                                               self.players[self.player_turn].set_move, None, None, None)

                cur_player = self.players[self.player_turn]
                move = cur_player.get_move()
                if move is not None:
                    if self.game_controller.check_move(move, cur_player.side) != MoveResult.INCORRECT:
                        self.game_controller.update(move)
                        self.player_turn = (self.player_turn + 1) % 2
                    board_str = self.game_controller.export_to_chess_board_str()
                    self.chess_board = Board(board_str)
                    self.render.set_game_state(board_str, self.players[self.player_turn].set_move,
                                           None, None, None)

            if self.render.state == RenderState.MENU:
                self.render.set_menu_state(buttons=of.buttons_arr, text_fields=of.text_fields_arr)

            self.render.step()
