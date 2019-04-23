###############################
# MODULE: Obtain functions    #
# AUTHOR: Yangildin Ivan      #
# LAST UPDATE: 09/04/2019     #
###############################

#### - const literals
L_LOGIN = "Login"
L_PAROL = "Parol"
L_GAME_TIME = "Game time"
L_MOVE_TIME = "Move time"
L_MIN_RATE = "Min. rate"
L_MAX_RATE = "Max. rate"

class room():
    def __init__(self):
        #### - array of buttons and textfields
        self.buttons_prim = None
        self.text_fields_prim = None

        ####
        self.user_param = []


        #### - functions to process data
        self.process_login = None
        self.process_find_player = None
        self.process_load_model = None

    def process_data(self, render):
        text_dict = {}
        if self.text_fields_prim is not None:
            for i in range(0, len(self.text_fields_prim)):
                text_dict[self.text_fields_prim[i].title] = self.text_fields_prim[i].text

        if text_dict.get("Path to .png") is not None:
            if len(self.user_param) == 0:
                self.process_load_model(text_dict)
            elif len(self.user_param) == 2:
                self.process_load_model(text_dict, self.user_param[0], self.user_param[1])

        if (text_dict.get(L_LOGIN) is not None) and (text_dict.get(L_PAROL) is not None):
            if self.process_login is not None:
                self.process_login(text_dict)
        if (text_dict.get(L_GAME_TIME) is not None) and (text_dict.get(L_MOVE_TIME) is not None) and (
                    text_dict.get(L_MIN_RATE) is not None) and (text_dict.get(L_MAX_RATE) is not None):
            if self.process_login is not None:
                self.process_find_player(text_dict)
        return text_dict
