import copy
from enum import Enum

from direct.gui.OnscreenText import CollisionTraverser, CollisionHandlerQueue, CollisionNode, \
    CollisionRay, OnscreenText, TransparencyAttrib, CollisionSphere
from direct.task import Task
from panda3d.core import BitMask32, LPoint3
from direct.gui.DirectButton import DirectButton

from ChessAI.GameController.game_controller import MoveResult
from ChessBoard.chess_figure import Side
from ChessRender.RenderFsmCommon.Camera.camera3d import Camera3D, Camera2D
from ChessRender.RenderFsmCommon.Lights.lights import Lights
from ChessRender.RenderFsmCommon.button_fsm import ButtonFsm
from ChessRender.RenderFsmCommon.screen_states import ScreenState
from ChessRender.RenderFsmCommon.figure_manage import FigureMngr, figure_as_render_object
from Vector2d.Vector2d import Vector2d, Move

HIGHLIGHT = (0, 1, 1, 1)

class Dimension(Enum):
    _2D = 1
    _3D = 2


class TapMovementManager:
    def __init__(self, render_fsm_ref, game_state):
        self.cur_clicked = None
        self.cur_clicked_pos = None
        self.render_fsm_ref = render_fsm_ref
        self.game_state = game_state

    def click(self, hiSq, pos):

        if self.cur_clicked is None or self.game_state.figures[self.cur_clicked] is None:
            if self.game_state.figures[hiSq] is None:
                return

            if self.game_state.get_cur_turn_side() is Side.WHITE and self.game_state.figures[hiSq].getTag("figue_lat").isupper() or \
                self.game_state.get_cur_turn_side() is Side.BLACK and self.game_state.figures[hiSq].getTag("figue_lat").islower():

                self.cur_clicked = hiSq
                self.cur_clicked_pos = pos
                return
            else:
                return

        # We have let go of the piece, but we are not on a square
        if self.render_fsm_ref.process_set_move_player is not None:
            move = Move(self.cur_clicked_pos, Vector2d(hiSq % 8, hiSq // 8))
            if self.game_state.figures[self.cur_clicked].getTag("figue_lat") is "p" and hiSq // 8 is 7:
                if self.game_state.get_cur_turn_side() is Side.BLACK and self.game_state.check_move_func(move, Side.BLACK) != MoveResult.INCORRECT:
                    self.game_state.swap_figures(self.cur_clicked, hiSq)
                    if self.game_state.figures[self.cur_clicked] is not None:
                        self.game_state.figures[self.cur_clicked].removeNode()
                    self.cur_clicked = None
                    self.game_state.fire_pawn_change_panel(Side.BLACK, copy.deepcopy(move))
                    self.game_state.dragging = False
                    return
            if self.game_state.figures[self.cur_clicked].getTag("figue_lat") is "P" and hiSq // 8 is 0:
                if self.game_state.get_cur_turn_side() is Side.WHITE and self.game_state.check_move_func(move, Side.WHITE) != MoveResult.INCORRECT:
                    self.game_state.swap_figures(self.cur_clicked, hiSq)
                    if self.game_state.figures[self.cur_clicked] is not None:
                        self.game_state.figures[self.cur_clicked].removeNode()
                    self.cur_clicked = None
                    self.game_state.fire_pawn_change_panel(Side.WHITE, copy.deepcopy(move))
                    self.game_state.dragging = False
                    return
            self.render_fsm_ref.process_set_move_player(Move(self.cur_clicked_pos, Vector2d(hiSq % 8, hiSq // 8)))
            self.cur_clicked = None

class FsmStateGameState(ScreenState):
    def __init__(self, render_fsm, whiteside_pack_name, blackside_pack_name, side, exit_link, check_move_func, get_cur_turn_side, on_exit_func=None):
        ScreenState.__init__(self)
        self.exit_link = "fsm:MainMenu"
        self.button_sizes = (-1.5, 1.5, -0.4, 0.8)
        self.render_fsm_ref = render_fsm
        self.render_fsm_ref.taskMgr.remove('camRotTask')
        self.side = side
        self.skysphere = None
        self.objMngr = FigureMngr(blackside_pack_name, whiteside_pack_name)

        self.dimension = Dimension._3D
        self.side = Side.WHITE

        self.init_sky_sphere()
        self.squares = [None for i in range(64)]
        self.info_squares = [None for i in range(100)]
        self.cubes = [None for i in range(64)]
        self.info_cubes = [None for i in range(100)]
        self.init_nodes_to_chsess_board()
        self.init_nodes_to_board_info()
        self.init_info_panel()
        self.pawn_change_panel = None
        self.swaped_icons = None

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

        self._camera_set()
        #self.camera_p = Camera(base.camera, base.camLens)
        base.disableMouse()
        # camera debug god mode
        #base.oobe()

        self.lights = Lights(base, self.render_fsm_ref.cur_window_width, self.render_fsm_ref.cur_window_height)

        self.screen_atributes.buttons["but:Exit"] = ButtonFsm("Exit", (-1, 0, 0.8), None, None, None, (1.8, 0.8, 0.8))
        self.screen_atributes.buttons["but:2D/3D"] = ButtonFsm("2D/3D", (1, 0, 0.8), None, None, None, (1.8, 0.8, 0.8))
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

        self.text_info = {}
        self.scale = 0.07
        self.on_exit_func = on_exit_func

        self.check_move_func = check_move_func
        self.get_cur_turn_side = get_cur_turn_side

        self.tap_movement_manager = TapMovementManager(render_fsm, self)

    def change_dimension(self):
        self.render_fsm_ref.taskMgr.remove('camPosTask')
        if self.dimension == Dimension._3D:
            self.dimension = Dimension._2D
        else:
            self.dimension = Dimension._3D
        self.update_board(self.str_board)
        self._camera_set()

    def _camera_set(self):
        if self.dimension == Dimension._3D:
            angle = Camera3D.WHITE_ANGLE if self.side is Side.WHITE else Camera3D.BLACK_ANGLE
            self.camera_p = Camera3D(base.camera, base.camLens, self.render_fsm_ref.cur_window_width, self.render_fsm_ref.cur_window_height, angle)
        else:
            angle = Camera2D.WHITE_ANGLE if self.side is Side.WHITE else Camera2D.BLACK_ANGLE
            self.camera_p = Camera2D(base.camera, base.camLens, self.render_fsm_ref.cur_window_width, self.render_fsm_ref.cur_window_height, angle)

    def init_sky_sphere(self):
        if self.side is Side.WHITE:
            self.skysphere = self.objMngr.load_skybox_white_side()
        else:
            self.skysphere = self.objMngr.load_skybox_black_side()
        self.skysphere.setBin('background', 1)
        self.skysphere.setDepthWrite(0)
        self.skysphere.reparentTo(render)
        self.skysphere.setPos(0, 0, 0)
        self.skysphere.setScale(20)

    def clear_state(self):
        self.render_fsm_ref.is_clearing = True
        for figure in self.figures:
            if figure is not None:
                figure.removeNode()

        for square in self.squares:
            square.removeNode()

        self.skysphere.removeNode()

        for square in self.info_squares:
            if square is not None:
                square.removeNode()

        for cube in self.cubes:
            cube.removeNode()

        for cube in self.info_cubes:
            if cube is not None:
                cube.removeNode()

        self.lights.unset()
        for key in self.text_info:
            self.text_info[key].destroy()

        self.panel.removeNode()
        if self.pawn_change_panel is not None:
            self.pawn_change_panel.removeNode()

        if self.swaped_icons is not None:
            for icon in self.swaped_icons:
                icon.removeNode()
        self.render_fsm_ref.is_clearing = False

        self.render_fsm_ref.taskMgr.remove('camRotTask')
        self.render_fsm_ref.taskMgr.add(self.render_fsm_ref.camera_m.update_on_task_rotate, 'camRotTask')

    def on_exit(self):
        if self.on_exit_func is not None:
            self.on_exit_func()
        self.clear_state()

    def initialize_button_links(self):
        self.screen_atributes.buttons["but:Exit"].add_command(self.on_exit)
        self.screen_atributes.buttons["but:Exit"].add_link(self.exit_link)
        self.screen_atributes.buttons["but:2D/3D"].add_command(self.change_dimension)

    def wheel_up(self):
        self.camera_p.update_on_mouse_wheel(1)

    def wheel_down(self):
        self.camera_p.update_on_mouse_wheel(-1)

    def middle_click(self, steps=60):
        self.render_fsm_ref.taskMgr.remove('camPosTask')
        #self.camera_p.set_default()
        if isinstance(self.camera_p, Camera3D):
            self.camera_p.prepare_task_goto_player_side_position(self.get_cur_turn_side(), steps)
            self.render_fsm_ref.taskMgr.add(self.camera_p.task_goto_player_side_position, 'camPosTask')
        elif isinstance(self.camera_p, Camera2D):
            self._camera_set()

    def right_click(self):
        self.render_fsm_ref.taskMgr.remove('camPosTask')
        mouse_watcher = base.mouseWatcherNode
        self.camera_p.start_rotating(mouse_watcher.getMouseX(), mouse_watcher.getMouseY())
        self.need_camera_update = True

    def right_release(self):
        self.render_fsm_ref.taskMgr.remove('camPosTask')
        self.need_camera_update = False

    def grab_piece(self):
        # If a square is highlighted and it has a piece, set it to dragging
        # mode
        if self.hiSq is not False and self.figures[self.hiSq]:
            self.dragging = self.hiSq
            self.dragging_figure_position = Vector2d(self.hiSq % 8, self.hiSq // 8)
            if self.tap_movement_manager is not None:
                self.tap_movement_manager.click(self.hiSq, self.dragging_figure_position)
            self.hiSq = False
            return

        if self.hiSq is not None and self.tap_movement_manager is not None:
            self.tap_movement_manager.click(self.hiSq, Vector2d(self.hiSq % 8, self.hiSq // 8))

    def release_piece(self):
        # Letting go of a piece. If we are not on a square, return it to its original
        # position. Otherwise, swap it with the piece in the new square
        # Make sure we really are dragging something
        if self.dragging is not False:
            # We have let go of the piece, but we are not on a square
            if self.dimension is Dimension._3D:
                self.figures[self.dragging].setPos(
                    self.FigurePos(self.dragging))
            else:
                self.figures[self.dragging].setPos(
                    self.FigurePos(self.dragging))
            if self.render_fsm_ref.process_set_move_player is not None:
                move = Move(self.dragging_figure_position, Vector2d(self.hiSq % 8, self.hiSq // 8))
                if self.figures[self.dragging].getTag("figue_lat") is "p" and self.hiSq // 8 is 7:
                    if self.get_cur_turn_side() is Side.BLACK and self.check_move_func(move, Side.BLACK) != MoveResult.INCORRECT:
                        self.swap_figures(self.dragging, self.hiSq)
                        if self.figures[self.dragging] is not None:
                            self.figures[self.dragging].removeNode()
                        self.dragging = False
                        self.fire_pawn_change_panel(Side.BLACK, move)
                        return
                if self.figures[self.dragging].getTag("figue_lat") is "P" and self.hiSq // 8 is 0:
                    if self.get_cur_turn_side() is Side.WHITE and self.check_move_func(move, Side.WHITE) != MoveResult.INCORRECT:
                        self.swap_figures(self.dragging, self.hiSq)
                        if self.figures[self.dragging] is not None:
                            self.figures[self.dragging].removeNode()
                        self.dragging = False
                        self.fire_pawn_change_panel(Side.WHITE, move)
                        return
                self.render_fsm_ref.process_set_move_player(Move(self.dragging_figure_position, Vector2d(self.hiSq % 8, self.hiSq // 8)))

        # We are no longer dragging anything
        self.dragging = False

    def fire_pawn_change_panel(self, side, move):
        self.render_fsm_ref.ignore("mouse1")  # left-click grabs a piece
        self.render_fsm_ref.ignore("mouse1-up")  # releasing places it
        self.render_fsm_ref.ignore("mouse2")
        self.render_fsm_ref.ignore("mouse3")
        self.render_fsm_ref.ignore("mouse3-up")

        self.render_fsm_ref.ignore("wheel_up")
        self.render_fsm_ref.ignore("wheel_down")

        self.screen_atributes.buttons["but:2D/3D"].command = None
        self.init_pawn_change_panel(side, move)

    def swap_figures(self, fr, to):
        temp = self.figures[fr]
        self.figures[fr] = self.figures[to]
        self.figures[to] = temp
        if self.figures[fr]:
            self.figures[fr].setPos(self.FigurePos(fr))
        if self.figures[to]:
            self.figures[to].setPos(self.FigurePos(to))

    def FigurePos(self, key):
        if self.dimension == Dimension._3D:
            return self.FigurePos3D(key)
        else:
            return self.FigurePos2D(key)

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
                    self.figures[key].setPos(self.FigurePos(key))
                else:
                    self.figures[key] = self.objMngr.load_figure_model_2D(self.str_board[key])
                    if self.side is Side.WHITE:
                        self.figures[key].setHpr(180, -90, 0)
                    else:
                        self.figures[key].setHpr(0, -90, 0)
                    self.figures[key].setPos(self.FigurePos(key))

                self.figures[key].reparentTo(self.render_fsm_ref.render)
                self.figures[key].setTag("figue_tag", str(key))
                self.figures[key].setTag("figue_lat", self.str_board[key])

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
            #self.squares[i].setTexture(self.SquareTexture(i))
            self.squares[i].reparentTo(self.squareRoot)
            self.squares[i].setPos(self.SquareUnderCubePos3D(i))
            #self.squares[i].setColor(self.SquareColor(i))

            self.cubes[i] = self.objMngr.load_cube()
            self.cubes[i].setColor(self.SquareColor(i))
            self.cubes[i].reparentTo(self.squareRoot)
            self.cubes[i].setPos(self.SquarePos(i))
            self.cubes[i].setScale(0.5)

            #self.cubes[i].setShaderAuto()

            self.cubes[i].setColor(self.SquareColor(i))
            self.cubes[i].setTexture(self.SquareTexture(i))


            # Set the model itself to be collideable with the ray. If this model was
            # any more complex than a single polygon, you should set up a collision
            # sphere around it instead. But for single polygons this works
            # fine.
            self.squares[i].find("**/polygon").node().setIntoCollideMask(
                BitMask32.bit(1))
            # Set a tag on the square's node so we can look up what square this is
            # later during the collision pass
            self.squares[i].find("**/polygon").node().setTag('square', str(i))

    def init_nodes_to_board_info(self):
        #self.squareRoot = self.render_fsm_ref.render.attachNewNode("squareRoot")

        # For each square
        for i in range(100):
            if i == 99 or i == 0 or i == 9 or i == 90:
                continue

            cube_pos = self.InfoCubePos(i)
            if cube_pos is None:
                continue

            # Load, parent, color, and position the model (a single square
            # polygon)

            self.info_squares[i] = loader.loadModel("ChessRender/data/chess_board/square")
            self.info_squares[i].setTexture(self.InfoTexture(i))
            self.info_squares[i].reparentTo(self.squareRoot)
            self.info_squares[i].setPos(self.InfoOnCubePos3D(i))

            if not (i == 99 or i == 0 or i == 9 or i == 90):
                if i // 10 == 0:
                    self.info_squares[i].setHpr(180, 0, 0)
                if i // 10 == 9:
                    self.info_squares[i].setHpr(0, 0, 0)
                if i % 10 == 0:
                    self.info_squares[i].setHpr(0, 0, 0)
                if i % 10 == 9:
                    self.info_squares[i].setHpr(180, 0, 0)

            self.info_cubes[i] = self.objMngr.load_cube()
            self.info_cubes[i].setColor(self.SquareColor(i))
            self.info_cubes[i].reparentTo(self.squareRoot)
            self.info_cubes[i].setPos(cube_pos)
            self.info_cubes[i].setScale(0.5)
            self.info_cubes[i].setTexture(self.SquareTexture(1))

    def init_info_panel(self):
        self.panel = self.objMngr.load_plane_textured("ChessRender/data/panel.png")
        self.panel.reparentTo(self.render_fsm_ref.aspect2d)
        self.panel.setPos((0, 0, 0.85))
        self.panel.setSx(1.3)
        self.panel.setSz(0.3)

    def init_pawn_change_panel(self, side, move):
        self.pawn_change_panel = self.objMngr.load_plane_textured("ChessRender/data/panel.png")
        self.pawn_change_panel.reparentTo(self.render_fsm_ref.aspect2d)
        self.pawn_change_panel.setPos((0, 0, -0.85))
        self.pawn_change_panel.setSx(1.8)
        self.pawn_change_panel.setSz(0.3)

        if side is Side.WHITE:
            swaped_figures = ["Q", "N", "B", "R"]
        else:
            swaped_figures = ["q", "n", "b", "r"]

        print('Side is ' + str(side))
        self.swaped_icons = []
        figure_num = 0
        for swaped_figure in swaped_figures:
            but = DirectButton(text="", scale=0.13,
                         command=self.swap_pawn_command,
                         extraArgs=[swaped_figure, move],
                         frameColor=((0.8, 0.8, 0.8, 0.0)),
                         pos=(-0.5 + 0.35 * figure_num, 0, -0.85),
                         image=self.objMngr.textures[figure_as_render_object(swaped_figure)]
                         )
            but.setTransparency(TransparencyAttrib.MAlpha)
            self.swaped_icons.append(but)
            figure_num += 1

    def swap_pawn_command(self, swaped_figure_latter, move):
        self.render_fsm_ref.accept("mouse1", self.grab_piece)  # left-click grabs a piece
        self.render_fsm_ref.accept("mouse1-up", self.release_piece)  # releasing places it
        self.render_fsm_ref.accept("mouse2", self.middle_click)
        self.render_fsm_ref.accept("mouse3", self.right_click)
        self.render_fsm_ref.accept("mouse3-up", self.right_release)
        self.render_fsm_ref.accept("wheel_up", self.wheel_up)
        self.render_fsm_ref.accept("wheel_down", self.wheel_down)
        self.screen_atributes.buttons["but:2D/3D"].add_command(self.change_dimension)
        self.render_fsm_ref.process_set_move_player(move, swaped_figure_latter)

    def SquareTexture(self, i):
        if (i + ((i // 8) % 2)) % 2:
            return loader.loadTexture("ChessRender/data/chess_board_cell.png")
        else:
            return loader.loadTexture("ChessRender/data/white_cell.png")

    def InfoTexture(self, i):
        latters = ["A", "B", "C", "D", "E", "F", "G", "H"]
        numbers = ["1", "2", "3", "4", "5", "6", "7", "8"]

        if i == 99 or i == 0 or i == 9 or i == 90:
            return loader.loadTexture(
                "ChessRender/data/chess_board_info/cell_empty.jpg")
        if i // 10 == 0:
            return loader.loadTexture(
                "ChessRender/data/chess_board_info/cell_{}.jpg".format(latters[i - 1]))
        if i // 10 == 9:
            return loader.loadTexture(
                "ChessRender/data/chess_board_info/cell_{}.jpg".format(latters[i - 91]))
        if i % 10 == 0:
            return loader.loadTexture(
                "ChessRender/data/chess_board_info/cell_{}.jpg".format(numbers[7 - (i // 10 - 1)]))
        if i % 10 == 9:
            return loader.loadTexture(
                "ChessRender/data/chess_board_info/cell_{}.jpg".format(numbers[7 - (i // 10 - 1)]))

    def SquareColor(self, i):
        if (i + ((i // 8) % 2)) % 2:
            return (0.54, 0.4, 0.26, 1)#BLACK
        else:
            return (0.98, 0.82, 0.01, 1)

    def SquarePos(self, i):
        return LPoint3(-(i % 8) + 3.5, int(i // 8) - 3.5, -0.5)

    def InfoCubePos(self, i):
        if i // 10 == 0 or i // 10 == 9 or i % 10 == 0 or i % 10 == 9:
            return LPoint3(-(i % 10) + 4.5, int(i // 10) - 4.5, -0.5)
        else:
            return None

    def InfoOnCubePos3D(self, i):
        if i // 10 == 0 or i // 10 == 9 or i % 10 == 0 or i % 10 == 9:
            return LPoint3(-(i % 10) + 4.5, int(i // 10) - 4.5, 0.01)
        else:
            return None

    def FigurePos3D(self, i):
        return LPoint3(-(i % 8) + 3.5, int(i // 8) - 3.5, 0)

    def SquareUnderCubePos3D(self, i):
        return LPoint3(-(i % 8) + 3.5, int(i // 8) - 3.5, -0.01)

    def SquareOnCubePos3D(self, i):
        return LPoint3(-(i % 8) + 3.5, int(i // 8) - 3.5, 0.01)

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
        if self.pawn_change_panel is not None:
            self.pawn_change_panel.removeNode()

            for icon in self.swaped_icons:
                icon.removeNode()

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

    def update_camera(self, side):
        self.side = side
        self._camera_set()

    def update_game_info(self, white_login, white_time, white_rate,
                         black_login, black_time, black_rate):
        for key in self.text_info:
            self.text_info[key].destroy()

        scale = self.scale
        if 'white_login' in self.text_info:
            self.text_info['white_login'].destroy()
        self.text_info['white_login'] = OnscreenText(text=white_login + " (" + str(white_rate) + ")",
                                                     pos=(-0.4, 0.9), scale=scale, fg=(1.0, 1.0, 1.0, 1.0))

        if 'white_time' in self.text_info:
            self.text_info['white_time'].destroy()
        self.text_info['white_time'] = OnscreenText(text=white_time,
                                                    pos=(-0.4, 0.8), scale=scale, fg=(1.0, 1.0, 1.0, 1.0))

        if 'slash' in self.text_info:
            self.text_info['slash'].destroy()
        self.text_info['slash'] = OnscreenText("-", pos=(-0.15, 0.9), scale=scale, fg=(1.0, 1.0, 1.0, 1.0))

        if 'black_login' in self.text_info:
            self.text_info['black_login'].destroy()
        self.text_info['black_login'] = OnscreenText(text=black_login + " (" + str(black_rate) + ")",
                                                     pos=(0.2, 0.9), scale=scale, fg=(1.0, 1.0, 1.0, 1.0))

        if 'black_time' in self.text_info:
            self.text_info['black_time'].destroy()
        self.text_info['black_time'] = OnscreenText(text=black_time, pos=(0.2, 0.8), scale=scale, fg=(1.0, 1.0, 1.0, 1.0))

    def update_game_result_info(self, win_side, delta_rate):
        for key in self.text_info:
            self.text_info[key].destroy()

        scale = self.scale
        if 'win_info' in self.text_info:
            self.text_info['win_info'].destroy()
        side_text = "Game over! \n"
        if win_side in (Side.WHITE, Side.BLACK):
            side_text += "Black won. " if win_side is Side.BLACK else "White won. "
        else:
            side_text += "It is draw. "
        self.text_info['win_info'] = OnscreenText(text=side_text +
                                                  "Delta rating is " + str(delta_rate),
                                                  pos=(-0.05, 0.9), scale=scale,
                                                  fg=(1.0, 0.0, 0.0, 1.0))
