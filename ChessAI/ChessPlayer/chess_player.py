###############################
# MODULE: Chess Player class  #
# AUTHOR: Fedorov Dmitrii     #
# LAST UPDATE: 03/03/2019     #
###############################
import datetime
import time

from ChessBoard.chess_figure import Side


class Player:

    def __init__(self, side=Side.WHITE):
        """
        Initialize player class function
        """
        self.time_left = -1
        self.time_of_update = -1
        self.login = ''
        self.rate = -1
        self.side = side
        self.is_stopped = False

    def make_move(self, game_controller=None):
        """
        Make player start calculate his move
        :return:
        """
        pass

    def get_move(self):
        """
        Try get move calculation results
        :return: NONE - player don't make move yet,
                 move - otherwise
        """
        pass

    @staticmethod
    def milli_seconds_time():
        return time.time() * 1000  #+ datetime.datetime.now().microsecond // 1000

    def init_time(self, time_in_millisecs):
        self.is_stopped = False
        self.time_left = time_in_millisecs
        self.time_of_update = Player.milli_seconds_time()

    def init_time_from_str(self, time_in_str):
        times = str(time_in_str).split(':')
        time_left = int(times[2]) + int(times[1]) * 60 + + int(times[0]) * 3600
        self.init_time(time_left * 1000)

    def restart_timer(self):
        self.time_of_update = Player.milli_seconds_time()

    def stop_timer(self):
        self.is_stopped = True

    def update_time(self):
        if self.is_stopped is True:
            return
        cur_time = Player.milli_seconds_time()
        if cur_time - self.time_of_update == 0:
            return

        self.time_left -= (cur_time - self.time_of_update)
        if self.time_left < 0:
            self.time_left = 0
        self.time_of_update = cur_time

    def is_time_over(self):
        return self.time_left == 0

    def time_str(self):
        seconds = self.time_left // 1000
        minutes = seconds // 60
        #hours = minutes // 60

        seconds = seconds % 60
        minutes = minutes % 60

        return str(int(minutes)).rjust(2, '0') + ":" + str(int(seconds)).rjust(2, '0')

    def update_login(self, login):
        self.login = str(login)

    def update_rate(self, rate):
        self.rate = int(rate)
