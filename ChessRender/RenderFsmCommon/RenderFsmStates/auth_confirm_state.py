from ChessRender.RenderFsmCommon.button_fsm import ButtonFsm
from ChessRender.RenderFsmCommon.screen_states import ScreenState
from ChessRender.RenderFsmCommon.screen_text_fsm import ScreenTextFsm
from ChessRender.RenderFsmCommon.text_field_fsm import TextFieldFsm


class FsmStateAuthConfirm(ScreenState):
    def __init__(self, process_auth_confirm, email=''):
        ScreenState.__init__(self)

        self.screen_atributes.buttons["but:Confirm"] = ButtonFsm("Confirm", (0, 0, -0.5))
        self.screen_atributes.buttons["but:Back"] = ButtonFsm("Back", (0, 0, -0.8))

        self.screen_atributes.text_fields["text_field:Email"] = TextFieldFsm("text_field_email", (-0.5, 0, 0.5),
                                                                             initial_text=email)
        self.screen_atributes.text_fields["text_field:AuthCode"] = TextFieldFsm("text_field_auth_code", (-0.5, 0, 0.3))

        self.screen_atributes.screen_texts["scrtext:Email"] = ScreenTextFsm("email:   ", (-0.7, 0.5))
        self.screen_atributes.screen_texts["scrtext:AuthCode"] = ScreenTextFsm("auth code:", (-0.7, 0.3))

        self.initialize_button_links()

        self.email_field = None
        self.auth_code_field = None

        self.process_auth_confirm = process_auth_confirm

    def initialize_button_links(self):
        #self.screen_atributes.buttons["but:Confirm"].add_link("fsm:Load")
        self.screen_atributes.buttons["but:Confirm"].add_command(self.confirm_command)
        self.screen_atributes.buttons["but:Back"].add_link("fsm:Multiplayer")

    def confirm_command(self):
        process_args = {"Email": self.gui_text_fields["text_field_email"].get(),
                        "AuthCode": self.gui_text_fields["text_field_auth_code"].get()}
        self.process_auth_confirm(process_args)


