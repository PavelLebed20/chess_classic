###############################
# MODULE: Menu button class   #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 02/03/2019     #
###############################

from panda3d.core import LPoint3
import ChessRender.UIPrimitives.object_manage as om
from direct.gui.OnscreenText import OnscreenText

OBJECT_I = 0
BUTTON_I = 1
TEXT_I = 2
STATE_I = 3

BUTTON_SCALE_X = 15
BUTTON_SCALE_Y = 5

def loadButtons(buttons, state):
    if buttons is None:
        return None
    button_arr = []
    key = 0
    for b in buttons:
        textObject = OnscreenText(text=b.title, pos=b.real_position/BUTTON_SCALE_X,
                                  scale=om.TEXT_SCALE)
        obj = om.loadObject("ChessRender/data/button.png", b.real_position,
                         scale_x=BUTTON_SCALE_X, scale_z=BUTTON_SCALE_Y)
        button_arr.append([obj, b, textObject, state])
        button_arr[key][OBJECT_I].setTag("button_tag", str(key))
        key += 1
    return button_arr

class Button:

    def __init__(self, position, obtainer_func=None, title="test_start", size=None):
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
        self.real_position = LPoint3(position.x, position.y, 0)
        self.size = size
