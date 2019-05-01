###############################
# MODULE: Chess engine class  #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 10/04/2019     #
###############################

from enum import Enum
from ChessAI.ChessPlayer.BotPlayer.minmax_bot import MinmaxBot
from ChessAI.ChessPlayer.LocalPlayer.local_player import LocalPlayer
from ChessAI.GameController.game_controller import GameController, MoveResult
from ChessBoard.chess_board import Board
from ChessBoard.chess_figure import Side
from ChessRender.RenderFsmCommon.render_fsm import RenderFsm
from direct.task.Task import Task
from ServerComponents.Client.client import Client


class GameStates(Enum):
    OFFLINE_GAME = 0,
    ONLINE_GAME = 1

class Engine:

    def __init__(self):
        """
        Initialize Engine class function
        """
        self.render = RenderFsm()
        self.server_address = 'http://localhost:8000'

        #### - functions to process data from users
        self.render.process_login = self.process_login
        self.render.process_find_player = self.process_find_player
        self.render.process_offline_game = self.process_offline_game
        self.render.process_load_model = self.process_load_model
        self.render.change_state(self.render, "fsm:MainMenu")
        self.online_game_was_started = False

        self.rate = 0
        self.client = None
        self.game_state = None

        self.local_player = None
        self.current_move = 0
        self.players = None

        self.render.taskMgr.add(self.step, "step")
        self.render.run()

    def step(self, task):
        """
        Main loop function
        :return: NONE.
        """
        if self.game_state == GameStates.OFFLINE_GAME:
            cur_player = self.players[self.player_turn]
            move = cur_player.get_move()
            if move is not None:
                if self.game_controller.check_move(move, cur_player.side) != MoveResult.INCORRECT:
                    self.game_controller.update(move)
                    self.player_turn = (self.player_turn + 1) % 2
                self.render_update_board(self.players[self.player_turn])

        elif self.game_state == GameStates.ONLINE_GAME:
            if Side(self.current_move) == self.local_player.side:
                cur_player = self.local_player
                move = cur_player.get_move()
                if move is not None:
                    if self.game_controller.check_move(move, cur_player.side) != MoveResult.INCORRECT:
                        self.game_controller.update(move)
                        self.render.process_set_move_player = None
                        self.current_move = (self.current_move + 1) % 2
                        self.client.send_message('update_board', "p1={}&p2={}&p3={}&p4={}".format(move.point_from.x,
                                                                                              move.point_from.y,
                                                                                              move.point_to.x,
                                                                                              move.point_to.y))
                        self.render_update_board(self.local_player)
        else:
            pass

        return Task.cont


    def process_offline_game(self):
        self.player_turn = 0
        self.chess_board = Board()
        self.game_controller = GameController(self.chess_board)
        self.players = [LocalPlayer(Side.WHITE), MinmaxBot(Side.BLACK, self.game_controller)]
        self.players[0].make_move()
        self.render.process_set_move_player = self.players[0].set_move
        self.game_state = GameStates.OFFLINE_GAME

    def process_load_model(self, text_dict, side=None, figure=None):
        if side is not None and figure is not None:
            if side == "white":
                self.render.objMngr.change_skin(text_dict["Path to .png"], figure.upper())
            else:
                self.render.objMngr.change_skin(text_dict["Path to .png"], figure.lower())
        else:
            self.render.objMngr.change_board(text_dict["Path to .png"])

    def process_login(self, text_dict):
        """
        Process text from text fields (login, parol)
        :param text_dict: dictionary, where
        keys are one the string const of the form L_SOME (see. UIPrimitives.room)
        values are strings (print by user)
        """

        login = text_dict["Login"]
        password = text_dict["Password"]

        # make client
        self.client = Client(self.server_address, on_login_call=self.on_login, on_update_call=self.on_update_game)

        # make request for connection
        self.client.send_message('login', 'login={0}&password={1}'.format(login, password))

    def process_auth(self, text_dict):
        login = text_dict["Login"]
        email = text_dict["Email"]
        password = text_dict["Password"]

        # make client
        self.client = Client(self.server_address, on_login_call=self.on_login, on_update_call=self.on_update_game)

        # make request for connection
        self.client.send_message('auth', 'login={0}&email{2}=&password={3}'.format(login, email, password))

    def process_confirm_auth(self, text_dict):
        email = text_dict["Email"]
        auth_code = text_dict["Auth_code"]

        # make client
        self.client = Client(self.server_address, on_login_call=self.on_login, on_update_call=self.on_update_game)

        # make request for connection
        self.client.send_message('confirm_auth', 'email={0}&auth_code{2}'.format(email, auth_code))


    def on_login(self, text_dict):
        self.rate = int(text_dict['self_rate'])

        self.render.change_state(self.render, "fsm:Matchmaking")

    def on_update_game(self, text_dict):
        if text_dict['board'] is "":
            self.chess_board = Board()
            self.game_controller = GameController(self.chess_board)
        else:
            print("board is " + str(text_dict['board']))
            self.game_controller =  GameController(None, str(text_dict['board']))

        if text_dict['side'] == '0':
            self.local_player = LocalPlayer(Side.WHITE)
        else:
            self.local_player = LocalPlayer(Side.BLACK)
        self.current_move = int(text_dict['next_move'])

        if (self.online_game_was_started == False):
            self.game_state = GameStates.ONLINE_GAME
            self.render.change_state(self.render, "fsm:GameState")
            self.online_game_was_started = True

        self.render_update_board(self.local_player)



    def render_update_board(self, player):
        board_str = self.game_controller.export_to_chess_board_str()
        self.chess_board = Board(board_str)
        self.render.process_set_move_player = player.set_move
        self.render.cur_state.update_board(board_str)

    def process_find_player(self, text_dict):
        """
        Process text from text fields (login, parol)
        :param text_dict: dictionary, where
        keys are one the string const of the form L_SOME (see. UIPrimitives.room)
        values are strings (print by user)
        """
        print(text_dict)
        try:
            game_time = int(text_dict["MatchTime"])
            move_time = int(text_dict["AddTime"])
            min_rate = int(text_dict["MinRate"])
            max_rate = int(text_dict["MaxRate"])
        except ValueError:
            # TO DO ADD ALERT
            return

        # make request
        self.client.send_message('find_pair',
                                 'low_rate={0}&hight_rate={1}&game_time={2}&move_time={3}'
                                 .format(min_rate, max_rate, game_time, move_time))




