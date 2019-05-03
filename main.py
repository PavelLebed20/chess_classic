###############################
# MODULE: Chess main class    #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 03/03/2019     #
###############################
import smtplib

from ChessEngine.chess_engine import Engine

if __name__ == '__main__':
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login("chess.classic.official@gmail.com", "ChhessClassicc1488")
        msg = "Hello"
        server.sendmail("chess.classic.official@gmail.com", "pavellebed30@gmail.com", msg)
        server.quit()
    except:
        print
        'Something went wrong...'

    engine = Engine()
    engine.render.run()
