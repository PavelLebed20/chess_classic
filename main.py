###############################
# MODULE: Chess main class    #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 03/03/2019     #
###############################

from ChessEngine.chess_engine import Engine

if __name__ == '__main__':
    engine = Engine()
    engine.render.run()
