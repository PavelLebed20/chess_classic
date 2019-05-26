
class HistMovementManager:
    def __init__(self):
        self.boards_hist = []
        self.cur_board = -1
        self.offset = 0

    def make_screen(self, board):
        if self.cur_board != -1 and self.boards_hist[self.cur_board] == board:
            return
        self.boards_hist.append(board)
        self.cur_board += 1

    def get_prev(self):
        if self.cur_board + self.offset > 0:
            self.offset -= 1
        return self.boards_hist[self.cur_board + self.offset]

    def get_next(self):
        if self.offset < 0:
            self.offset += 1
        return self.boards_hist[self.cur_board + self.offset]

    def clear(self):
        self.boards_hist = []
        self.cur_board = -1
        self.offset = 0

    def get_hist_board(self):
        return self.boards_hist[self.cur_board + self.offset]

    def up_to_date(self):
        return self.offset == 0

    def reset_offset(self):
        self.offset = 0
