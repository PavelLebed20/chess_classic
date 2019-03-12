###################################
# MODULE: Menu text field class   #
# AUTHOR: Lebed' Pavel            #
# LAST UPDATE: 02/03/2019         #
###################################


class TextField:
    def __init__(self, title, position, size):
        """
        Initialize text field function
        :param title: text field title
        :param position: screen position
        :param size: screen size
        """
        self.title = title
        self.position = position
        self.size = size
