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

import ChessRender.UIPrimitives.object_manage as om
import ChessRender.UIPrimitives.text_field as tf
import ChessRender.UIPrimitives.button as bu
import ChessRender.obtain_functions as of
from ChessRender.UIPrimitives.object_manage import RenderState
from ChessRender.UIPrimitives.room import room

WIDTH = 480
HEIGHT = 480

CENTER_X = 3.5
CENTER_Y = 3.5
STEP_X = 3.7
STEP_Y = -3.7


def posOfIndex(i, j):
    return LPoint3((i-CENTER_X)*STEP_X, (j-CENTER_Y)*STEP_Y, 0)

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
        self.figues = None

        #### - buttons objects
        self.button_arr = []
        self.current_button = None

        #### - text_fields objects
        self.text_field_arr = []
        self.current_text_field = None

        self.objMngr = om.ObjectMngr()

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
                        self.objMngr.load_figure(str_board[i + j * 8], posOfIndex(i, j)))
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

                    if figue is not None:
                        figue.setPos(pos.getX(), om.DEPTH, pos.getY())
                        a[0] = None
                        b[0] = None

        #### - eat figues
        for a in before_figues:
            if a[0] is not None :
                if a[3] != None:
                    self.figues[int(a[3])].removeNode()
                    self.figues[int(a[3])] = None

        #### - create figues
        for b in after_figues:
            if b[0] is not None :
                for key in range(0, 32):
                    self.figues[key] = self.objMngr.loadObject(b[0], posOfIndex(b[1], b[2]))
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
                       buttons=None, text_fields=None, text_fields_obtainer_func=None):
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
                                                       scale_x=32, scale_z=32, depth=om.DEPTH+5, transparency=False)
        if self.figues is None:
            self.figues = self.initPosition(chess_board_str)

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
            if self.picked_figue != None:
                mpos = self.mouseWatcherNode.getMouse()
                self.picked_figue.setPos(mpos.getX() * 14.5, om.DEPTH, mpos.getY() * 14.5)
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
                self.picked_figue = self.figues[int(pickedObj)]
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
            pos = posOfIndex(i, j)

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
