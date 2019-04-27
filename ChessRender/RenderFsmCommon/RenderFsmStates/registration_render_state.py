from ChessRender.RenderFsmCommon.button_fsm import ButtonFsm
from ChessRender.RenderFsmCommon.screen_states import ScreenState


class FsmStateRegistration(ScreenState):
    def __init__(self):
        ScreenState.__init__(self)
        self.screen_atributes.buttons["but:Confirm"] = ButtonFsm("Confirm", (0, 0, 0))

    def initialize_button_links(self):
        pass
