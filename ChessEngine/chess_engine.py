###############################
# MODULE: Chess engine class  #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 03/03/2019     #
###############################

from ChessRender.chess_render import Render


class Engine:

    def __init__(self):
        """
        Initialize Engine class function
        """
        self.render = Render()
        self.player = None
        self.opponent = None

    def run(self):
        """
        Main loop function
        :return: NONE.
        """
        while True is True:
            self.render.render()
