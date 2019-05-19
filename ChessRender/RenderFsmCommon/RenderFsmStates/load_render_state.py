from ChessRender.RenderFsmCommon.button_fsm import ButtonFsm
from ChessRender.RenderFsmCommon.screen_states import ScreenState
from ChessRender.RenderFsmCommon.screen_text_fsm import ScreenTextFsm


class FsmStateLoad(ScreenState):
    def __init__(self):
        ScreenState.__init__(self)

        self.screen_atributes.screen_texts["scrtext:Loading"] = ScreenTextFsm("Loading...", (0, 0))
        self.screen_atributes.buttons["but:Back"] = ButtonFsm("Back", (0, 0, -0.8))
        self.initialize_button_links()

    def initialize_button_links(self):
        self.screen_atributes.buttons["but:Back"].add_link("fsm:MainMenu")