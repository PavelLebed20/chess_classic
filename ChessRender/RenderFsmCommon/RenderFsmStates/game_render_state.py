from enum import Enum

from direct.gui.OnscreenText import CollisionTraverser, CollisionHandlerQueue, CollisionNode, \
    CollisionRay
from direct.task import Task
from panda3d.core import BitMask32, LPoint3
from ChessRender.RenderFsmCommon.Camera.camera import Camera, Camera2D
from ChessRender.RenderFsmCommon.Lights.lights import Lights
from ChessRender.RenderFsmCommon.button_fsm import ButtonFsm
from ChessRender.RenderFsmCommon.screen_states import ScreenState
from ChessRender.RenderFsmCommon.figure_manage import FigureMngr
from Vector2d.Vector2d import Vector2d, Move

HIGHLIGHT = (0, 1, 1, 1)

class Dimension(Enum):
    _2D = 1
    _3D = 2

class FsmStateGameState(ScreenState):
    def __init__(self, render_fsm, whiteside_pack_name, blackside_pack_name):
        ScreenState.__init__(self)
        self.render_fsm_ref = render_fsm
        self.objMngr = FigureMngr(blackside_pack_name, whiteside_pack_name)

        self.dimension = Dimension._3D

        self.init_sky_sphere()
        self.squares = [None for i in range(64)]
        self.init_nodes_to_chsess_board()

        self.str_board = "rnbqkbnr" \
                         "pppppppp" \
                         "........" \
                         "........" \
                         "........" \
                         "........" \
                         "PPPPPPPP" \
                         "RNBQKBNR"

        self.figures = [None for i in range(64)]
        self.init_nodes_to_figures()

        self.camera_p = Camera(base.camera, base.camLens)
        base.disableMouse()
        # camera debug god mode
        #base.oobe()

        self.lights = Lights(base, self.render_fsm_ref.WIDTH, self.render_fsm_ref.HEIGHT)

        self.screen_atributes.buttons["but:Exit"] = ButtonFsm("Exit", (-0.8, 0, 0.8))
        self.screen_atributes.buttons["but:2D/3D"] = ButtonFsm("2D/3D", (0.8, 0, 0.8))
        self.initialize_button_links()

        self.init_ray()

        render_fsm.accept("mouse1", self.grab_piece)  # left-click grabs a piece
        render_fsm.accept("mouse1-up", self.release_piece)  # releasing places it

        render_fsm.accept("mouse2", self.middle_click)

        self.need_camera_update = False
        render_fsm.accept("mouse3", self.right_click)
        render_fsm.accept("mouse3-up", self.right_release)

        render_fsm.accept("wheel_up", self.wheel_up)
        render_fsm.accept("wheel_down", self.wheel_down)

        self.dragging = False
        self.dragging_figure_position = None
        self.hiSq = False


    def change_dimension(self):
        if self.dimension == Dimension._3D:
            self.dimension = Dimension._2D
            self.camera_p = Camera2D(base.camera, base.camLens)
        else:
            self.dimension = Dimension._3D
            self.camera_p = Camera(base.camera, base.camLens)
        self.update_board(self.str_board)

    def init_sky_sphere(self):
        self.skysphere = loader.loadModel("SkySphere.bam")
        self.skysphere.setBin('background', 1)
        self.skysphere.setDepthWrite(0)
        self.skysphere.reparentTo(render)
        self.skysphere.setPos(0, 0, 0)
        self.skysphere.setScale(20)

    def process_set_move_player(self):
        pass

    def clear_state(self):
        for figure in self.figures:
            if figure is not None:
                figure.removeNode()
        for square in self.squares:
            square.removeNode()
        self.skysphere.removeNode()

        self.lights.unset()

    def initialize_button_links(self):
        self.screen_atributes.buttons["but:Exit"].add_command(self.clear_state)
        self.screen_atributes.buttons["but:Exit"].add_link("fsm:MainMenu")
        self.screen_atributes.buttons["but:2D/3D"].add_command(self.change_dimension)


    def wheel_up(self):
        self.camera_p.update_on_mouse_wheel(3)

    def wheel_down(self):
        self.camera_p.update_on_mouse_wheel(-3)

    def middle_click(self):
        self.camera_p.set_default()

    def right_click(self):
        mouse_watcher = base.mouseWatcherNode
        self.camera_p.start_rotating(mouse_watcher.getMouseX(), mouse_watcher.getMouseY())
        self.need_camera_update = True

    def right_release(self):
        self.need_camera_update = False

    def grab_piece(self):
        # If a square is highlighted and it has a piece, set it to dragging
        # mode
        if self.hiSq is not False and self.figures[self.hiSq]:
            self.dragging = self.hiSq
            self.dragging_figure_position = Vector2d(self.hiSq % 8, self.hiSq // 8)
            self.hiSq = False

    def release_piece(self):
        # Letting go of a piece. If we are not on a square, return it to its original
        # position. Otherwise, swap it with the piece in the new square
        # Make sure we really are dragging something
        if self.dragging is not False:
            # We have let go of the piece, but we are not on a square
            if self.hiSq is False:
                self.figures[self.dragging].setPos(
                    self.SquarePos(self.dragging))
            if self.render_fsm_ref.process_set_move_player is not None:
                self.render_fsm_ref.process_set_move_player(Move(self.dragging_figure_position, Vector2d(self.hiSq % 8, self.hiSq // 8))
)

        # We are no longer dragging anything
        self.dragging = False

    def swap_figures(self, fr, to):
        temp = self.figures[fr]
        self.figures[fr] = self.figures[to]
        self.figures[to] = temp
        if self.figures[fr]:
            self.figures[fr].setPos(self.SquarePos(fr))
        if self.figures[to]:
            self.figures[to].setPos(self.SquarePos(to))

    def mouse_task(self):
        mouse_watcher = base.mouseWatcherNode
        if mouse_watcher.hasMouse() and self.need_camera_update:
            self.camera_p.update_pos(mouse_watcher.getMouseX(), mouse_watcher.getMouseY())

        # First, clear the current highlight
        if self.hiSq is not False:
            #self.squares[self.hiSq].setColor(self.SquareColor(self.hiSq))
            self.hiSq = False

        if base.mouseWatcherNode.hasMouse():
            # get the mouse position
            mpos = base.mouseWatcherNode.getMouse()
            # Set the position of the ray based on the mouse position
            self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())
            # If we are dragging something, set the position of the object
            # to be at the appropriate point over the plane of the board
            if self.dragging is not False:
                # Gets the point described by pickerRay.getOrigin(), which is relative to
                # camera, relative instead to render
                nearPoint = base.render.getRelativePoint(
                    camera, self.pickerRay.getOrigin())
                # Same thing with the direction of the ray
                nearVec = base.render.getRelativeVector(
                    base.camera, self.pickerRay.getDirection())
                self.figures[self.dragging].setPos(
                    self.PointAtZ(.5, nearPoint, nearVec))

            # Do the actual collision pass (Do it only on the squares for
            # efficiency purposes)
            self.myTraverser.traverse(self.squareRoot)
            if self.myHandler.getNumEntries() > 0:
                # if we have hit something, sort the hits so that the closest
                # is first, and highlight that node
                self.myHandler.sortEntries()
                i = int(self.myHandler.getEntry(0).getIntoNode().getTag('square'))
                # Set the highlight on the picked square
                #self.squares[i].setColor(HIGHLIGHT)
                self.hiSq = i

        return Task.cont

    def init_nodes_to_figures(self, need_to_add_dragging_figure=True, dragging_pos=None):
        """
        Creation of figues on the board (visual interpretation)
        :param str_board: chess board in string format
        :return: figues: array of objects.
        """
        for key in range(64):
            if self.str_board[key] != ".":
                # skip adding dragging figure
                if dragging_pos is not None and key == dragging_pos and need_to_add_dragging_figure is False:
                    key += 1
                    continue

                if self.dimension is Dimension._3D:
                    self.figures[key] = self.objMngr.load_figure_model(self.str_board[key])
                    self.figures[key].setPos(self.SquarePos(key))
                else:
                    self.figures[key] = self.objMngr.load_figure_model_2D(self.str_board[key])
                    self.figures[key].setHpr(180, -90, 0)
                    self.figures[key].setPos(self.FigurePos2D(key))

                self.figures[key].reparentTo(self.render_fsm_ref.render)
                self.figures[key].setTag("figue_tag", str(key))

                # rotate white figures
                if self.dimension is Dimension._3D:
                    if self.str_board[key].isupper():
                        self.figures[key].setH(180)
            else:
                self.figures[key] = None
            key += 1

    def init_nodes_to_chsess_board(self):
        self.squareRoot = self.render_fsm_ref.render.attachNewNode("squareRoot")

        # For each square
        for i in range(64):
            # Load, parent, color, and position the model (a single square
            # polygon)
            self.squares[i] = loader.loadModel("ChessRender/data/chess_board/square")
            self.squares[i].setTexture(self.SquareTexture(i))
            self.squares[i].reparentTo(self.squareRoot)
            self.squares[i].setPos(self.SquarePos(i))
            #self.squares[i].setColor(self.SquareColor(i))

            # Set the model itself to be collideable with the ray. If this model was
            # any more complex than a single polygon, you should set up a collision
            # sphere around it instead. But for single polygons this works
            # fine.
            self.squares[i].find("**/polygon").node().setIntoCollideMask(
                BitMask32.bit(1))
            # Set a tag on the square's node so we can look up what square this is
            # later during the collision pass
            self.squares[i].find("**/polygon").node().setTag('square', str(i))

    def SquareTexture(self, i):
        if (i + ((i // 8) % 2)) % 2:
            return loader.loadTexture("ChessRender/data/chess_board_cell.png")
        else:
            return loader.loadTexture("ChessRender/data/white_cell.png")

    def SquareColor(self, i):
        if (i + ((i // 8) % 2)) % 2:
            return (0.54, 0.4, 0.26, 1)#BLACK
        else:
            return (0.98, 0.82, 0.01, 1)

    def SquarePos(self, i):
        return LPoint3(-(i % 8) + 3.5, int(i // 8) - 3.5, 0)

    def FigurePos2D(self, i):
        return LPoint3(-(i % 8) + 3.5, int(i // 8) - 3.5, 0.3)

    def SquarePosFig(self, i):
        return LPoint3(-(i % 8) + 3.5, int(i // 8) - 3.5, 0.5)

    def PointAtZ(self, z, point, vec):
        return point + vec * ((z - point.getZ()) / vec.getZ())

    def init_ray(self):
        self.myTraverser = CollisionTraverser()
        self.myHandler = CollisionHandlerQueue()
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = base.camera.attachNewNode(self.pickerNode)

        self.pickerNode.setFromCollideMask(BitMask32.bit(1))
        self.pickerRay = CollisionRay()

        self.pickerNode.addSolid(self.pickerRay)
        self.myTraverser.addCollider(self.pickerNP, self.myHandler)

    def update_board(self, board_str):
        need_add_dragging_figure = None
        if self.dragging is not False:
            if self.str_board[self.dragging] == board_str[self.dragging]:
                need_add_dragging_figure = False
            else:
                need_add_dragging_figure = True
                self.dragging = False
        for i in range(len(self.figures)):
            if self.figures[i] is not None:
                if self.dragging is False or i != self.dragging:
                    self.figures[i].removeNode()
                else:
                    if need_add_dragging_figure is True:
                        self.figures[i].removeNode()

        self.str_board = board_str
        self.init_nodes_to_figures(need_add_dragging_figure, self.dragging)
