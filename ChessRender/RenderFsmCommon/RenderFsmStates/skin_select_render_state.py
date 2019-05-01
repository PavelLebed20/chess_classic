from direct.gui.DirectOptionMenu import DirectOptionMenu

from ChessRender.RenderFsmCommon.button_fsm import ButtonFsm
from ChessRender.RenderFsmCommon.option_list_fsm import OptionListFsm
from ChessRender.RenderFsmCommon.screen_states import ScreenState
from ChessRender.RenderFsmCommon.screen_text_fsm import ScreenTextFsm
from ChessRender.RenderFsmCommon.text_field_fsm import TextFieldFsm


class FsmStateSkinSelect(ScreenState):
    def __init__(self, process_skin_select):
        ScreenState.__init__(self)

        self.screen_atributes.buttons["but:Confirm"] = ButtonFsm("Confirm", (0.5, 0, -0.8))
        self.screen_atributes.buttons["but:Back"] = ButtonFsm("Back", (-0.5, 0, -0.8))
        self.screen_atributes.option_lists["oplst:PackName"] = OptionListFsm("Pack", ["pack 0", "pack 1"], self.option_list_confirm, (-0.5, 0 ,0.8))

        self.initialize_button_links()

        self.process_skin_select = process_skin_select

    def initialize_button_links(self):
        self.screen_atributes.buttons["but:Confirm"].add_link("fsm:MainMenu")
        self.screen_atributes.buttons["but:Confirm"].add_command(self.confirm_command)
        self.screen_atributes.buttons["but:Back"].add_link("fsm:MainMenu")

    def option_list_confirm(self, arg):
        print(arg)

    def confirm_command(self):
        self.process_skin_select()


