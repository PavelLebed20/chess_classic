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
from ServerComponents.Client.client import Client

class GameStates(Enum):
    OFFLINE_GAME = 0,
    ONLINE_GAME = 1

class Engine:

    def __init__(self):
        """
        Initialize Engine class function
        """
        self.render = Render()
        #### - functions to process data from users
        self.render.room.process_login = self.process_login
        self.render.room.process_find_player = self.process_find_player
        self.render.process_offline_game = self.process_offline_game
        #self.render.room.process_update_game = self.process_update_game

        self.rate = 0
        self.client = None
        self.game_state = GameStates.OFFLINE_GAME

        self.local_player = None
        self.current_move = 0
        self.players = None

        #### - init main menu
        render_obtain_funcs.main_menu(self.render)

    def run(self):
        """
        Main loop function
        :return: NONE.
        """
        while True:

            if self.render.state == RenderState.GAME:
                if self.game_state == GameStates.OFFLINE_GAME:
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
                else:
                    if self.current_move == int(self.local_player.side):
                        cur_player = self.local_player
                        move = cur_player.get_move()
                        if move is not None:
                            if self.game_controller.check_move(move, cur_player.side) != MoveResult.INCORRECT:
                                self.game_controller.update(move)
                                self.current_move = (self.current_move + 1) % 2
                            board_str = self.game_controller.export_to_chess_board_str()
                            self.chess_board = Board(board_str)
                            self.render.set_game_state(board_str, self.local_player.set_move,
                                                       None, None, None)
                            self.client.send_message('update_board', "p1={}&p2={}&p3={}&p4={}".format(move.point_from.x, move.point_from.y, move.point_to.x, move.point_to.y))

            if self.render.state == RenderState.MENU:
                self.render.set_menu_state(buttons=self.render.room.buttons_prim,
                                           text_fields=self.render.room.text_fields_prim)

            self.render.step()

    def process_offline_game(self):
        self.player_turn = 0
        self.chess_board = Board()
        self.game_controller = GameController(self.chess_board)
        self.players = [LocalPlayer(Side.WHITE), MinmaxBot(Side.BLACK, self.game_controller)]
        self.players[0].make_move()
        render_obtain_funcs.game_fun(self.render)

    def process_login(self, text_dict):
        """
        Process text from text fields (login, parol)
        :param text_dict: dictionary, where
        keys are one the string const of the form L_SOME (see. UIPrimitives.room)
        values are strings (print by user)
        """
        login = text_dict[ChessRender.UIPrimitives.room.L_LOGIN]
        password = text_dict[ChessRender.UIPrimitives.room.L_PAROL]

        # make client
        self.client = Client('http://localhost:8000', on_login_call=self.on_login, on_update_call=self.on_update_game)

        # make request for connection
        self.client.send_message('login', 'login={0}&password={1}'.format(login, password))

    def on_login(self, text_dict):
        self.game_state = GameStates.ONLINE_GAME

        self.rate = int(text_dict['self_rate'])

        render_obtain_funcs.find_player_fun(self.render)

    def on_update_game(self, text_dict):
        if text_dict['board'] == "":
            self.chess_board = Board()
            self.game_controller = GameController(self.chess_board)
            if text_dict['side'] == '0':
                self.local_player = LocalPlayer(Side.WHITE)
            else:
                self.local_player = LocalPlayer(Side.BLACK)
            self.current_move = int(text_dict['next_move'])
        else:
            self.game_controller = text_dict['board']
            self.current_move = text_dict['next_move']

    def process_find_player(self, text_dict):
        """
        Process text from text fields (login, parol)
        :param text_dict: dictionary, where
        keys are one the string const of the form L_SOME (see. UIPrimitives.room)
        values are strings (print by user)
        """
        print(text_dict)
        try:
            game_time = int(text_dict[ChessRender.UIPrimitives.room.L_GAME_TIME])
            move_time = int(text_dict[ChessRender.UIPrimitives.room.L_MOVE_TIME])
            min_rate = int(text_dict[ChessRender.UIPrimitives.room.L_MIN_RATE])
            max_rate = int(text_dict[ChessRender.UIPrimitives.room.L_MAX_RATE])
        except ValueError:
            # TO DO ADD ALERT
            return

        # make request
        self.client.send_message('find_pair',
                                 'low_rate={0}&hight_rate={1}&game_time={2}&move_time={3}'
                                 .format(min_rate, max_rate, game_time, move_time))

        # justchill render_obtain_funcs.game_online_fun(self.render)


