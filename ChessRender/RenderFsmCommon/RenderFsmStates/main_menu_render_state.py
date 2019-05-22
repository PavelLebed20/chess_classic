import sys

from ChessRender.RenderFsmCommon.button_fsm import ButtonFsm
from ChessRender.RenderFsmCommon.screen_states import ScreenState
from ChessRender.RenderFsmCommon.screen_states import screen_style as style


class FsmStateMainMenu(ScreenState):
    def __init__(self, is_client_connected_to_server, process_continue_online_game, on_application_exit, render_fsm):
        ScreenState.__init__(self)
        self.button_sizes = (-4, 4, -0.5, 1)

        self.screen_atributes.buttons["but:Single player"] = ButtonFsm("Single player", (0, 0, 0.7))
        if is_client_connected_to_server is False:
            self.screen_atributes.buttons["but:Multiplayer"] = ButtonFsm("Connect to online", (0, 0, 0.35))
        else:
            self.screen_atributes.buttons["but:Multiplayer"] = ButtonFsm("Multiplayer", (0, 0, 0.35))

        self.screen_atributes.buttons["but:Select skins"] = ButtonFsm("Select skins", (0, 0, 0))
        self.screen_atributes.buttons["but:Window settings"] = ButtonFsm("Settigns", (0, 0, -0.35))
        self.screen_atributes.buttons["but:Exit"] = ButtonFsm("Exit", (0, 0, -0.8))

        self.screen_atributes.buttons["but:Style"] = ButtonFsm("Style", (1.3, 0, 0.7), None, None, (-1.5, 1.5, -0.4, 0.8), (1.8, 0.8, 0.8))

        # self.process_offline_game = process_offline_game
        self.process_continue_online_game = process_continue_online_game
        self.is_client_connected_to_server = is_client_connected_to_server
        self.on_application_exit = on_application_exit
        self.render_fsm_ref = render_fsm
        self.initialize_button_links()

    def initialize_button_links(self):
        self.screen_atributes.buttons["but:Single player"].add_link("fsm:SinglePlayerLobby")
        #self.screen_atributes.buttons["but:Single player"].add_command(self.process_offline_game)
        if self.is_client_connected_to_server is False:
            self.screen_atributes.buttons["but:Multiplayer"].add_link("fsm:Multiplayer")
        else:
            self.screen_atributes.buttons["but:Multiplayer"].add_command(self.process_continue_online_game)
        self.screen_atributes.buttons["but:Select skins"].add_link("fsm:SkinSelect")
        self.screen_atributes.buttons["but:Window settings"].add_link("fsm:WinSettings")
        self.screen_atributes.buttons["but:Exit"].add_command(self.on_application_exit)
        self.screen_atributes.buttons["but:Style"].add_command(self.change_screen_style)

    def change_screen_style(self):
        global style
        style = not style
        self.clear_state()
        self.clear()
        self.render(self.render_fsm_ref)