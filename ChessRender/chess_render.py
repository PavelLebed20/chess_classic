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

from ChessBoard.chess_board import Board
from Vector2d.Vector2d import Move, Vector2d


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

        self.chess_run_func = None
        self.last_pos = None

        self.chess_board = loadObject("ChessRender/data/chess_board.png", scale=29.5, transparency=False)
        self.figues = self.initPosition()

        self.current_figue = None

        self.accept("mouse1", self.mouse_press)
        self.accept("mouse1-up", self.mouse_release)

        self.set_game_state(Board.DEFAULT_BOARD_POSITION, None, None, None, None)


    def initPosition(self, str_board="rnbqkbnr" \
                               "pppppppp" \
                               "........" \
                               "........" \
                               "........" \
                               "........" \
                               "PPPPPPPP" \
                               "RNBQKBNR"):
        """
        Creation of figues on the board (visual interpretation)
        :param str_board: chess board in string format
        :return: figues: array of objects.
        """
        figues = []
        key = 0
        self.board_info = str_board

        for i in range(0, 8):
            for j in range(0, 8):
                if str_board[i + j * 8] != ".":
                    figues.append(
                        loadObject("ChessRender/data/chess_figues/" + trLiter(str_board[i + j * 8]) + ".png",
                                   posOfIndex(i, j)))
                    figues[key].setTag("figue_tag", str(key))
                    key += 1
        return figues

    def updatePosition(self, str_board):
        """
        Update of figues on the board (visual interpretation)
        :param str_board: chess board in string format
        :return: None.
        """
        before_figues = list()
        after_figues = list()

        for i in range(0, 8):
            for j in range(0, 8):
                if str_board[i + j * 8] != self.board_info[i + j * 8]:
                    if str_board[i + j * 8] != '.':
                        after_figues.append([str_board[i + j * 8], i, j])
                    if self.board_info[i + j * 8] != '.':
                        before_figues.append([self.board_info[i + j * 8], i, j, self.pick_figue_num(i,j)])

        #### - change positions of figues
        for a in before_figues:
            for b in after_figues:
                if a[0] == b[0]:
                    figue = self.pick_figue(a[1],a[2])
                    pos = posOfIndex(b[1], b[2])
                    
                    if figue != None:
                        figue.setPos(pos.getX(), DEPTH, pos.getY())
                        a[0] = None
                        b[0] = None

        #### - eat figues
        for a in before_figues:
            if a[0] != None :
                if a[3] != None:
                    self.figues[int(a[3])].removeNode()
                    self.figues[int(a[3])] = None

        #### - create figues
        for b in after_figues:
            if b[0] != None :
                for key in range(0, 32):
                    self.figues[key] = loadObject("ChessRender/data/chess_figues/" + b[0] + ".png",
                                            posOfIndex(b[1], b[2]))
                    self.figues[key].setTag("figue_tag", str(key))

        self.board_info = str_board


    def pick_figue_num(self, i, j):
        mpos = posOfIndex(i, j)
        self.pickerRay.setFromLens(self.camNode, mpos.getX()/14.5, mpos.getY()/14.5)
        self.myTraverser.traverse(render)
        if self.myHandler.getNumEntries() > 0:
            self.myHandler.sortEntries()
            pickedObj = self.myHandler.getEntry(0).getIntoNodePath().findNetTag("figue_tag").getTag("figue_tag")
            return pickedObj
        return None

    def pick_figue(self, i, j):
        pickedObj = self.pick_figue_num(i, j)
        if pickedObj != None and pickedObj != '':
            return self.figues[int(pickedObj)]
        return None

    def get_position(self, x, y):
        ####  - calculate position
        i = int((x + 15) * 8 / 30)
        j = int((15 - y) * 8 / 30)
        return i,j


    def set_menu_state(self, buttons, text_fields, text_fields_obtainer_func):
        """
        Set render state to menu mode
        :param buttons: array buttons (see. UIPrimitives.button)
        :param text_fields: text fields array (see. TO DO)
        :param text_fields_obtainer_func: text fields result obtainer
        :return: NONE.
        """
        print("Set state to input")

    def set_game_state(self, chess_board_str, chess_board_obtainer_func,
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

        self.updatePosition(chess_board_str)
        self.chess_run_func = chess_board_obtainer_func


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
                ####  - calculate position
                self.render_last_pos = self.current_figue.getPos()
                i, j = self.get_position(self.render_last_pos.getX(), self.render_last_pos.getZ())
                self.last_pos = Vector2d(i, j)

    def mouse_release(self):
        if self.current_figue != None:
            pos = self.current_figue.getPos()
            i, j = self.get_position(pos.getX(), pos.getZ())
            pos = posOfIndex(i, j)

            # run engine function
            if self.last_pos is not None:
                move = Move(self.last_pos, Vector2d(i, j))

                self.last_pos = None
                if self.chess_run_func is not None:
                    self.current_figue.setPos(self.render_last_pos.getX(), DEPTH, self.render_last_pos.getZ())
                    self.current_figue = None
                    self.chess_run_func(move)



    def step(self):
        """
        Render scene function
        :return: NONE.
        """
        self.taskMgr.step()
