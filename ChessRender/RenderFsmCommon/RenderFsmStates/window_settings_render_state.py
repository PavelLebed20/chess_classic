from ChessRender.RenderFsmCommon.button_fsm import ButtonFsm
from ChessRender.RenderFsmCommon.radio_button_fsm import RadioButtonFsm
from ChessRender.RenderFsmCommon.screen_states import ScreenState
from ChessRender.RenderFsmCommon.screen_text_fsm import ScreenTextFsm
from direct.showbase.ShowBase import ShowBase, WindowProperties

DEFAULT16x9SCREEN_W = 1280
DEFAULT16x9SCREEN_H = 720

DEFAULT4x3SCREEN_W = 1024
DEFAULT4x3SCREEN_H = 768

class FsmStateWindowSettings(ScreenState):
    def __init__(self, render_fsm):
        ScreenState.__init__(self)
        self.render_fsm_ref = render_fsm

        self.screen_atributes.screen_texts["screen_text:Title"] = ScreenTextFsm("Select your windows params:", (0, 0.3))

        self.screen_atributes.radio_buttons["rb:WinSize 16:9"] = RadioButtonFsm("16:9", (-0.2, 0, 0), self.confirm_command)
        self.screen_atributes.radio_buttons["rb:WinSize 4:3"] = RadioButtonFsm("4:3", (0.2, 0, 0), self.confirm_command)

        self.screen_atributes.buttons["but:Confirm"] = ButtonFsm("Confirm", (0, 0, -0.5))
        self.screen_atributes.buttons["but:Back"] = ButtonFsm("Back", (0, 0, -0.8))

        self.initialize_button_links()


    def initialize_button_links(self):
        self.screen_atributes.buttons["but:Confirm"].add_link("fsm:MainMenu")
        self.screen_atributes.buttons["but:Confirm"].add_command(self.confirm_command)
        self.screen_atributes.buttons["but:Back"].add_link("fsm:MainMenu")

    def confirm_command(self):
        # 16:9
        if self.radio_button_var[0] == 0:
            props = WindowProperties()
            props.clearSize()
            props.setTitle('Chess Classic')
            props.setSize(DEFAULT16x9SCREEN_W, DEFAULT16x9SCREEN_H)
            props.setFixedSize(True)
            self.render_fsm_ref.win.requestProperties(props)

        # 4:3
        if self.radio_button_var[0] == 1:
            props = WindowProperties()
            props.clearSize()
            props.setTitle('Chess Classic')
            props.setSize(DEFAULT4x3SCREEN_W, DEFAULT4x3SCREEN_H)
            props.setFixedSize(True)
            self.render_fsm_ref.win.requestProperties(props)
