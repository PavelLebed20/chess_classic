###############################
# MODULE: Chess render class  #
# AUTHOR: Lebed' Pavel        #
# LAST UPDATE: 03/03/2019     #
###############################
import copy

from direct.showbase.ShowBase import ShowBase

from direct.gui.OnscreenText import OnscreenText
from panda3d.core import WindowProperties

from panda3d.core import LPoint3, LVector3, BitMask32
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import GeomNode
from direct.task.Task import Task

from Vector2d.Vector2d import Move, Vector2d

from ChessBoard.chess_figure import Side
import ChessRender.UIPrimitives.object_manage as om
import ChessRender.UIPrimitives.text_field as tf
import ChessRender.UIPrimitives.button as bu
import ChessRender.obtain_functions as of
from ChessRender.UIPrimitives.object_manage import RenderState
from ChessRender.UIPrimitives.room import room

WIDTH = 480
HEIGHT = 480




def PointAtZ(y, point, vec):
    if vec.getY() != 0:
        return point + vec * ((y - point.getY()) / vec.getY())
    return point


class Render(ShowBase):

    def __init__(self):
        """
        Initialize render function
        """
        ShowBase.__init__(self)
        self.disableMouse()

        props = WindowProperties()
        props.clearSize()
        props.setSize(WIDTH, HEIGHT)
        props.setTitle('Chess Classic')
        self.win.requestProperties(props)

        self.init_ray()

        taskMgr.add(self.mouseTask, 'mouseTask')
        self.accept("mouse1", self.mouse_press)
        self.accept("mouse1-up", self.mouse_release)

        self.buttonThrowers[0].node().setKeystrokeEvent('keystroke')
        self.accept("keystroke", self.key_print)

        self.chess_run_func = None
        # picked figure info

        self.state = RenderState.MENU
        self.need_init = True
        self.room = room()
        #### - picked figure info
        self.picked_figure_last_pos = None
        self.picked_figue = None

        #### - game objects
        self.chess_board = None
        self.figues_tag = None
        self.figues_pos = None
        self.current_figure = None
        self.CENTER_X = 3.5
        self.CENTER_Y = 3.5
        self.STEP_X = 3
        self.STEP_Y = -3

        #### - buttons objects
        self.button_arr = []
        self.current_button = None

        #### - text_fields objects
        self.text_field_arr = []
        self.current_text_field = None

        self.objMngr = om.ObjectMngr()

    def posOfIndex(self, i, j):
        return LPoint3((i - self.CENTER_X) * self.STEP_X, (j - self.CENTER_Y) * self.STEP_Y, 0)

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
        f_tag = []
        f_pos = dict()
        key = 0
        self.board_info = str_board

        for i in range(0, 8):
            for j in range(0, 8):
                if str_board[i + j * 8] != ".":
                    obj = self.objMngr.load_figure(str_board[i + j * 8], self.posOfIndex(i, j))
                    f_tag.append(obj)
                    f_pos[self.posOfIndex(i, j)] = obj
                    f_tag[key].setTag("figue_tag", str(key))
                    key += 1
        return f_tag, f_pos

    def initLines(self):
        lines_h = []
        lines_v = []
        for i in range(0, 8):
            c1 = OnscreenText(text=chr(ord("A")+i), pos =LPoint3((i-3.5)/8, -0.58, 0), scale=0.09)
            c2 = OnscreenText(text=chr(ord("1")+i), pos =LPoint3(-0.55, (i-3.5)/8, 0), scale=0.09)
            c1.reparentTo(self.chess_board)
            c2.reparentTo(self.chess_board)
            lines_h.append(c1)
            lines_v.append(c2)
        for i in range(0, 8):
            c1 = OnscreenText(text=chr(ord("A")+i), pos =LPoint3((i-3.5)/8, -0.58, 0), scale=0.09)
            c2 = OnscreenText(text=chr(ord("1")+i), pos =LPoint3(-0.55, (i-3.5)/8, 0), scale=0.09)
            c1.reparentTo(self.chess_board)
            c2.reparentTo(self.chess_board)
            c1.setHpr(0, 0, 180)
            c2.setHpr(0, 0, 180)
            lines_h.append(c1)
            lines_v.append(c2)

        return lines_v, lines_h

    def updatePosition(self, str_board):
        """
        Update of figues on the board (visual interpretation)
        :param str_board: chess board in string format
        :return: None.
        """
        before_figures = dict()
        after_figures = dict()
        buffer = dict()

        for i in range(0, 8):
            for j in range(0, 8):
                if str_board[i + j * 8] != self.board_info[i + j * 8]:
                    if str_board[i + j * 8] != '.':
                        after_figures[self.posOfIndex(i, j)] = str_board[i + j * 8]
                    if self.board_info[i + j * 8] != '.':
                        before_figures[self.posOfIndex(i, j)] = self.board_info[i + j * 8]

        #### - change positions of figues
        for b in before_figures.keys():
            fig = self.figues_pos.pop(b)
            is_dead = True
            for a in after_figures.keys():
                if before_figures[b] == after_figures[a]:
                    buffer[a] = fig
                    after_figures.pop(a)
                    fig.setPos(x=a.getX(),y=om.DEPTH, z=a.getY())
                    is_dead = False
                    break
            if is_dead:
                if self.picked_figue is fig:
                    self.picked_figue = None
                ind = self.figues_tag.index(fig)
                self.figues_tag[ind] = None
                fig.removeNode()

        self.figues_pos.update(buffer)
        self.board_info = str_board

    def get_position(self, x, y):
        ####  - calculate position
        i = int(x / self.STEP_X + self.CENTER_X + 0.5)
        j = int(y / self.STEP_Y + self.CENTER_Y + 0.5)
        return i, j


    def set_menu_state(self, buttons=None, text_fields=None, text_fields_obtainer_func=None):
        """
        Set render state to menu mode
        :param buttons: array buttons (see. UIPrimitives.button)
        :param text_fields: text fields array (see. TO DO)
        :param text_fields_obtainer_func: text fields result obtainer
        :return: NONE.
        """
        self.need_init = False
        if not self.button_arr:
            self.button_arr = self.objMngr.loadButtons(buttons=buttons, state=self.state)

        if not self.text_field_arr:
            self.text_field_arr = self.objMngr.loadTextField(text_fields=text_fields, state=self.state)

    def set_game_state(self, chess_board_str=None, chess_board_obtainer_func=None,
                       buttons=None, text_fields=None, text_fields_obtainer_func=None, side=Side.WHITE):
        """
        Set render state to game mode
        :param chess_board: chess board class (see ChessBoard.Board)
        :param chess_board_obtainer_func: chess move result obtainer function
        :param buttons: array buttons (see. UIPrimitives.button)
        :param text_fields: text fields array (see. TO DO)
        :param text_fields_obtainer_func: text fields result obtainer
        :return: NONE.
        """
        self.need_init = False

        if self.chess_board is None:
            self.chess_board = self.objMngr.loadObject(om.RenderObject.BOARD,
                                                       scale_x=abs(self.STEP_X*8.65), scale_z=abs(self.STEP_Y*8.65), depth=om.DEPTH+5, transparency=False)
            self.lines_v, self.lines_h = self.initLines()

        if self.figues_tag is None:
            self.figues_tag, self.figues_pos = self.initPosition(chess_board_str)

        self.updatePosition(chess_board_str)
        self.chess_run_func = chess_board_obtainer_func

        if side is Side.WHITE:
            self.camera.setHpr(0, 0, 0)
            for fgr in self.figues_tag:
                if fgr is not None:
                    fgr.setHpr(0, 0, 0)
        else:
            self.camera.setHpr(0, 0, 180)
            for fgr in self.figues_tag:
                if fgr is not None:
                    fgr.setHpr(0, 0, 180)

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
            if self.picked_figue != None:
                mpos = self.mouseWatcherNode.getMouse()
                self.pickerRay.setFromLens(self.camNode, mpos.getX(), mpos.getY())
                nearPoint = render.getRelativePoint(camera, self.pickerRay.getOrigin())
                nearVec = render.getRelativeVector(camera, self.pickerRay.getDirection())

                self.picked_figue.setPos(PointAtZ(om.DEPTH-0, nearPoint, nearVec))
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
                self.picked_figue = self.figues_tag[int(pickedObj)]
                ####  - calculate position
                self.picked_figure_render_last_pos = self.picked_figue.getPos()
                i, j = self.get_position(self.picked_figure_render_last_pos.getX(), self.picked_figure_render_last_pos.getZ())
                self.picked_figure_last_pos = Vector2d(i, j)

            pickedObj = self.myHandler.getEntry(0).getIntoNodePath().findNetTag("button_tag").getTag("button_tag")
            if pickedObj != '':
                self.current_button = self.button_arr[int(pickedObj)]

            pickedObj = self.myHandler.getEntry(0).getIntoNodePath().findNetTag("text_field_tag").getTag("text_field_tag")
            if pickedObj != '':
                self.current_text_field = self.text_field_arr[int(pickedObj)]

    def mouse_release(self):
        ####  - figues action
        if self.picked_figue is not None:
            pos = self.picked_figue.getPos()
            i, j = self.get_position(pos.getX(), pos.getZ())
            pos = self.posOfIndex(i, j)

            # run engine function
            if self.picked_figure_last_pos is not None:
                move = Move(self.picked_figure_last_pos, Vector2d(i, j))

                self.picked_figure_last_pos = None
                if self.chess_run_func is not None:
                    self.picked_figue.setPos(self.picked_figure_render_last_pos.getX(), om.DEPTH, self.picked_figure_render_last_pos.getZ())
                    self.picked_figue = None
                    self.chess_run_func(move)

        ####  - buttons action
        if self.current_button is not None:
            self.current_button[bu.BUTTON_I].obtainer_func(self)
            self.current_button = None

    def key_print(self, keyname):
        if self.current_text_field is not None:
            kascad = self.current_text_field
            kascad[tf.TEXT_FIELD_I].add_text(keyname)
            kascad[tf.TEXT_PRINT_I].text = kascad[tf.TEXT_FIELD_I].text

    def step(self):
        """
        Render scene function
        :return: NONE.
        """
        if self.appRunner is None or self.appRunner.dummy or \
           (self.appRunner.interactiveConsole and not self.appRunner.initialAppImport):
            self.taskMgr.step()
