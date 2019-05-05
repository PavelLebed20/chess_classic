from time import sleep

from direct.showbase.ShowBase import ShowBase, WindowProperties
from direct.task import Task

from ChessRender.RenderFsmCommon.RenderFsmStates.auth_confirm_state import FsmStateAuthConfirm
from ChessRender.RenderFsmCommon.RenderFsmStates.game_render_state import FsmStateGameState
from ChessRender.RenderFsmCommon.RenderFsmStates.load_render_state import FsmStateLoad
from ChessRender.RenderFsmCommon.RenderFsmStates.login_render_state import FsmStateLogin
from ChessRender.RenderFsmCommon.RenderFsmStates.main_menu_render_state import FsmStateMainMenu
from ChessRender.RenderFsmCommon.RenderFsmStates.match_making_state import FsmStateMatchmaking
from ChessRender.RenderFsmCommon.RenderFsmStates.multiplayer_menu_render_state import FsmStateMultiplayer
from ChessRender.RenderFsmCommon.RenderFsmStates.registration_render_state import FsmStateRegistration
from ChessRender.RenderFsmCommon.RenderFsmStates.skin_select_render_state import FsmStateSkinSelect


class RenderFsm(ShowBase):
    WIDTH = 1024
    HEIGHT = 900

    def __init__(self):
        ShowBase.__init__(self)

        props = WindowProperties()
        props.clearSize()
        props.setTitle('Chess Classic')
        props.setSize(self.WIDTH, self.HEIGHT)
        self.win.requestProperties(props)

        self.taskMgr.add(self.mouse_task, 'mouseTask')
        self.accept("mouse1", self.mouse_press)
        self.accept("mouse1-up", self.mouse_release)

        self.cur_state = None

        # user data obtain fucntins
        self.process_login = None
        self.process_find_player = None
        self.process_registration = None
        self.process_skin_select = None
        self.process_confirm_auth = None

        self.process_offline_game = None
        self.process_set_move_player = None

        self.whiteside_pack_name = None
        self.blackside_pack_name = None

        self.on_update_now = False
        self.is_clearing = False
        self.state_priority = -1
        self.cur_state_key = ""
        self.on_game_exit = None

    def init_state_by_key(self, key):
        self.cur_state_key = key
        if key == "fsm:MainMenu":
            return FsmStateMainMenu(self.process_offline_game)
        elif key == "fsm:GameState":
            return FsmStateGameState(self, self.whiteside_pack_name,
                                     self.blackside_pack_name, self.on_game_exit)
        elif key == "fsm:Multiplayer":
            return FsmStateMultiplayer()
        elif key == "fsm:Login":
            return FsmStateLogin(self.process_login)
        elif key == "fsm:Registration":
            return FsmStateRegistration(self.process_registration)
        elif key == "fsm:Load":
            return FsmStateLoad()
        elif key == "fsm:Matchmaking":
            return FsmStateMatchmaking(self.process_find_player)
        elif key == "fsm:SkinSelect":
            return FsmStateSkinSelect(self, self.process_skin_select)
        elif key == "fsm:AuthConfirm":
            return FsmStateAuthConfirm(self.process_confirm_auth)

    def render(self):
        self.cur_state.render(self)

    def change_state(self, render_fsm, link_key):
        while self.on_update_now or self.is_clearing:
            sleep(1000.0 / 1000.0)
        self.on_update_now = True
        print("create " + link_key)
        if render_fsm.cur_state is not None:
            print("clear " + str(render_fsm.cur_state))
            render_fsm.cur_state.clear()
        render_fsm.cur_state = render_fsm.init_state_by_key(link_key)
        render_fsm.cur_state.render(render_fsm)
        self.on_update_now = False

    # Mouse functions
    def mouse_task(self, task):
        self.cur_state.mouse_task()
        return Task.cont

    def mouse_press(self):
        self.cur_state.mouse_press()

    def mouse_release(self):
        self.cur_state.mouse_release()
