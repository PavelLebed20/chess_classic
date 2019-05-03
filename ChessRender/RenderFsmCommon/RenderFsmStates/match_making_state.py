from ChessRender.RenderFsmCommon.button_fsm import ButtonFsm
from ChessRender.RenderFsmCommon.screen_states import ScreenState
from ChessRender.RenderFsmCommon.screen_text_fsm import ScreenTextFsm
from ChessRender.RenderFsmCommon.text_field_fsm import TextFieldFsm


class FsmStateMatchmaking(ScreenState):
    def __init__(self, process_find_player):
        ScreenState.__init__(self)

        self.screen_atributes.buttons["but:Back"] = ButtonFsm("Back", (0, 0, -0.8))
        self.screen_atributes.buttons["but:Confirm"] = ButtonFsm("Confirm", (0, 0, -0.5))

        self.screen_atributes.text_fields["text_field:Match time"] = TextFieldFsm("text_field_match_time", (-0.5, 0, 0.5), "")
        self.screen_atributes.text_fields["text_field:Addition time"] = TextFieldFsm("text_field_add_time", (-0.5, 0, 0.3), "")
        self.screen_atributes.text_fields["text_field:Min rate"] = TextFieldFsm("text_field_min_rate", (-0.5, 0, 0.1), "")
        self.screen_atributes.text_fields["text_field:Max rate"] = TextFieldFsm("text_field_max_rate", (-0.5, 0, -0.1), "")

        self.screen_atributes.screen_texts["scrtext:Match time"] = ScreenTextFsm("Match time:          ", (-0.85, 0.5))
        self.screen_atributes.screen_texts["scrtext:Addition time"] = ScreenTextFsm("Addition time:    ", (-0.85, 0.3))
        self.screen_atributes.screen_texts["scrtext:Min rate"] = ScreenTextFsm("Min rate:              ", (-0.85, 0.1))
        self.screen_atributes.screen_texts["scrtext:Max rate"] = ScreenTextFsm("Max rate:              ", (-0.85, -0.1))

        self.initialize_button_links()

        self.login_field = None
        self.password_field = None

        self.process_matchmaking = process_find_player

    def initialize_button_links(self):
        self.screen_atributes.buttons["but:Confirm"].add_link("fsm:Load")
        self.screen_atributes.buttons["but:Confirm"].add_command(self.confirm_command)
        self.screen_atributes.buttons["but:Back"].add_link("fsm:Login")

    def confirm_command(self):
        process_matchmaking_arg = {"MatchTime": self.gui_text_fields["text_field_match_time"].get(),
                                    "AddTime": self.gui_text_fields["text_field_add_time"].get(),
                                    "MinRate": self.gui_text_fields["text_field_min_rate"].get(),
                                    "MaxRate": self.gui_text_fields["text_field_max_rate"].get()
                                    }
        self.process_matchmaking(process_matchmaking_arg)


