###############################
# MODULE: Chess engine class  #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 10/04/2019     #
###############################
import copy
import sys
import threading
from enum import Enum
from time import sleep

from ChessAI.ChessPlayer.BotPlayer.minmax_bot import MinmaxBot
from ChessAI.ChessPlayer.LocalPlayer.local_player import LocalPlayer
from ChessAI.ChessPlayer.chess_player import Player
from ChessAI.GameController.game_controller import GameController, MoveResult
from ChessBoard.chess_board import Board
from ChessBoard.chess_figure import Side
from ChessEngine.hist_movement_manager import HistMovementManager
from ChessRender.RenderFsmCommon.render_fsm import RenderFsm
from direct.task.Task import Task

from ChessSound.Sound import SoundTypes
from ServerComponents.Client.client import Client


class GameStates(Enum):
    OFFLINE_GAME = 0
    ONLINE_GAME = 1
    MENU = 2


class OfflineGameMode(Enum):
    WITH_FRIEND = 0
    WITH_COMPUTER = 1


class PlayerData:
    def __init__(self, player):
        self.time_left = player.time_left
        self.login = player.login
        self.rate = player.rate
        self.side = player.side
        self.is_stopped = player.is_stopped

    def player_init(self, player):
        player.init_time(self.time_left)
        player.login = self.login
        player.rate = self.rate
        player.side = self.side
        player.is_stopped = self.is_stopped

class MatchData:
    def __init__(self, serialized_game_controller, player_turn, white_player, black_player):
        self.serialized_game_controller = serialized_game_controller
        self.player_turn = player_turn
        self.white_player_data = PlayerData(white_player)
        self.black_player_data = PlayerData(black_player)

class Engine:

    def __init__(self):
        """
        Initialize Engine class function
        """
        self.render = RenderFsm()
        self.server_address = 'https://chessservertest.herokuapp.com'  # 'http://localhost:8000' 'https://chessservertest.herokuapp.com'

        self.render.on_application_exit = self.on_application_exit
        #### - functions to process data from users
        self.render.process_login = self.process_login
        self.render.process_registration = self.process_auth
        self.render.process_find_player = self.process_find_player
        self.render.process_offline_with_computer = self.process_offline_game
        self.render.process_offline_with_firend = self.process_offline_game_with_firend
        self.render.process_reset_save_data_friend = self.process_reset_save_data_friend
        self.render.process_reset_save_data_computer = self.process_reset_save_data_computer
        self.render.on_match_making_state = self.on_match_making_state
        self.render.get_loacal_player_rating = self.get_loacal_player_rating
        self.render.start_game_by_pairing = self.start_game_by_pairing
        self.render.get_cur_turn_side = self.get_cur_turn_side
        self.player_turn = None

        self.render.on_press_giveup_button = self.on_localplayer_giveup
        self.render.on_offline_game_exit = self.on_offline_game_exit
        self.render.process_confirm_auth = self.process_confirm_auth
        self.render.on_game_exit = self.set_menu_state
        self.render.process_skin_select = self.process_skin_select
        self.render.process_continue_online_game = self.on_continue_game
        self.render.change_state(self.render, "fsm:MainMenu")
        self.online_game_was_started = False

        self.render.get_hist_movement_manager = self.get_hist_movement_manager
        self.render.refresh_matchmaking_pairlist = self.refresh_matchmaking_pairlist

        self.offline_with_friend_match_data = None
        self.offline_with_computer_match_data = None

        self.current_offline_game_mode = None

        # maybe to replace on player?
        self.whiteside_pack_name = "pack0"
        self.blackside_pack_name = "pack0"
        self.render.whiteside_pack_name = self.whiteside_pack_name
        self.render.blackside_pack_name = self.blackside_pack_name

        self.login = ''
        self.email = ''
        self.password = ''
        self.client = None
        self.on_update_now = False
        self.game_state = GameStates.MENU
        self.delta_rate = 0

        self.render.is_client_connected_to_server = False
        self.render.is_game_played = False
        self.local_player = None
        self.online_player = None
        self.current_move = 0
        self.players = None
        self.game_result = -1
        self.game_controller = None
        self.chess_board = None
        self.offline_game_played = False
        self.server_calculation = False

        self.pack_name = 'pack0'

        self.withfriend_hist_movement_manager = HistMovementManager()
        self.computer_hist_movement_manager = HistMovementManager()
        self.online_hist_movement_manager = HistMovementManager()

        self.render.taskMgr.add(self.step, "step")
        self.render.run()

    def _make_client(self):
        # make client
        if self.client is None:
            self.client = Client(self.server_address, on_login_call=self.on_login,
                                 on_update_call=self.on_update_game,
                                 on_update_time_call=self.on_update_time,
                                 on_avail_packs_call=self.on_avail_packs,
                                 on_win_pack_call=self.process_win_pack,
                                 on_find_pairing_list_call=self.process_pairing_list,
                                 on_error_call=self.process_error)

    def step(self, task):
        """
        Main loop function
        :return: NONE.
        """

        if self.render.on_update_now or self.render.is_clearing or self.server_calculation:
            return Task.cont
        self.server_calculation = True
        self.render.on_update_now = True
        if self.game_state == GameStates.OFFLINE_GAME:
            if self.offline_game_played is None:
                self.offline_game_played = True
                self.render_update_board()
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
            if cur_player.is_time_over():
                self.game_result = self.players[(self.player_turn + 1) % 2].side
                self.delta_rate = 20
                self.offline_game_played = False
                if self.game_result == self.players[(self.player_turn + 1) % 2].side:
                    self.render.sound.play(SoundTypes.WIN)
            if move is not None:
                pawn_swaped_figure = cur_player.get_pawn_swaped_figure()
                move_res = self.game_controller.check_move(move, cur_player.side)

                if move_res != MoveResult.INCORRECT and self.game_result == -1:
                    self.game_controller.update(move, cur_player.side)

                    if pawn_swaped_figure is not None:
                        self.game_controller.swap_pawn(move.point_to, pawn_swaped_figure)
                        move_res = self.game_controller.check_board_res(cur_player.side)
                        assert (move_res != MoveResult.INCORRECT)

                    self.player_turn = (self.player_turn + 1) % 2
                    self.players[self.player_turn].restart_timer()
                    # game over
                    if move_res == MoveResult.MATE:
                        self.game_result = cur_player.side
                        self.delta_rate = 20
                        self.offline_game_played = False
                        if self.game_result == self.players[(self.player_turn + 1) % 2].side:
                            self.render.sound.play(SoundTypes.WIN)
                    elif move_res == MoveResult.STALEMATE:
                        self.game_result = None
                        self.delta_rate = 0
                        self.offline_game_played = False
                    elif self.current_offline_game_mode is OfflineGameMode.WITH_FRIEND:
                        self.render.cur_state.side = self.players[self.player_turn].side
                        self.render.cur_state.middle_click(steps=30)
                    # play music
                    self.render.sound.play(SoundTypes.MOVE)

                self.render.process_set_move_player = self.players[self.player_turn].set_move
            if move is not None or self.game_result != -1:
                self.render_update_board()

            if self.game_result != -1:
                self.render.cur_state.update_game_result_info(self.game_result, self.delta_rate)
                self.players[0].stop_timer()
                self.players[1].stop_timer()

        elif self.game_state == GameStates.ONLINE_GAME:
            if self.online_game_was_started is None:
                self.render.cur_state.update_camera(self.local_player.side)
                self.online_game_was_started = True
                self.render_update_board()

            if Side(self.current_move) == self.local_player.side:
                self.local_player.update_time()
            else:
                self.online_player.update_time()

            move = self.local_player.get_move()
            if move is not None:
                if Side(self.current_move) == self.local_player.side:
                    pawn_swaped_figure = self.local_player.get_pawn_swaped_figure()
                    self.local_player.update_time()
                    if self.game_controller.check_move(move, self.local_player.side) != MoveResult.INCORRECT:
                        self.game_controller.update(move, self.local_player.side)

                        data_str = "p1={}&p2={}&p3={}&p4={}&swapped_figure=" \
                            .format(move.point_from.x,
                                    move.point_from.y,
                                    move.point_to.x,
                                    move.point_to.y)
                        if pawn_swaped_figure is not None:
                            self.game_controller.swap_pawn(move.point_to, pawn_swaped_figure)
                            move_res = self.game_controller.check_board_res(self.local_player.side)
                            assert (move_res != MoveResult.INCORRECT)
                            data_str += str(pawn_swaped_figure)

                        self.client.send_message('update_board', data_str)
                        self.online_player.restart_timer()
                        # play music
                        self.render.sound.play(SoundTypes.MOVE)
                self.render.process_set_move_player = self.local_player.set_move
                self.render_update_board()

            if self.game_result != -1:
                self.render.cur_state.update_game_result_info(self.game_result, self.delta_rate)
                self.local_player.stop_timer()
                self.online_player.stop_timer()
            else:
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
        self.server_calculation = False
        return Task.cont

    def get_cur_turn_side(self):
        if self.game_state is GameStates.ONLINE_GAME:
            player_turn = self.current_move
        else:
            player_turn = self.player_turn
        if player_turn is None:
            return None
        return Side(player_turn)

    def set_menu_state(self):
        self.game_state = GameStates.MENU

    def process_skin_select(self, pack_name):
        self.pack_name = copy.deepcopy(pack_name)
        if self.render.is_client_connected_to_server:
            # make request for skin update
            self.client.send_message('update_pack', 'pack_name={0}'.format(self.pack_name))

    def process_offline_game(self):

        if self.offline_with_computer_match_data is None:
            self.player_turn = 0
            self.chess_board = Board()
            self.game_controller = GameController(self.chess_board)
            self.players = [LocalPlayer(Side.WHITE), MinmaxBot(Side.BLACK, self.game_controller)]
            self.players[0].update_login('Your')
            self.players[0].update_rate(1200)
            self.players[0].make_move()

            self.players[1].update_login('Computer')
            self.players[1].update_rate(1800)

            for i in range(0, len(self.players)):
                self.players[i].init_time(1000 * 60 * 5)  # 5 minutes
        else:
            self.player_turn = self.offline_with_computer_match_data.player_turn
            self.game_controller = GameController(None, self.offline_with_computer_match_data.serialized_game_controller)
            self.players = [LocalPlayer(Side.WHITE), MinmaxBot(Side.BLACK, self.game_controller)]
            self.offline_with_computer_match_data.white_player_data.player_init(self.players[0])
            self.offline_with_computer_match_data.black_player_data.player_init(self.players[1])

        self.render.side = Side.WHITE
        self.render.process_set_move_player = self.players[self.player_turn].set_move
        self.game_result = -1
        self.delta_rate = 0

        self.offline_game_played = None
        self.current_offline_game_mode = OfflineGameMode.WITH_COMPUTER

        self.game_state = GameStates.OFFLINE_GAME

        self.render.whiteside_pack_name = self.pack_name
        self.render.check_move_func_for_pawn_swap = self.game_controller.check_move

    def process_offline_game_with_firend(self):
        self.players = [LocalPlayer(Side.WHITE), LocalPlayer(Side.BLACK)]

        if self.offline_with_friend_match_data is None:
            self.player_turn = 0
            self.chess_board = Board()
            self.game_controller = GameController(self.chess_board)
            self.players[0].update_login('1st')
            self.players[0].update_rate(1200)
            self.players[0].make_move()

            self.players[1].update_login('2nd')
            self.players[1].update_rate(1200)
            for i in range(0, len(self.players)):
                self.players[i].init_time(1000 * 60 * 5)  # 5 minutes
        else:
            self.player_turn = self.offline_with_friend_match_data.player_turn
            self.game_controller = GameController(None, self.offline_with_friend_match_data.serialized_game_controller)
            self.offline_with_friend_match_data.white_player_data.player_init(self.players[0])
            self.offline_with_friend_match_data.black_player_data.player_init(self.players[1])

        self.render.side = Side.WHITE
        self.render.process_set_move_player = self.players[self.player_turn].set_move
        self.game_result = -1
        self.delta_rate = 0

        self.offline_game_played = None
        self.current_offline_game_mode = OfflineGameMode.WITH_FRIEND

        self.game_state = GameStates.OFFLINE_GAME

        self.render.whiteside_pack_name = self.pack_name
        self.render.check_move_func_for_pawn_swap = self.game_controller.check_move

    def on_offline_game_exit(self):
        if self.game_result == -1:
            board = self.game_controller.serialize_to_str()
            if self.current_offline_game_mode is OfflineGameMode.WITH_FRIEND:
                self.offline_with_friend_match_data = MatchData(board, self.player_turn, self.players[0], self.players[1])
            if self.current_offline_game_mode is OfflineGameMode.WITH_COMPUTER:
                self.offline_with_computer_match_data = MatchData(board, self.player_turn, self.players[0], self.players[1])
        else:
            if self.current_offline_game_mode is OfflineGameMode.WITH_FRIEND:
                self.offline_with_friend_match_data = None
                self.withfriend_hist_movement_manager.clear()
            if self.current_offline_game_mode is OfflineGameMode.WITH_COMPUTER:
                self.offline_with_computer_match_data = None
                self.computer_hist_movement_manager.clear()
        self.game_state = GameStates.MENU
        self.offline_game_played = None
        self.players[0].stop_timer()
        self.players[1].stop_timer()
        self.players = None


    def process_reset_save_data_friend(self):
        self.withfriend_hist_movement_manager.clear()
        self.offline_with_friend_match_data = None

    def process_reset_save_data_computer(self):
        self.computer_hist_movement_manager.clear()
        self.offline_with_computer_match_data = None

    def process_login(self, text_dict):
        while self.server_calculation:
            sleep(5.0 / 1000.0)
        self.server_calculation = True
        """
        Process text from text fields (login, parol)
        :param text_dict: dictionary, where
        keys are one the string const of the form L_SOME (see. UIPrimitives.room)
        values are strings (print by user)
        """
        self.login_process_thead = threading.Thread(target=self.login_process_theading,
                                                    args=(text_dict,))
        self.login_process_thead.start()

    def login_process_theading(self, text_dict):
        print("a")
        login = text_dict["Login"]
        password = text_dict["Password"]

        self.login = str(login)
        self.password = str(password)

        self.online_game_was_started = False

        # make client
        self._make_client()

        # make request for connection
        self.client.send_message('login', 'login={0}&password={1}'.format(login, password))

        self.server_calculation = False

    def process_auth(self, text_dict):
        login = text_dict["Login"]
        email = text_dict["Email"]
        password = text_dict["Password"]

        # save params
        self.email = email
        self.login = login
        self.password = password

        # make client
        self._make_client()
        # make request for connection
        self.client.send_message('auth', 'login={0}&email={1}=&password={2}'.format(login, email, password))
        # go to confirm menu
        self.render.login = login
        self.render.email = email
        self.render.change_state(self.render, "fsm:AuthConfirm")

    def process_confirm_auth(self, text_dict):
        email = text_dict["Email"]
        auth_code = text_dict["AuthCode"]

        # make client
        self._make_client()
        # make request for connection
        self.client.send_message('confirm_auth', 'email={0}&auth_code={1}'.format(email, auth_code))
        sleep(0.5)
        # make request for connection
        self.client.send_message('login', 'login={0}&password={1}'.format(self.login, self.password))
        self.render.change_state(self.render, "fsm:MainMenu")

    def on_login(self, text_dict):
        while self.server_calculation:
            sleep(5.0 / 1000.0)
        self.server_calculation = True

        if self.render.cur_state_key == "fsm:GameState":
            return
        if 'not_verified' in text_dict:
            self.render.change_state(self.render, "fsm:AuthConfirm")
        else:
            self.rate = int(text_dict['self_rate'])
            self.render.is_client_connected_to_server = True
            self.render.change_state(self.render, "fsm:MainMenu")
        self.server_calculation = False

    def on_continue_game(self):
        if self.online_game_was_started is False:
            self.render.change_state(self.render, "fsm:Matchmaking1Step")
            return
        self.render.change_state(self.render, "fsm:GameState")
        self.render.cur_state.update_camera(self.local_player.side)
        self.render.process_set_move_player = self.local_player.set_move
        self.render_update_board()
        self.game_state = GameStates.ONLINE_GAME

    def on_update_game(self, text_dict):
        while self.server_calculation:
            sleep(5.0 / 1000.0)
        self.server_calculation = True
        self.game_state = GameStates.MENU
        self.game_result = -1
        self.delta_rate = 0

        self.current_move = int(text_dict['next_move'])

        if text_dict['board'] is None:
            self.chess_board = Board()
            self.game_controller = GameController(self.chess_board)
        else:
            print("board is " + str(text_dict['board']))
            # play music
            self.render.sound.play(SoundTypes.MOVE)
            self.game_controller = GameController(None, str(text_dict['board']))

        if text_dict['side'] == '0':
            self.local_player = LocalPlayer(Side.WHITE)
            self.online_player = Player(Side.BLACK)
            self.render.whiteside_pack_name = text_dict['self_pack']
            self.render.blackside_pack_name = text_dict['opponent_pack']
            self.render.side = Side.BLACK  # watch opponent
        else:
            self.local_player = LocalPlayer(Side.BLACK)
            self.online_player = Player(Side.WHITE)
            self.render.whiteside_pack_name = text_dict['opponent_pack']
            self.render.blackside_pack_name = text_dict['self_pack']
            self.render.side = Side.WHITE  # watch opponent

        self.render.process_set_move_player = self.local_player.set_move
        self.render.check_move_func_for_pawn_swap = self.game_controller.check_move
        if self.online_game_was_started is False:
            self.online_game_was_started = True
            self.render.is_game_played = True
            self.render.change_state(self.render, "fsm:GameState")
            self.render.cur_state.update_camera(self.local_player.side)

        self.render.cur_state.check_move_func = self.game_controller.check_move

        if int(text_dict['is_playing']) == 0:
            self.online_game_was_started = False
            self.render.is_game_played = False
            if text_dict['result'] is None:
                self.game_result = None
            else:
                self.game_result = Side(int(text_dict['result']))
                if self.game_result == self.local_player.side:
                    self.render.sound.play(SoundTypes.WIN)
            self.delta_rate = self.rate - int(text_dict['self_rate'])
            self.rate = int(text_dict['self_rate'])

        self.local_player.update_login(self.login)
        self.local_player.update_rate(self.rate)
        self.local_player.init_time_from_str(text_dict['self_time'])

        self.online_player.update_login(text_dict['opponent_login'])
        self.online_player.update_rate(text_dict['opponent_rate'])

        self.online_player.init_time_from_str(text_dict['opponent_time'])

        self.render_update_board()
        self.game_state = GameStates.ONLINE_GAME
        self.server_calculation = False

    def on_update_time(self, text_dict):
        if self.game_state != GameStates.ONLINE_GAME:
            return

        if int(text_dict['is_playing']) == 0:
            self.online_game_was_started = False
            self.render.is_game_played = False
            if text_dict['result'] is None:
                self.game_result = None
            else:
                self.game_result = Side(int(text_dict['result']))
                if self.game_result == self.local_player.side:
                    self.render.sound.play(SoundTypes.WIN)
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

        if self.game_result == GameStates.ONLINE_GAME:
            self.online_hist_movement_manager.make_screen(board_str)
        else:
            if self.current_offline_game_mode == OfflineGameMode.WITH_FRIEND:
                self.withfriend_hist_movement_manager.make_screen(board_str)
            else:
                self.computer_hist_movement_manager.make_screen(board_str)

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

    def process_pairing_list(self, text_dict):
        # here add buttons with ids
        if 'pairing_list' not in text_dict or text_dict['pairing_list'] is None:
            pairings = []
        else:
            pairings_texts = str(text_dict['pairing_list']).split(';')
            pairings = []
            for p in pairings_texts:
                if p != '':
                    pairings.append(str(p).split(','))

        self.render.set_pairing_list(pairings)

    def start_game_by_pairing(self, pairing_id):
        # make client
        self._make_client()
        # make request for connection
        self.client.send_message('start_game_by_pairing', 'pairing_id={0}'.format(pairing_id))

    def on_match_making_state(self):
        # make client
        self._make_client()
        # make request for connection
        self.client.send_message('find_pair_list', '')

    def process_error(self, text_dict):
        self.render.message = text_dict['message']
        self.render.change_state(self.render, "fsm:Message")

    def process_win_pack(self, pack_data):
        while self.server_calculation:
            sleep(5.0 / 1000.0)
        self.server_calculation = True
        self.game_state = GameStates.MENU
        if pack_data['new_pack'] not in self.render.avail_packs:
            self.render.avail_packs.append(pack_data['new_pack'])
            self.render.avail_packs.sort()
        self.render.win_pack = pack_data['new_pack']
        self.render.change_state(self.render, "fsm:WinPack")
        self.server_calculation = False

    def on_application_exit(self):
        if self.client is not None:
            self.client.disconnect()
        sys.exit()

    def get_loacal_player_rating(self):
        return self.rate

    def on_localplayer_giveup(self):
        if self.game_state == GameStates.OFFLINE_GAME:
            self.game_result = 0
            self.on_offline_game_exit()
            self.render.go_to_prev_state()
        if self.game_state == GameStates.ONLINE_GAME:
            # make client
            self._make_client()
            # make request for connection
            print('Send surrender message')
            self.client.send_message('surrender', '')

    def get_hist_movement_manager(self):
        if self.game_result == GameStates.ONLINE_GAME:
            return self.online_hist_movement_manager
        else:
            if self.current_offline_game_mode == OfflineGameMode.WITH_FRIEND:
                return self.withfriend_hist_movement_manager
            else:
                return self.computer_hist_movement_manager

    def refresh_matchmaking_pairlist(self):
        self.on_match_making_state()
