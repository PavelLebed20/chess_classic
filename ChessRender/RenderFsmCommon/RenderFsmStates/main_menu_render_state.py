import sys

from ChessRender.RenderFsmCommon.button_fsm import ButtonFsm
from ChessRender.RenderFsmCommon.screen_states import ScreenState


class FsmStateMainMenu(ScreenState):
    def __init__(self, process_offline_game):
        ScreenState.__init__(self)

        self.screen_atributes.buttons["but:Single player"] = ButtonFsm("Single player", (0, 0, 0.7))
        self.screen_atributes.buttons["but:Multiplayer"] = ButtonFsm("Multiplayer", (0, 0, 0.35))
        self.screen_atributes.buttons["but:Select skins"] = ButtonFsm("Select skins", (0, 0, 0))
        self.screen_atributes.buttons["but:Window settings"] = ButtonFsm("Settigns", (0, 0, -0.35))
        self.screen_atributes.buttons["but:Exit"] = ButtonFsm("Exit", (0, 0, -0.8))

        self.process_offline_game = process_offline_game
        self.initialize_button_links()

    def initialize_button_links(self):
        self.screen_atributes.buttons["but:Single player"].add_link("fsm:GameState")
        self.screen_atributes.buttons["but:Single player"].add_command(self.process_offline_game)
        self.screen_atributes.buttons["but:Multiplayer"].add_link("fsm:Multiplayer")
        self.screen_atributes.buttons["but:Select skins"].add_link("fsm:SkinSelect")
        self.screen_atributes.buttons["but:Window settings"].add_link("fsm:WinSettings")
        self.screen_atributes.buttons["but:Exit"].add_command(sys.exit)
