###############################
# MODULE: Chess board class   #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 03/03/2019     #
###############################

# BOARD FORMAT DESCRIPTION
# uppercase letters - for white
# lowercase letters - for black
# K\k - king
# Q\q - queen
# B\b - bishop
# N\n - knight
# R\r - rook
# P\p - pawn


from ChessBoard.chess_figure import Side, Figure, FigureType
from Vector2d.Vector2d import Vector2d


class Board:
    _DEFAULT_BOARD_POSITION = "rnbqkbkr" \
                              "pppppppp" \
                              "........" \
                              "........" \
                              "........" \
                              "........" \
                              "PPPPPPPP" \
                              "RNBQKBNR"

    COLUMN_SIZE = 8
    ROW_SIZE = 8
    FULL_SIZE = COLUMN_SIZE * ROW_SIZE

    def __init__(self, board_position=_DEFAULT_BOARD_POSITION):
        """
        Initialize ChessBoard class function
        :param board_position: board position in special format (str),
         see: BOARD_FORMAT_DESCRIPTION
        """
        assert len(board_position) == Board.FULL_SIZE
        self.board = [[None for j in range(0, Board.ROW_SIZE)]
                      for i in range(0, Board.COLUMN_SIZE)]
        for i in range(0, Board.COLUMN_SIZE):
            for j in range(0, Board.ROW_SIZE):
                figure_letter = board_position[i * Board.COLUMN_SIZE + j]
                if figure_letter.isupper():
                    side = Side.WHITE
                    figure_letter = figure_letter.lower()
                else:
                    side = Side.BLACK
                if figure_letter == 'k':
                    figure_type = FigureType.KING
                elif figure_letter == 'q':
                    figure_type = FigureType.QUEEN
                elif figure_letter == 'b':
                    figure_type = FigureType.BISHOP
                elif figure_letter == 'n':
                    figure_type = FigureType.KNIGHT
                elif figure_letter == 'r':
                    figure_type = FigureType.ROOK
                elif figure_letter == 'p':
                    figure_type = FigureType.PAWN
                else:
                    continue
                self.board[j][i] = Figure(figure_type, side, Vector2d(j, i))
