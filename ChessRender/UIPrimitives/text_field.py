###################################
# MODULE: Menu text field class   #
# AUTHOR: Lebed' Pavel            #
# LAST UPDATE: 02/03/2019         #
###################################
from panda3d.core import LPoint3
import ChessRender.UIPrimitives.object_manage as om
from direct.gui.OnscreenText import OnscreenText
from Vector2d.Vector2d import Move, Vector2d

OBJECT_I = 0
TEXT_FIELD_I = 1
TEXT_I = 2
STATE_I = 3
TEXT_PRINT_I = 4

TEXT_FIELD_SCALE_X = 15
MINI_SCALE_X = 10
TEXT_FIELD_SCALE_Y = 2

def loadTextField(text_fields, state):
    if text_fields is None:
        return None
    text_field_arr = []
    key = 0
    for b in text_fields:
        textObject = OnscreenText(text=b.title, pos=b.title_position / TEXT_FIELD_SCALE_X,
                                  scale=om.TEXT_SCALE)
        textPrint = OnscreenText(text=b.text, pos=b.text_position / TEXT_FIELD_SCALE_X,
                                  scale=om.TEXT_SCALE)
        obj = om.loadObject("ChessRender/data/text_field_light.png", b.real_position,
                         scale_x=b.size.x, scale_z=b.size.y)
        text_field_arr.append([obj, b, textObject, state, textPrint])
        text_field_arr[key][OBJECT_I].setTag("text_field_tag", str(key))
        key += 1
    return text_field_arr

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
        if (c >= 'a' and c <='z') or (c >= 'A' and c <='Z') or (c >= '0' and c <='9'):
            if len(self.text) < self.max_legth:
                self.text += c
                return 1
        return 0
    def __init__(self, position, title = "Test:", size=Vector2d(TEXT_FIELD_SCALE_X, TEXT_FIELD_SCALE_Y),
                 max_length=15):
        """
        Initialize text field function
        :param title: text field title
        :param position: screen position
        :param size: screen size
        """
        self.title = title
        self.position = position
        self.real_position = LPoint3(position.x, position.y, 0)
        self.title_position = LPoint3(position.x, position.y + 1.5, 0)
        self.text_position = LPoint3(position.x, position.y, 0)
        self.size = size

        self.text = ""
        self.max_legth = max_length
