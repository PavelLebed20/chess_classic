from ChessRender.RenderFsmCommon.button_fsm import ButtonFsm
from ChessRender.RenderFsmCommon.screen_states import ScreenState
from ChessRender.RenderFsmCommon.screen_text_fsm import ScreenTextFsm
from ChessRender.RenderFsmCommon.text_field_fsm import TextFieldFsm


class FsmStateWinPack(ScreenState):
    def __init__(self, pack_name):
        ScreenState.__init__(self)

        self.screen_atributes.buttons["but:Confirm"] = ButtonFsm("Confirm", (0, 0, -0.5))

        self.screen_atributes.screen_texts["scrtext:WinPack"] = ScreenTextFsm(pack_name, (0.0, 0.0))

        self.initialize_button_links()


    def initialize_button_links(self):
        self.screen_atributes.buttons["but:Confirm"].add_link("fsm:MainMenu")


