###############################
# MODULE: Menu button class   #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 02/03/2019     #
###############################


class Button:

    def __init__(self, obtainer_func, title, position, size):
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
        self.size = size
