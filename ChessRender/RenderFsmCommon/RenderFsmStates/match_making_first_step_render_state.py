from direct.gui.DirectButton import DirectButton
from direct.gui.DirectScrolledList import DirectScrolledList

from ChessRender.RenderFsmCommon.button_fsm import ButtonFsm
from ChessRender.RenderFsmCommon.screen_states import ScreenState
from ChessRender.RenderFsmCommon.screen_text_fsm import ScreenTextFsm
from ChessRender.RenderFsmCommon.text_field_fsm import TextFieldFsm


class FsmStateMatchmakingFirstStep(ScreenState):
    def __init__(self, process_find_player, start_game_by_pairing, render_fsm):
        ScreenState.__init__(self)

        self.render_fsm_ref = render_fsm
        self.start_game_by_pairing = start_game_by_pairing
        self.screen_atributes.buttons["but:Back"] = ButtonFsm("Back", (0, 0, -0.8))
        self.screen_atributes.buttons["but:Create"] = ButtonFsm("Create game", (0, 0, -0.5))

        self.screen_atributes.screen_texts["scrtext:info"] = ScreenTextFsm(
            "Quick game:\nGame time (minutes), adding time (seconds)", (-0.85, 0.9))
        self.screen_atributes.screen_texts["scrtext:info1"] = ScreenTextFsm(
            "Connect to:\nLogin, rate, game time, adding time", (0.8, 0.73))

        self.screen_atributes.buttons["but:preset1"] = ButtonFsm("10, 0", (-1.25, 0, 0.7), None, None, (-1.5, 1.5, -0.3, 0.9), (1.8, 0.8, 0.8))
        self.screen_atributes.buttons["but:preset2"] = ButtonFsm("30,0", (-0.5, 0, 0.7), None, None, (-1.5, 1.5, -0.3, 0.9), (1.8, 0.8, 0.8))
        self.screen_atributes.buttons["but:preset3"] = ButtonFsm("5, 3", (-1.25, 0, 0.3), None, None, (-1.5, 1.5, -0.3, 0.9), (1.8, 0.8, 0.8))
        self.screen_atributes.buttons["but:preset4"] = ButtonFsm("3, 2", (-0.5, 0, 0.3), None, None, (-1.5, 1.5, -0.3, 0.9), (1.8, 0.8, 0.8))
        self.screen_atributes.buttons["but:preset5"] = ButtonFsm("1, 0", (-0.9, 0, -0.1), None, None, (-1.5, 1.5, -0.3, 0.9), (1.8, 0.8, 0.8))

        self.pairs_buts = []
        self.my_scrolled_list = None
        self.initialize_button_links()

        self.pairing_list = None

        self.process_matchmaking = process_find_player

        self.render_fsm_ref.message = "Finding player..."
        self.set_pairing_list([])

    def initialize_button_links(self):
        self.screen_atributes.buttons["but:Create"].add_link("fsm:Matchmaking")
        self.screen_atributes.buttons["but:Back"].add_link("fsm:MainMenu")

        self.screen_atributes.buttons["but:preset1"].add_command(self.confirm_preset1)
        self.screen_atributes.buttons["but:preset2"].add_command(self.confirm_preset2)
        self.screen_atributes.buttons["but:preset3"].add_command(self.confirm_preset3)
        self.screen_atributes.buttons["but:preset4"].add_command(self.confirm_preset4)
        self.screen_atributes.buttons["but:preset5"].add_command(self.confirm_preset5)

        self.screen_atributes.buttons["but:preset1"].add_link("fsm:Message")
        self.screen_atributes.buttons["but:preset2"].add_link("fsm:Message")
        self.screen_atributes.buttons["but:preset3"].add_link("fsm:Message")
        self.screen_atributes.buttons["but:preset4"].add_link("fsm:Message")
        self.screen_atributes.buttons["but:preset5"].add_link("fsm:Message")

    def confirm_preset1(self):
        process_matchmaking_arg = {"MatchTime": 30,
                                   "AddTime": 0,
                                   "MinRate": 0,
                                   "MaxRate": 3000
                                   }
        self.process_matchmaking(process_matchmaking_arg)

    def confirm_preset2(self):
        process_matchmaking_arg = {"MatchTime": 10,
                                   "AddTime": 0,
                                   "MinRate": 0,
                                   "MaxRate": 3000
                                   }
        self.process_matchmaking(process_matchmaking_arg)

    def confirm_preset3(self):
        process_matchmaking_arg = {"MatchTime": 5,
                                   "AddTime": 3,
                                   "MinRate": 0,
                                   "MaxRate": 3000
                                   }
        self.process_matchmaking(process_matchmaking_arg)

    def confirm_preset4(self):
        process_matchmaking_arg = {"MatchTime": 3,
                                   "AddTime": 2,
                                   "MinRate": 0,
                                   "MaxRate": 3000
                                   }
        self.process_matchmaking(process_matchmaking_arg)

    def confirm_preset5(self):
        process_matchmaking_arg = {"MatchTime": 1,
                                   "AddTime": 0,
                                   "MinRate": 0,
                                   "MaxRate": 3000
                                   }
        self.process_matchmaking(process_matchmaking_arg)

    def set_pairing_list(self, pairing_list):
        for but in self.pairs_buts:
            but.removeNode()
        if self.my_scrolled_list is not None:
            self.my_scrolled_list.removeNode()

        self.pairing_list = pairing_list
        self.pairs_buts = []
        for pair in pairing_list:
            print(str(pair))
            self.pairs_buts.append(
                DirectButton(
                    text=str(pair[1]) + ', ' + str(pair[2]) + ', ' + str(pair[3]) + ', ' + str(pair[4]), scale=0.1,
                    command=self.start_game_by_pairing,
                    extraArgs=[pair[0]],
                    frameColor=((0.8, 0.8, 0.8, 0.8), (0.4, 0.4, 0.4, 0.8), (0.4, 0.4, 0.8, 0.8),
                                (0.1, 0.1, 0.1, 0.8)),
                    frameSize=(-6.5, 6.5, -0.4, 0.8)
                )
            )

        self.my_scrolled_list = DirectScrolledList(
            decButton_pos=(0.35, -0, 0.87),
            decButton_text="up",
            decButton_text_scale=0.08,
            decButton_borderWidth=(0.005, 0.005),
            decButton_frameSize=(-0.25, 0.25, -0.05, 0.1),

            incButton_pos=(0.35, 0, -0.08),
            incButton_text="down",
            incButton_text_scale=0.08,
            incButton_borderWidth=(0.005, 0.005),
            incButton_frameSize=(-0.25, 0.25, -0.05, 0.1),

            # frameSize=(-0.7, 1.7, 0.8, 0),
            # frameColor=(1.3, 0.3, 1, 0.5),
            pos=(0.5, 0, 0),
            items=self.pairs_buts,
            numItemsVisible=5,
            forceHeight=0.11,
            itemFrame_frameSize=(-0.8, 0.8, -0.52, 0.26),
            itemFrame_pos=(0.35, 0, 0.55),
        )

    def clear_state(self):
        self.render_fsm_ref.is_clearing = True
        self.my_scrolled_list.removeNode()
        for but in self.pairs_buts:
            but.removeNode()
        #for but in self.pairs_buts:
            #but.remove_node()
        self.render_fsm_ref.is_clearing = False
