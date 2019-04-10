###############################
# MODULE: Chess engine class  #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 10/04/2019     #
###############################

from enum import Enum
import ChessRender.obtain_functions as render_obtain_funcs
import ChessRender.UIPrimitives.room
from ChessAI.ChessPlayer.BotPlayer.minmax_bot import MinmaxBot
from ChessAI.ChessPlayer.LocalPlayer.local_player import LocalPlayer
from ChessAI.GameController.game_controller import GameController, MoveResult
from ChessBoard.chess_board import Board
from ChessBoard.chess_figure import Side
from ChessRender.chess_render import Render
from ChessRender.chess_render import RenderState

class Engine:

    def __init__(self):
        """
        Initialize Engine class function
        """
        self.render = Render()
        #### - functions to process data from users
        self.render.room.process_login = self.process_login
        self.render.room.process_find_player = self.process_find_player

        self.player_turn = 0
        self.chess_board = Board()
        self.game_controller = GameController(self.chess_board)
        self.players = [LocalPlayer(Side.WHITE), MinmaxBot(Side.BLACK, self.game_controller)]
        self.players[0].make_move()

        #### - init main menu
        render_obtain_funcs.main_menu(self.render)

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
                self.render.set_menu_state(buttons=self.render.room.buttons_prim,
                                           text_fields=self.render.room.text_fields_prim)

            self.render.step()

    def process_login(self, text_dict):
        """
        Process text from text fields (login, parol)
        :param text_dict: dictionary, where
        keys are one the string const of the form L_SOME (see. UIPrimitives.room)
        values are strings (print by user)
        """
        login = text_dict[ChessRender.L_LOGIN]
        password = text_dict[ChessRender.L_PAROL]

        # make request for connection

    def process_find_player(self, text_dict):
        """
        Process text from text fields (login, parol)
        :param text_dict: dictionary, where
        keys are one the string const of the form L_SOME (see. UIPrimitives.room)
        values are strings (print by user)
        """
        print(text_dict)
        try:
            game_time = text_dict[ChessRender.L_GAME_TIME]
            move_time = int(text_dict[ChessRender.L_MOVE_TIME])
            min_rate = int(text_dict[ChessRender.L_MIN_RATE])
            max_rate = int(text_dict[ChessRender.L_MAX_RATE])
        except ValueError:
            # TO DO ADD ALERT
            return

        # make request


