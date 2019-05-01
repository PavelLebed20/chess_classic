###############################
# MODULE: Object settings     #
# AUTHOR: Yangildin Ivan      #
# LAST UPDATE: 08/04/2019     #
###############################
import copy

from panda3d.core import LPoint3
from panda3d.core import TransparencyAttrib
from enum import Enum, IntEnum
from direct.gui.OnscreenText import OnscreenText

from ChessRender.UIPrimitives.button import BUTTON_SCALE_X, BUTTON_SCALE_Y, OBJECT_I
from ChessRender.UIPrimitives.text_field import TEXT_FIELD_SCALE_X


class RenderState(Enum):
    DEFAULT = -1
    INPUT   = 0
    MENU    = 1
    GAME    = 2

TEXT_SCALE = 0.07
FIGUE_SCALE = 3

DEPTH = 55


class RenderModels(Enum):
    PLANE = 0


class RenderObject(IntEnum):
    BLACK_KING   = 0
    BLACK_QUEEN  = 1
    BLACK_BISHOP = 2
    BLACK_KNIGHT = 3
    BLACK_ROOK   = 4
    BLACK_PAWN   = 5

    WHITE_KING =   6
    WHITE_QUEEN =  7
    WHITE_BISHOP = 8
    WHITE_KNIGHT = 9
    WHITE_ROOK =  10
    WHITE_PAWN =  11

    BOARD       = 18

    BUTTON      = 19
    TEXT_FIELD  = 20
    MENU        = 21

def figure_as_render_object(figure_latter):
    res = 0
    lower = figure_latter.lower()

    if figure_latter.isupper():
        res += 6

    if lower == 'k':
        res += 0
    if lower == 'q':
        res += 1
    if lower == 'b':
        res += 2
    if lower == 'n':
        res += 3
    if lower == 'r':
        res += 4
    if lower == 'p':
        res += 5

    return RenderObject(res)


class ObjectMngr:

    def __init__(self):
        self.textures = dict({
            RenderObject.BLACK_KING   : loader.loadTexture("ChessRender/data/chess_figures/bK.png"),
            RenderObject.BLACK_QUEEN  : loader.loadTexture("ChessRender/data/chess_figures/bQ.png"),
            RenderObject.BLACK_BISHOP : loader.loadTexture("ChessRender/data/chess_figures/bB.png"),
            RenderObject.BLACK_KNIGHT : loader.loadTexture("ChessRender/data/chess_figures/bN.png"),
            RenderObject.BLACK_ROOK   : loader.loadTexture("ChessRender/data/chess_figures/bR.png"),
            RenderObject.BLACK_PAWN   : loader.loadTexture("ChessRender/data/chess_figures/bP.png"),

            RenderObject.WHITE_KING   : loader.loadTexture("ChessRender/data/chess_figures/wK.png"),
            RenderObject.WHITE_QUEEN  : loader.loadTexture("ChessRender/data/chess_figures/wQ.png"),
            RenderObject.WHITE_BISHOP : loader.loadTexture("ChessRender/data/chess_figures/wB.png"),
            RenderObject.WHITE_KNIGHT : loader.loadTexture("ChessRender/data/chess_figures/wN.png"),
            RenderObject.WHITE_ROOK   : loader.loadTexture("ChessRender/data/chess_figures/wR.png"),
            RenderObject.WHITE_PAWN   : loader.loadTexture("ChessRender/data/chess_figures/wP.png"),

            RenderObject.BOARD        : loader.loadTexture("ChessRender/data/chess_board.png"),

            RenderObject.BUTTON       : loader.loadTexture("ChessRender/data/button.png"),
            RenderObject.TEXT_FIELD   : loader.loadTexture("ChessRender/data/text_field.png"),
        })

        self.modeles = dict({
            RenderObject.WHITE_KING: loader.loadModel("ChessRender/data/chess_figures/king.egg.pz"),
            RenderObject.WHITE_QUEEN: loader.loadModel("ChessRender/data/chess_figures/queen.egg.pz"),
            RenderObject.WHITE_BISHOP: loader.loadModel("ChessRender/data/chess_figures/bishop.egg.pz"),
            RenderObject.WHITE_KNIGHT: loader.loadModel("ChessRender/data/chess_figures/knight.egg.pz"),
            RenderObject.WHITE_ROOK: loader.loadModel("ChessRender/data/chess_figures/rook.egg.pz"),
            RenderObject.WHITE_PAWN: loader.loadModel("ChessRender/data/chess_figures/pawn.egg.pz"),

            RenderObject.BLACK_KING: loader.loadModel("ChessRender/data/chess_figures/king.egg.pz"),
            RenderObject.BLACK_QUEEN: loader.loadModel("ChessRender/data/chess_figures/queen.egg.pz"),
            RenderObject.BLACK_BISHOP: loader.loadModel("ChessRender/data/chess_figures/bishop.egg.pz"),
            RenderObject.BLACK_KNIGHT: loader.loadModel("ChessRender/data/chess_figures/knight.egg.pz"),
            RenderObject.BLACK_ROOK: loader.loadModel("ChessRender/data/chess_figures/rook.egg.pz"),
            RenderObject.BLACK_PAWN: loader.loadModel("ChessRender/data/chess_figures/pawn.egg.pz"),

            RenderModels.PLANE : loader.loadModel("ChessRender/data/chess_figures/plane")
        })

    def change_skin(self, filepath, figure_latter):
        render_obj = figure_as_render_object(figure_latter)
        try:
            new_texture = loader.loadTexture(filepath)
        except IOError:
            return

        if new_texture is None:
            return
        self.textures[render_obj] = new_texture



    def change_board(self, filepath):
        try:
            new_texture = loader.loadTexture(filepath)
        except IOError:
            return
        if new_texture is None:
            return
        self.textures[RenderObject.BOARD] = new_texture

    def load_figure_model(self, figure_latter):
        BLACK = (0.8, 0.3, 0.5, 1)
        WHITE = (1, 1, 1, 1)
        render_obj = figure_as_render_object(figure_latter)
        obj =  copy.deepcopy(self.modeles[render_obj])
        if RenderObject.BLACK_KING <= RenderObject(render_obj) <= RenderObject.BLACK_PAWN:
            obj.setColor(BLACK)
        else:
            obj.setColor(WHITE)
        return obj

    def loadObject(self, render_object, pos=LPoint3(0, 0), depth=DEPTH, scale_x=FIGUE_SCALE,
                   scale_z=FIGUE_SCALE, transparency=True):
        obj = copy.deepcopy(self.modeles[RenderModels.PLANE])

        texture = copy.deepcopy(self.textures[render_object])
        obj.set_texture(texture)

        obj.setPos(pos.getX(), depth, pos.getY())
        obj.setSx(scale_x)
        obj.setSz(scale_z)

        obj.setBin("unsorted", 0)
        obj.setDepthTest(False)

        obj.reparentTo(camera)

        if transparency:
            obj.setTransparency(TransparencyAttrib.MAlpha)
        return obj

    def loadButtons(self, buttons, state):
        if buttons is None:
            return None
        button_arr = []
        key = 0
        for b in buttons:
            textObject = OnscreenText(text=b.title, pos=b.real_position / BUTTON_SCALE_X,
                                      scale= TEXT_SCALE)
            obj = self.loadObject(RenderObject.BUTTON, b.real_position,
                                scale_x=BUTTON_SCALE_X, scale_z=BUTTON_SCALE_Y)
            button_arr.append([obj, b, textObject, state])
            button_arr[key][OBJECT_I].setTag("button_tag", str(key))
            key += 1
        return button_arr


    def loadTextField(self, text_fields, state):
        if text_fields is None:
            return None
        text_field_arr = []
        key = 0
        for b in text_fields:
            textObject = OnscreenText(text=b.title, pos=b.title_position / TEXT_FIELD_SCALE_X,
                                      scale=TEXT_SCALE)
            textPrint = OnscreenText(text=b.text, pos=b.text_position / TEXT_FIELD_SCALE_X,
                                     scale=TEXT_SCALE)
            obj = self.loadObject(RenderObject.TEXT_FIELD, b.real_position,
                                scale_x=b.size.x, scale_z=b.size.y)
            text_field_arr.append([obj, b, textObject, state, textPrint])
            text_field_arr[key][OBJECT_I].setTag("text_field_tag", str(key))
            key += 1
        return text_field_arr
