###################################
# MODULE: Menu text field class   #
# AUTHOR: Lebed' Pavel            #
# LAST UPDATE: 02/03/2019         #
###################################
from panda3d.core import LPoint3


class TextField:
    def add_text(self, c):
        """
        Add new char to text
        :param c: new char
        """
        if c == '\b':
            if len(self.text) > 0:
                self.text = self.text[0:len(self.text)-1]
                return -1
            return 0
        if (c >= 'a' and c <='z') or (c >= 'A' and c <='Z') or (c >= '1' and c <='9'):
            if len(self.text) < self.max_legth:
                self.text += c
                return 1
        return 0
    def __init__(self, position, obtainer_func=None, title = "Test:", size=None):
        """
        Initialize text field function
        :param title: text field title
        :param position: screen position
        :param size: screen size
        """
        self.obtainer_func = obtainer_func
        self.title = title
        self.position = position
        self.real_position = LPoint3(position.x, position.y, 0)
        self.title_position = LPoint3(position.x, position.y + 1.5, 0)
        self.text_position = LPoint3(position.x, position.y, 0)
        self.size = size

        self.text = ""
        self.max_legth = 15
