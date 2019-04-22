###############################
# MODULE: Obtain functions    #
# AUTHOR: Yangildin Ivan      #
# LAST UPDATE: 09/04/2019     #
###############################
from enum import Enum

#### - const literals
L_LOGIN = "Login"
L_PAROL = "Parol"
L_GAME_TIME = "Game time"
L_MOVE_TIME = "Move time"
L_MIN_RATE = "Min. rate"
L_MAX_RATE = "Max. rate"
L_EMAIL = "E-mail"

class RoomState(Enum):
    DEFAULT = -1,
    INPUT = 0,
    GAME = 1,
    MENU = 2,
    LOGIN = 3,
    FIND_PLAYER = 4,
    REGISTER = 5,

def dummy_fun(text_dict):
    """
    Just fake function
    """
    print(text_dict)

class room():
    def __init__(self):
        self.state = RoomState.MENU

        #### - array of buttons and textfields
        self.buttons_prim = None
        self.text_fields_prim = None

        #### - functions to process data
        self.process_login = dummy_fun
        self.process_find_player = dummy_fun
        self.process_register = dummy_fun


    def process_data(self, render):
        text_dict = {}
        if self.text_fields_prim is not None:
            for i in range(0, len(self.text_fields_prim)):
                text_dict[self.text_fields_prim[i].title] = self.text_fields_prim[i].text

        if self.state is RoomState.LOGIN:
            self.process_login(text_dict)
        if self.state is RoomState.FIND_PLAYER:
            self.process_find_player(text_dict)
        if self.state is RoomState.REGISTER:
            self.process_register(text_dict)

        return text_dict
