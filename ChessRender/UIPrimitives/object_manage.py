###############################
# MODULE: Object settings     #
# AUTHOR: Yangildin Ivan      #
# LAST UPDATE: 08/04/2019     #
###############################
from panda3d.core import LPoint3
from panda3d.core import TransparencyAttrib

TEXT_SCALE = 0.07
FIGUE_SCALE = 3

DEPTH = 55

def loadObject(text=None, pos=LPoint3(0, 0), depth=DEPTH, scale_x=FIGUE_SCALE,
               scale_z=FIGUE_SCALE, transparency=True):
    obj = loader.loadModel("ChessRender/data/chess_figues/plane")
    obj.reparentTo(camera)

    texture = loader.loadTexture(text)
    obj.set_texture(texture)

    obj.setPos(pos.getX(), depth, pos.getY())
    obj.setSx(scale_x)
    obj.setSz(scale_z)

    obj.setBin("unsorted", 0)
    obj.setDepthTest(False)

    if transparency:
        obj.setTransparency(TransparencyAttrib.MAlpha)
    return obj
