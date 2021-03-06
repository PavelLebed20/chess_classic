import sys
from time import sleep

from direct.showbase.ShowBase import ShowBase, WindowProperties
from direct.task import Task

from ChessBoard.chess_figure import Side
from ChessRender.RenderFsmCommon.Camera.camera3d import CameraMenu
from ChessRender.RenderFsmCommon.RenderFsmStates.auth_confirm_state import FsmStateAuthConfirm
from ChessRender.RenderFsmCommon.RenderFsmStates.game_render_state import FsmStateGameState
from ChessRender.RenderFsmCommon.RenderFsmStates.login_render_state import FsmStateLogin
from ChessRender.RenderFsmCommon.RenderFsmStates.main_menu_render_state import FsmStateMainMenu
from ChessRender.RenderFsmCommon.RenderFsmStates.match_making_first_step_render_state import \
    FsmStateMatchmakingFirstStep
from ChessRender.RenderFsmCommon.RenderFsmStates.match_making_state import FsmStateMatchmaking
from ChessRender.RenderFsmCommon.RenderFsmStates.multiplayer_menu_render_state import FsmStateMultiplayer
from ChessRender.RenderFsmCommon.RenderFsmStates.registration_render_state import FsmStateRegistration
from ChessRender.RenderFsmCommon.RenderFsmStates.single_player_lobby import FsmStateSinglePlayerLobby
from ChessRender.RenderFsmCommon.RenderFsmStates.skin_select_render_state import FsmStateSkinSelect
from ChessRender.RenderFsmCommon.RenderFsmStates.win_pack_render_state import FsmStateWinPack
from ChessRender.RenderFsmCommon.RenderFsmStates.window_settings_render_state import FsmStateWindowSettings, \
    DEFAULT16x9SCREEN_W, DEFAULT16x9SCREEN_H

from ChessRender.RenderFsmCommon.RenderFsmStates.message_render_state import FsmStateMessage
from ChessSound.Sound import Sound, SoundTypes


class RenderFsm(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.cur_window_width = DEFAULT16x9SCREEN_W
        self.cur_window_height = DEFAULT16x9SCREEN_H

        props = WindowProperties()
        props.clearSize()
        props.setTitle('Chess Classic')
        props.setSize(self.cur_window_width, self.cur_window_height)
        #props.setFixedSize(True)
        self.win.requestProperties(props)

        self.taskMgr.add(self.mouse_task, 'mouseTask')
        self.accept("mouse1", self.mouse_press)
        self.accept("mouse1-up", self.mouse_release)
        self.accept("escape", sys.exit)

        self.cur_state = None

        # user data obtain fucntins
        self.process_login = None
        self.process_find_player = None
        self.process_registration = None
        self.process_skin_select = None
        self.process_confirm_auth = None
        self.process_continue_online_game = None

        self.process_offline_with_firend = None
        self.process_offline_with_computer = None
        self.process_reset_save_data_friend = None
        self.process_reset_save_data_computer = None
        self.on_offline_game_exit = None
        self.process_set_move_player = None

        self.on_application_exit = None

        self.on_press_giveup_button = None
        self.get_hist_movement_manager = None

        self.get_cur_turn_side = None

        self.whiteside_pack_name = None
        self.blackside_pack_name = None

        self.is_client_connected_to_server = False
        self.is_game_played = False

        self.on_update_now = False
        self.is_clearing = False
        self.state_priority = -1
        self.cur_state_key = ""
        self.on_game_exit = None
        self.side = Side.WHITE

        self.login = ''
        self.email = ''

        self.avail_packs = ['pack0']

        # sound
        self.sound = Sound(self)

        # play default
        self.sound.turn(SoundTypes.MAIN, False)
        self.sound.turn(SoundTypes.WIN, False)

        self.check_move_func_for_pawn_swap = None

        self.win_pack = None

        self.prev_render_not_message_state_key = None

        self.message = None

        self.get_loacal_player_rating = None

        self.init_sky_sphere()
        self.camera_m = CameraMenu(base.camera, base.camLens)
        self.taskMgr.add(self.camera_m.update_on_task_rotate, 'camRotTask')
        self.on_match_making_state = None
        self.start_game_by_pairing = None

        self.refresh_matchmaking_pairlist = None

    def init_sky_sphere(self):
        self.skysphere = loader.loadModel("ChessRender/data/menu_cubemap1.bam")
        self.skysphere.setBin('background', 1)
        self.skysphere.setDepthWrite(0)
        self.skysphere.reparentTo(render)
        self.skysphere.setPos(0, 0, 0)
        self.skysphere.setScale(25)

    def init_state_by_key(self, key):
        if self.cur_state_key != "fsm:Message":
            self.prev_render_not_message_state_key = self.cur_state_key

        self.cur_state_key = key
        if key == "fsm:MainMenu":
            return FsmStateMainMenu(self.is_client_connected_to_server,
                                    self.process_continue_online_game,
                                    self.on_application_exit,
                                    self)
        elif key == "fsm:SinglePlayerLobby":
            return FsmStateSinglePlayerLobby(self.process_offline_with_computer, self.process_offline_with_firend, self.process_reset_save_data_friend, self.process_reset_save_data_computer)
        elif key == "fsm:GameState":
            self.taskMgr.remove('camRotTask')
            if isinstance(self.cur_state, FsmStateSinglePlayerLobby):
                return FsmStateGameState(self,
                                         self.whiteside_pack_name,
                                         self.blackside_pack_name,
                                         self.side,
                                         "fsm:SinglePlayerLobby",
                                         self.check_move_func_for_pawn_swap,
                                         self.get_cur_turn_side,
                                         self.on_offline_game_exit)
            else:
                return FsmStateGameState(self,
                                         self.whiteside_pack_name,
                                         self.blackside_pack_name,
                                         self.side, "fsm:Matchmaking",
                                         self.check_move_func_for_pawn_swap,
                                         self.get_cur_turn_side,
                                         self.on_game_exit)
        elif key == "fsm:Multiplayer":
            return FsmStateMultiplayer()
        elif key == "fsm:Login":
            return FsmStateLogin(self.process_login, self)
        elif key == "fsm:Registration":
            return FsmStateRegistration(self.process_registration)
        elif key == "fsm:Message":
            return FsmStateMessage(self.message, self)
        elif key == "fsm:Matchmaking1Step":
            self.on_match_making_state()
            return FsmStateMatchmakingFirstStep(self.process_find_player, self.start_game_by_pairing, self)
        elif key == "fsm:Matchmaking":
            return FsmStateMatchmaking(self.process_find_player, self)
        elif key == "fsm:SkinSelect":
            self.taskMgr.remove('camRotTask')
            return FsmStateSkinSelect(self, self.process_skin_select, self.avail_packs)
        elif key == "fsm:AuthConfirm":
            return FsmStateAuthConfirm(self.process_confirm_auth, self.email)
        elif key == "fsm:WinSettings":
            return FsmStateWindowSettings(self)
        elif key == "fsm:WinPack":
            self.taskMgr.remove('camRotTask')
            return FsmStateWinPack(self, self.win_pack)
        else:
            assert (False, "Incorrect fsm state")

    def render(self):
        self.cur_state.render(self)

    def change_state(self, render_fsm, link_key):
        while self.on_update_now or self.is_clearing:
            sleep(5.0 / 1000.0)
        self.on_update_now = True
        print("create " + link_key)
        if render_fsm.cur_state is not None:
            print("clear " + str(render_fsm.cur_state))
            render_fsm.cur_state.clear()
            if self.cur_state_key == "fsm:GameState":
                render_fsm.sound.turn_off_all()
        render_fsm.cur_state = render_fsm.init_state_by_key(link_key)
        render_fsm.cur_state.render(render_fsm)
        # play music
        if link_key != "fsm:GameState":
            render_fsm.sound.play(SoundTypes.MAIN)
        else:
            render_fsm.sound.turn_off_all()
        self.on_update_now = False

    def go_to_prev_state(self):
        self.change_state(self, self.prev_render_not_message_state_key)

    # Mouse functions
    def mouse_task(self, task):
        self.cur_state.mouse_task()
        return Task.cont

    def mouse_press(self):
        self.cur_state.mouse_press()

    def mouse_release(self):
        self.cur_state.mouse_release()

    def set_pairing_list(self, pairing_list):
        if isinstance(self.cur_state, FsmStateMatchmakingFirstStep):
            self.cur_state.set_pairing_list(pairing_list)
