###############################
# MODULE: Chess engine class  #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 10/04/2019     #
###############################
import copy
from enum import Enum
from time import sleep

from ChessAI.ChessPlayer.BotPlayer.minmax_bot import MinmaxBot
from ChessAI.ChessPlayer.LocalPlayer.local_player import LocalPlayer
from ChessAI.ChessPlayer.chess_player import Player
from ChessAI.GameController.game_controller import GameController, MoveResult
from ChessBoard.chess_board import Board
from ChessBoard.chess_figure import Side
from ChessRender.RenderFsmCommon.render_fsm import RenderFsm
from direct.task.Task import Task

from ChessSound.Sound import SoundTypes
from ServerComponents.Client.client import Client


class GameStates(Enum):
    OFFLINE_GAME = 0,
    ONLINE_GAME = 1,
    MENU = 2

class Engine:

    def __init__(self):
        """
        Initialize Engine class function
        """
        self.render = RenderFsm()
        self.server_address = 'http://localhost:8000'

        #### - functions to process data from users
        self.render.process_login = self.process_login
        self.render.process_registration = self.process_auth
        self.render.process_find_player = self.process_find_player
        self.render.process_offline_game = self.process_offline_game
        self.render.process_load_model = self.process_load_model
        self.render.process_confirm_auth = self.process_confirm_auth
        self.render.on_game_exit = self.set_menu_state
        self.render.process_skin_select = self.process_skin_select
        self.render.change_state(self.render, "fsm:MainMenu")
        self.online_game_was_started = False

        # maybe to replace on player?
        self.whiteside_pack_name = "pack0"
        self.blackside_pack_name = "pack0"
        self.render.whiteside_pack_name = self.whiteside_pack_name
        self.render.blackside_pack_name = self.blackside_pack_name

        self.rate = 0
        self.login = ''
        self.client = None
        self.on_update_now = False
        self.game_state = GameStates.MENU
        self.delta_rate = 0

        self.connected = False
        self.local_player = None
        self.online_player = None
        self.current_move = 0
        self.players = None
        self.game_result = -1
        self.game_controller = None
        self.chess_board = None

        self.pack_name = 'pack0'

        self.render.taskMgr.add(self.step, "step")
        self.render.run()

    def _make_client(self):
        # make client
        if self.client is None:
            self.client = Client(self.server_address, on_login_call=self.on_login,
                                 on_update_call=self.on_update_game,
                                 on_update_time_call=self.on_update_time,
                                 on_avail_packs_call=self.on_avail_packs)

    def step(self, task):
        """
        Main loop function
        :return: NONE.
        """
        if self.render.on_update_now or self.render.is_clearing:
            return Task.cont
        self.render.on_update_now = True
        if self.game_state == GameStates.OFFLINE_GAME:
            cur_player = self.players[self.player_turn]
            # obtain time
            cur_player.update_time()
            self.render.cur_state.update_game_info(self.players[0].login,
                                                   self.players[0].time_str(),
                                                   self.players[0].rate,
                                                   self.players[1].login,
                                                   self.players[1].time_str(),
                                                   self.players[1].rate)

            move = cur_player.get_move()
            other_move = self.players[(self.player_turn + 1) % 2].get_move()
            if cur_player.is_time_over():
                self.game_result = self.players[(self.player_turn + 1) % 2].side
                self.delta_rate = 20
            if move is not None:
                move_res = self.game_controller.check_move(move, cur_player.side)

                if move_res != MoveResult.INCORRECT and self.game_result == -1:
                    self.game_controller.update(move)
                    self.player_turn = (self.player_turn + 1) % 2
                    self.players[self.player_turn].restart_timer()
                    # game over
                    if move_res == MoveResult.MATE:
                        self.game_result = cur_player.side
                        self.delta_rate = 20
                    elif move_res == MoveResult.STALEMATE:
                        self.game_result = None
                        self.delta_rate = 0
                    # play music
                    self.render.sound.play(SoundTypes.MOVE)

                self.render.process_set_move_player = self.players[self.player_turn].set_move
            if move is not None or other_move is not None or self.game_result != -1:
                self.render_update_board()

            if self.game_result != -1:
                self.render.cur_state.update_game_result_info(self.game_result, self.delta_rate)
                self.players[0].stop_timer()
                self.players[1].stop_timer()

        elif self.game_state == GameStates.ONLINE_GAME:
            if Side(self.current_move) == self.local_player.side:
                self.local_player.update_time()
            else:
                self.online_player.update_time()

            move = self.local_player.get_move()
            if move is not None:
                if Side(self.current_move) == self.local_player.side:
                    self.local_player.update_time()
                    if self.game_controller.check_move(move, self.local_player.side) != MoveResult.INCORRECT:
                        self.game_controller.update(move)
                        self.current_move = (int(self.current_move) + 1) % 2
                        self.client.send_message('update_board', "p1={}&p2={}&p3={}&p4={}"
                                                 .format(move.point_from.x,
                                                         move.point_from.y,
                                                         move.point_to.x,
                                                         move.point_to.y))
                        self.online_player.restart_timer()
                        # play music
                        self.render.sound.play(SoundTypes.MOVE)
                self.render.process_set_move_player = self.local_player.set_move
            self.render_update_board()

            if self.game_result != -1:
                self.render.cur_state.update_game_result_info(self.game_result, self.delta_rate)
                self.local_player.stop_timer()
                self.online_player.stop_timer()

            # set text info
            white_login = self.local_player.login
            white_time = self.local_player.time_str()
            white_rate = self.local_player.rate
            black_login = self.online_player.login
            black_time = self.online_player.time_str()
            black_rate = self.online_player.rate
            if self.local_player.side is Side.BLACK:
                white_login, black_login = black_login, white_login
                white_time, black_time = black_time, white_time
                white_rate, black_rate = black_rate, white_rate
            self.render.cur_state.update_game_info(white_login, white_time, white_rate,
                                                   black_login, black_time, black_rate)
        else:
            pass

        self.render.on_update_now = False
        return Task.cont

    def set_menu_state(self):
        self.game_state = GameStates.MENU

    def process_skin_select(self, pack_name):
        self.pack_name = copy.deepcopy(pack_name)

    def process_offline_game(self):
        self.player_turn = 0
        self.chess_board = Board()
        self.game_controller = GameController(self.chess_board)
        self.players = [LocalPlayer(Side.WHITE), MinmaxBot(Side.BLACK, self.game_controller)]
        self.players[0].update_login('Your')
        self.players[0].update_rate(1200)
        self.players[0].make_move()

        self.players[1].update_login('Computer')
        self.players[1].update_rate(1800)

        self.render.process_set_move_player = self.players[0].set_move
        self.game_result = -1
        self.delta_rate = 0

        for i in range(0, len(self.players)):
            self.players[i].init_time(1000 * 60 * 5)  # 5 minutes

        self.game_state = GameStates.OFFLINE_GAME

        self.render.whiteside_pack_name = self.pack_name

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

        self.login = str(login)

        self.online_game_was_started = False

        # make client
        self.connected = True
        self._make_client()

        # make request for connection
        self.client.send_message('login', 'login={0}&password={1}'.format(login, password))

    def process_auth(self, text_dict):
        login = text_dict["Login"]
        email = text_dict["Email"]
        password = text_dict["Password"]

        # make client
        self._make_client()
        # make request for connection
        self.client.send_message('auth', 'login={0}&email={1}=&password={2}'.format(login, email, password))

    def process_confirm_auth(self, text_dict):
        email = text_dict["Email"]
        auth_code = text_dict["AuthCode"]

        # make client
        self._make_client()
        # make request for connection
        self.client.send_message('confirm_auth', 'email={0}&auth_code={1}'.format(email, auth_code))

    def on_login(self, text_dict):
        if self.render.cur_state_key == "fsm:GameState":
            return
        if 'not_verified' in text_dict:
            self.render.change_state(self.render, "fsm:AuthConfirm")
        else:
            self.rate = int(text_dict['self_rate'])
            self.render.change_state(self.render, "fsm:Matchmaking")

    def on_update_game(self, text_dict):
        self.game_state = GameStates.MENU
        self.game_result = -1
        self.delta_rate = 0

        if text_dict['board'] is "":
            self.chess_board = Board()
            self.game_controller = GameController(self.chess_board)
        else:
            print("board is " + str(text_dict['board']))
            if text_dict['board'] != self.game_controller.serialize_to_str():
                # play music
                self.render.sound.play(SoundTypes.MOVE)
                self.game_controller = GameController(None, str(text_dict['board']))

        if text_dict['side'] == '0':
            self.local_player = LocalPlayer(Side.WHITE)
            self.online_player = Player(Side.BLACK)
            self.render.whiteside_pack_name = text_dict['self_pack']
            self.render.blackside_pack_name = text_dict['opponent_pack']
        else:
            self.local_player = LocalPlayer(Side.BLACK)
            self.online_player = Player(Side.WHITE)
            self.render.whiteside_pack_name = text_dict['opponent_pack']
            self.render.blackside_pack_name = text_dict['self_pack']

        if int(text_dict['is_playing']) == 0:
            if text_dict['result'] is None:
                self.game_result = None
            else:
                self.game_result = Side(int(text_dict['result']))
            self.delta_rate = self.rate - int(text_dict['self_rate'])
            self.rate = int(text_dict['self_rate'])

        self.local_player.update_login(self.login)
        self.local_player.update_rate(self.rate)
        self.local_player.init_time_from_str(text_dict['self_time'])

        self.online_player.update_login(text_dict['opponent_login'])
        self.online_player.update_rate(text_dict['opponent_rate'])

        self.current_move = int(text_dict['next_move'])
        self.online_player.init_time_from_str(text_dict['opponent_time'])

        if self.online_game_was_started is False:
            self.online_game_was_started = True
            self.render.change_state(self.render, "fsm:GameState")
            self.render.cur_state.update_camera(self.local_player.side)

        self.render.process_set_move_player = self.local_player.set_move
        self.render_update_board()
        self.game_state = GameStates.ONLINE_GAME

    def on_update_time(self, text_dict):
        if self.game_state != GameStates.ONLINE_GAME:
            return

        if int(text_dict['is_playing']) == 0:
            if text_dict['result'] is None:
                self.game_result = None
            else:
                self.game_result = Side(int(text_dict['result']))
            self.delta_rate = self.rate - int(text_dict['self_rate'])
            self.rate = int(text_dict['self_rate'])

        self.local_player.update_login(self.login)
        self.local_player.update_rate(self.rate)
        self.local_player.init_time_from_str(text_dict['self_time'])

        self.online_player.update_rate(text_dict['opponent_rate'])
        self.online_player.init_time_from_str(text_dict['opponent_time'])

    def on_avail_packs(self, packs):
        self.render.avail_packs = str(packs).split(',')

    def render_update_board(self):
        board_str = self.game_controller.export_to_chess_board_str()
        self.chess_board = Board(board_str)
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

        self.online_game_was_started = False

        # make request for skin update
        self.client.send_message('update_pack', 'pack_name={0}'.format(self.pack_name))

        # make request
        self.client.send_message('find_pair',
                                 'low_rate={0}&hight_rate={1}&game_time={2}&move_time={3}'
                                 .format(min_rate, max_rate, game_time, move_time))




