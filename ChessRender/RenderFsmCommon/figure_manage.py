###############################
# MODULE: Object settings     #
# AUTHOR: Yangildin Ivan      #
# LAST UPDATE: 08/04/2019     #
###############################
import copy

from enum import Enum, IntEnum
from direct.gui.OnscreenText import TransparencyAttrib

BLACK = (0.8, 0.3, 0.5, 1)
WHITE = (1, 1, 1, 1)

class RenderState(Enum):
    DEFAULT = -1
    INPUT   = 0
    MENU    = 1
    GAME    = 2


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

    PLANE = 12

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


class FigureMngr:

    def __init__(self, blackside_pack, whiteside_pack):
        self.data_path = "ChessRender/data/"
        self.whiteside_pack_name = self.data_path + "chess_figures/" + whiteside_pack + "/"
        self.blackside_pack_name = self.data_path + "chess_figures/"  + blackside_pack + "/"

        self.textures = dict({
            RenderObject.BLACK_KING   : loader.loadTexture(self.blackside_pack_name + "bK.png"),
            RenderObject.BLACK_QUEEN  : loader.loadTexture(self.blackside_pack_name + "bQ.png"),
            RenderObject.BLACK_BISHOP : loader.loadTexture(self.blackside_pack_name + "bB.png"),
            RenderObject.BLACK_KNIGHT : loader.loadTexture(self.blackside_pack_name + "bN.png"),
            RenderObject.BLACK_ROOK   : loader.loadTexture(self.blackside_pack_name + "bR.png"),
            RenderObject.BLACK_PAWN   : loader.loadTexture(self.blackside_pack_name + "bP.png"),

            RenderObject.WHITE_KING   : loader.loadTexture(self.whiteside_pack_name + "wK.png"),
            RenderObject.WHITE_QUEEN  : loader.loadTexture(self.whiteside_pack_name + "wQ.png"),
            RenderObject.WHITE_BISHOP : loader.loadTexture(self.whiteside_pack_name + "wB.png"),
            RenderObject.WHITE_KNIGHT : loader.loadTexture(self.whiteside_pack_name + "wN.png"),
            RenderObject.WHITE_ROOK   : loader.loadTexture(self.whiteside_pack_name + "wR.png"),
            RenderObject.WHITE_PAWN   : loader.loadTexture(self.whiteside_pack_name + "wP.png"),
        })

        self.modeles = dict({
            RenderObject.WHITE_KING: loader.loadModel(self.whiteside_pack_name + "king.egg"),
            RenderObject.WHITE_QUEEN: loader.loadModel(self.whiteside_pack_name + "queen.egg"),
            RenderObject.WHITE_BISHOP: loader.loadModel(self.whiteside_pack_name + "bishop.egg"),
            RenderObject.WHITE_KNIGHT: loader.loadModel(self.whiteside_pack_name + "knight.egg"),
            RenderObject.WHITE_ROOK: loader.loadModel(self.whiteside_pack_name + "rook.egg"),
            RenderObject.WHITE_PAWN: loader.loadModel(self.whiteside_pack_name + "pawn.egg"),

            RenderObject.BLACK_KING: loader.loadModel(self.blackside_pack_name + "king.egg"),
            RenderObject.BLACK_QUEEN: loader.loadModel(self.blackside_pack_name + "queen.egg"),
            RenderObject.BLACK_BISHOP: loader.loadModel(self.blackside_pack_name + "bishop.egg"),
            RenderObject.BLACK_KNIGHT: loader.loadModel(self.blackside_pack_name + "knight.egg"),
            RenderObject.BLACK_ROOK: loader.loadModel(self.blackside_pack_name + "rook.egg"),
            RenderObject.BLACK_PAWN: loader.loadModel(self.blackside_pack_name + "pawn.egg"),

            RenderObject.PLANE: loader.loadModel(self.data_path + "plane.egg")
        })


    def load_figure_model(self, figure_latter):
        render_obj = figure_as_render_object(figure_latter)
        obj =  copy.deepcopy(self.modeles[render_obj])
        if RenderObject.BLACK_KING <= RenderObject(render_obj) <= RenderObject.BLACK_PAWN:
            obj.setColor(BLACK)
        else:
            obj.setColor(WHITE)
        return obj

    def load_figure_model_2D(self, figure_latter):
        render_obj = figure_as_render_object(figure_latter)
        return self.load_plane_object(render_obj)

    def load_plane_object(self, render_object):
        obj = copy.deepcopy(self.modeles[RenderObject.PLANE])

        texture = copy.deepcopy(self.textures[render_object])
        obj.set_texture(texture)

        obj.setTransparency(TransparencyAttrib.MAlpha)

        return obj

    def load_skybox_white_side(self):
        return loader.loadModel(self.whiteside_pack_name + "cubemap.bam")

    def load_skybox_black_side(self):
        return loader.loadModel(self.blackside_pack_name + "cubemap.bam")
