from ChessRender.RenderFsmCommon.button_fsm import ButtonFsm
from ChessRender.RenderFsmCommon.screen_states import ScreenState
from ChessRender.RenderFsmCommon.screen_text_fsm import ScreenTextFsm


class FsmStateMessage(ScreenState):
    def __init__(self, str_message, render_fsm):
        ScreenState.__init__(self)
        self.render_fsm_ref = render_fsm
        self.screen_atributes.screen_texts["scrtext:Message"] = ScreenTextFsm(str_message, (0, 0))
        self.screen_atributes.buttons["but:Back"] = ButtonFsm("Back", (0, 0, -0.8))
        self.initialize_button_links()

    def initialize_button_links(self):
        self.screen_atributes.buttons["but:Back"].add_command(self.render_fsm_ref.go_to_prev_state)
