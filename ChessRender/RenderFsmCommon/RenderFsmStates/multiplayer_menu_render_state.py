from ChessRender.RenderFsmCommon.button_fsm import ButtonFsm
from ChessRender.RenderFsmCommon.screen_states import ScreenState


class FsmStateMultiplayer(ScreenState):
    def __init__(self):
        ScreenState.__init__(self)
        self.button_sizes = (-4, 4, -0.5, 1)
        self.screen_atributes.buttons["but:Registration"] = ButtonFsm("Registration", (0, 0, 0.4))
        self.screen_atributes.buttons["but:Login"] = ButtonFsm("Login", (0, 0, 0))
        self.screen_atributes.buttons["but:Back"] = ButtonFsm("Back", (0, 0, -0.8))
        self.initialize_button_links()

    def initialize_button_links(self):
        self.screen_atributes.buttons["but:Registration"].add_link("fsm:Registration")
        self.screen_atributes.buttons["but:Login"].add_link("fsm:Login")
        self.screen_atributes.buttons["but:Back"].add_link("fsm:MainMenu")
