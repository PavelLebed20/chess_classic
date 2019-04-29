from ChessRender.RenderFsmCommon.screen_states import ScreenState
from ChessRender.RenderFsmCommon.screen_text_fsm import ScreenTextFsm


class FsmStateLoad(ScreenState):
    def __init__(self):
        ScreenState.__init__(self)

        self.screen_atributes.screen_texts["scrtext:Loading"] = ScreenTextFsm("Loading...", (0, 0))
