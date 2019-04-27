from ChessRender.RenderFsmCommon.button_fsm import ButtonFsm
from ChessRender.RenderFsmCommon.screen_states import ScreenState


class FsmStateMainMenu(ScreenState):
    def __init__(self):
        ScreenState.__init__(self)
        self.screen_atributes.buttons["but:Single player"] = ButtonFsm("Single player", (0, 0, 0.4))
        self.screen_atributes.buttons["but:Multiplayer"] = ButtonFsm("Multiplayer", (0, 0, 0))
        self.screen_atributes.buttons["but:Load skins"] = ButtonFsm("Load skins", (0, 0, -0.4))
        self.screen_atributes.buttons["but:Exit"] = ButtonFsm("Exit", (0, 0, -0.8))
        self.initialize_button_links()

    def initialize_button_links(self):
        self.screen_atributes.buttons["but:Single player"].add_link("fsm:GameState")
        self.screen_atributes.buttons["but:Multiplayer"].add_link("fsm:Multiplayer")
        self.screen_atributes.buttons["but:Load skins"].add_link("fsm:Load")
        self.screen_atributes.buttons["but:Exit"].add_link("fsm:Exit")
