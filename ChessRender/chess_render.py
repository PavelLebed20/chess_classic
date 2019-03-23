###############################
# MODULE: Chess render class  #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 03/03/2019     #
###############################

from enum import Enum
from direct.showbase.ShowBase import ShowBase

from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import WindowProperties
from panda3d.core import TransparencyAttrib

from panda3d.core import LPoint3, LVector3, BitMask32
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import GeomNode
from direct.task.Task import Task
import sys

class RenderState(Enum):
    INPUT = 0,
    MENU = 1,
    GAME = 2

WIDTH = 480
HEIGHT = 480

CENTER_X = 3.5
CENTER_Y = 3.5
STEP_X = 3.7
STEP_Y = -3.7
DEPTH = 55

def trLiter(simbol):
    if (simbol.isupper()):
        return "w" + simbol
    else:
        return "b" + simbol.upper()

def posOfIndex(i, j):
    return LPoint3((i-CENTER_X)*STEP_X, (j-CENTER_Y)*STEP_Y, 0)

def loadObject(text=None, pos=LPoint3(0, 0), depth=DEPTH, scale=3,
               transparency=True):
    obj = loader.loadModel("ChessRender/data/chess_figues/plane")
    obj.reparentTo(camera)

    texture = loader.loadTexture(text)
    obj.set_texture(texture, 1)

    obj.setPos(pos.getX(), depth, pos.getY())
    obj.set_scale(scale)

    obj.setBin("unsorted", 0)
    obj.setDepthTest(False)

    if transparency:
        obj.setTransparency(TransparencyAttrib.MAlpha)
    return obj


def initPosition(str_board ="rnbqkbnr" \
                            "pppppppp" \
                            "........" \
                            "........" \
                            "........" \
                            "........" \
                            "PPPPPPPP" \
                            "RNBQKBNR"):
    figues = []
    key = 0

    for i in range(0, 8):
        for j in range(0, 8):
            if str_board[i + j*8] != ".":
                figues.append(
                    loadObject("ChessRender/data/chess_figues/" + trLiter(str_board[i + j*8]) + ".png", posOfIndex(i, j)))
                figues[key].setTag("figue_tag", str(key))
                key += 1
    return figues

class Render(ShowBase):

    def __init__(self):
        """
        Initialize render function
        """
        ShowBase.__init__(self)

        props = WindowProperties()
        props.clearSize()
        props.setSize(WIDTH, HEIGHT)
        self.win.requestProperties(props)

        self.init_ray()

        self.mouseTask = taskMgr.add(self.mouseTask, 'mouseTask')

        self.chess_board = loadObject("ChessRender/data/chess_board.png", scale=29.5, transparency=False)
        self.figues = initPosition()
        self.current_figue = None

        self.accept("mouse1", self.mouse_press)
        self.accept("mouse1-up", self.mouse_release)

        print("Render initialize")

    def set_menu_state(self, buttons, text_fields, text_fields_obtainer_func):
        """
        Set render state to menu mode
        :param buttons: array buttons (see. UIPrimitives.button)
        :param text_fields: text fields array (see. TO DO)
        :param text_fields_obtainer_func: text fields result obtainer
        :return: NONE.
        """
        print("Set state to input")

    def set_game_state(self, chess_board, chess_board_obtainer_func,
                       buttons, text_fields, text_fields_obtainer_func):
        """
        Set render state to game mode
        :param chess_board: chess board class (see ChessBoard.Board)
        :param chess_board_obtainer_func: chess move result obtainer function
        :param buttons: array buttons (see. UIPrimitives.button)
        :param text_fields: text fields array (see. TO DO)
        :param text_fields_obtainer_func: text fields result obtainer
        :return: NONE.
        """
        print("Set state to game")

    def init_ray(self):
        self.myTraverser = CollisionTraverser()
        self.myHandler = CollisionHandlerQueue()
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = self.camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.myTraverser.addCollider(self.pickerNP, self.myHandler)

    def mouseTask(self, task):
        if self.mouseWatcherNode.hasMouse():
            if self.current_figue != None:
                mpos = self.mouseWatcherNode.getMouse()
                self.current_figue.setPos(mpos.getX()*14.5, DEPTH, mpos.getY()*14.5)
        return Task.cont

    def mouse_press(self):
        mpos = self.mouseWatcherNode.getMouse()
        self.pickerRay.setFromLens(self.camNode, mpos.getX(), mpos.getY())
        pickedObj = None
        self.myTraverser.traverse(render)
        if self.myHandler.getNumEntries() > 0:
            self.myHandler.sortEntries()
            pickedObj = self.myHandler.getEntry(0).getIntoNodePath().findNetTag("figue_tag").getTag("figue_tag")
            if pickedObj != '':
                self.current_figue = self.figues[int(pickedObj)]

    def mouse_release(self):
        if self.current_figue != None:
            pos = self.current_figue.getPos()
            i = int((pos.getX() + 15)*8/30)
            j = int((15 - pos.getZ())*8/30)
            pos = posOfIndex(i, j)
            self.current_figue.setPos(pos.getX(), DEPTH, pos.getY())
            self.current_figue = None

    def step(self):
        """
        Render scene function
        :return: NONE.
        """
        self.taskMgr.step()
