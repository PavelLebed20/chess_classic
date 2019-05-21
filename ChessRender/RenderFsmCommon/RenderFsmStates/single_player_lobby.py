from ChessRender.RenderFsmCommon.button_fsm import ButtonFsm
from ChessRender.RenderFsmCommon.screen_states import ScreenState


class FsmStateSinglePlayerLobby(ScreenState):
    def __init__(self, process_game_with_computer, process_game_with_firend, process_reset_save_data_friend, process_reset_save_data_computer):
        ScreenState.__init__(self)
        self.button_sizes = (-4, 4, -0.5, 1)
        self.screen_atributes.buttons["but:2Players"] = ButtonFsm("With friend", (-0.5, 0, 0.4), None, None, None, (4, 1, 1))
        self.screen_atributes.buttons["but:Computer"] = ButtonFsm("With computer", (-0.5, 0, 0), None, None, None, (4, 1, 1))

        self.screen_atributes.buttons["but:2PlayersReset"] = ButtonFsm("Reset", (0.8, 0, 0.4), None, None, (-1.3, 1.4, -0.5, 1), (3, 1, 1))
        self.screen_atributes.buttons["but:ComputerReset"] = ButtonFsm("Reset", (0.8, 0, 0),  None, None, (-1.3, 1.4, -0.5, 1), (3, 1, 1))

        self.screen_atributes.buttons["but:Back"] = ButtonFsm("Back", (0, 0, -0.8))

        self.process_game_with_computer = process_game_with_computer
        self.process_game_with_firend = process_game_with_firend

        self.process_reset_save_data_friend = process_reset_save_data_friend
        self.process_reset_save_data_computer = process_reset_save_data_computer

        self.initialize_button_links()

    def initialize_button_links(self):
        self.screen_atributes.buttons["but:2Players"].add_link("fsm:GameState")
        self.screen_atributes.buttons["but:2Players"].add_command(self.process_game_with_firend)

        self.screen_atributes.buttons["but:Computer"].add_link("fsm:GameState")
        self.screen_atributes.buttons["but:Computer"].add_command(self.process_game_with_computer)

        self.screen_atributes.buttons["but:2PlayersReset"].add_command(self.process_reset_save_data_friend)
        self.screen_atributes.buttons["but:ComputerReset"].add_command(self.process_reset_save_data_computer)

        self.screen_atributes.buttons["but:Back"].add_link("fsm:MainMenu")
