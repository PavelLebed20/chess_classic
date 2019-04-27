from ChessRender.RenderFsmCommon.button_fsm import ButtonFsm
from ChessRender.RenderFsmCommon.screen_states import ScreenState
from ChessRender.RenderFsmCommon.text_field_fsm import TextFieldFsm


class FsmStateLogin(ScreenState):
    def __init__(self, process_login):
        ScreenState.__init__(self)

        self.screen_atributes.buttons["but:Back"] = ButtonFsm("Back", (0, 0, -0.8))
        self.screen_atributes.buttons["but:Confirm"] = ButtonFsm("Confirm", (0, 0, -0.5))

        self.screen_atributes.text_fields["text_field:Login"] = TextFieldFsm("text_field_login", (-0.5, 0, 0.5), "Login")
        self.screen_atributes.text_fields["text_field:Password"] = TextFieldFsm("text_field_password", (-0.5, 0, 0.3), "Password")

        self.initialize_button_links()

        self.login_field = None
        self.password_field = None

        self.process_login = process_login

    def initialize_button_links(self):
        self.screen_atributes.buttons["but:Confirm"].add_link("fsm:Load")
        self.screen_atributes.buttons["but:Confirm"].add_command(self.confirm_command)
        self.screen_atributes.buttons["but:Back"].add_link("fsm:Multiplayer")

    def confirm_command(self):
        process_login_arg = {"Login": self.gui_text_fields["text_field_login"].get(),
                             "Password": self.gui_text_fields["text_field_password"].get()}
        self.process_login(process_login_arg)


