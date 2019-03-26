###############################
# MODULE: Menu button class   #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 02/03/2019     #
###############################
from panda3d.core import LPoint3

class Button:

    def __init__(self, obtainer_func=None, title="test_start", position=None, size=None):
        """
        Initialize button function
        :param obtainer_func: obtain click func (Func)
        :param title: button tittle (Str)
        :param position: screen position (Vector2d)
        :param size: screen size (Vector2d)
        """
        self.obtainer_func = obtainer_func
        self.title = title
        self.position = position
        self.real_position = LPoint3(0, 0)
        self.size = size
