from direct.task import Task

from ChessRender.RenderFsmCommon.Camera.camera3d import Camera3D, Camera2D
from ChessRender.RenderFsmCommon.Lights.lights import Lights
from ChessRender.RenderFsmCommon.RenderFsmStates.game_render_state import Dimension
from ChessRender.RenderFsmCommon.button_fsm import ButtonFsm
from ChessRender.RenderFsmCommon.figure_manage import FigureMngr
from ChessRender.RenderFsmCommon.option_list_fsm import OptionListFsm
from ChessRender.RenderFsmCommon.screen_states import ScreenState


class FsmStateSkinSelect(ScreenState):
    def __init__(self, render_fsm, process_skin_select, avail_packs=["pack0", "pack1"]):
        ScreenState.__init__(self)
        self.render_fsm_ref = render_fsm
        self.lights = Lights(base, self.render_fsm_ref.cur_window_width, self.render_fsm_ref.cur_window_height)
        self.camera_p = Camera3D(base.camera, base.camLens, self.render_fsm_ref.cur_window_width, self.render_fsm_ref.cur_window_height)
        base.disableMouse()

        self.need_camera_update = False
        render_fsm.accept("mouse2", self.middle_click)

        render_fsm.accept("mouse3", self.right_click)
        render_fsm.accept("mouse3-up", self.right_release)

        render_fsm.accept("wheel_up", self.wheel_up)
        render_fsm.accept("wheel_down", self.wheel_down)

        self.screen_atributes.buttons["but:2D/3D"] = ButtonFsm("2D/3D", (0.8, 0, 0.8))
        self.screen_atributes.buttons["but:Prev"] = ButtonFsm("Prev", (-0.5, 0, -0.5))
        self.screen_atributes.buttons["but:Next"] = ButtonFsm("Next", (0.5, 0, -0.5))
        self.screen_atributes.buttons["but:Confirm"] = ButtonFsm("Confirm", (0.5, 0, -0.8))
        self.screen_atributes.buttons["but:Back"] = ButtonFsm("Back", (-0.5, 0, -0.8))

        self.screen_atributes.option_lists["oplst:PackName"] = OptionListFsm("Pack",
                                                                             avail_packs,
                                                                             self.option_list_confirm,
                                                                             (-0.8, 0 ,0.8))

        self.initialize_button_links()

        self.dimension = Dimension._3D

        self.current_pack = avail_packs[0]
        self.cur_model_num = 0
        self.cur_model_node = None
        self.models_order = ['k', 'q', 'b', 'n', 'r', 'p'
                             'K', 'Q', 'B', 'N', 'R', 'P']

        self.option_list_confirm("pack0")

        self.process_skin_select = process_skin_select

    def initialize_button_links(self):
        self.screen_atributes.buttons["but:Confirm"].add_link("fsm:MainMenu")
        self.screen_atributes.buttons["but:Confirm"].add_command(self.confirm_command)

        self.screen_atributes.buttons["but:Back"].add_link("fsm:MainMenu")
        self.screen_atributes.buttons["but:Back"].add_command(self.clear_state)
        self.screen_atributes.buttons["but:Next"].add_command(self.get_next)
        self.screen_atributes.buttons["but:Prev"].add_command(self.get_prev)
        self.screen_atributes.buttons["but:2D/3D"].add_command(self.change_dimension)

    def change_dimension(self):
        if self.dimension == Dimension._3D:
            self.dimension = Dimension._2D
            self.camera_p = Camera2D(base.camera, base.camLens, self.render_fsm_ref.cur_window_width, self.render_fsm_ref.cur_window_height)
        else:
            self.dimension = Dimension._3D
            self.camera_p = Camera3D(base.camera, base.camLens, self.render_fsm_ref.cur_window_width, self.render_fsm_ref.cur_window_height)

        self.load_model_to_screen()

    def clear_state(self):
        self.lights.unset()
        self.cur_model_node.removeNode()

    def get_next(self):
        self.cur_model_num += 1
        self.cur_model_num %= 11
        self.load_model_to_screen()

    def get_prev(self):
        self.cur_model_num -= 1
        self.cur_model_num %= 11
        self.load_model_to_screen()

    def option_list_confirm(self, arg):
        self.figure_manager = FigureMngr(arg, arg)
        self.load_model_to_screen()
        self.current_pack = arg

    def confirm_command(self):
        self.process_skin_select(self.current_pack)
        self.clear_state()

    def load_model_to_screen(self):
        if self.cur_model_node is not None:
            self.cur_model_node.removeNode()
        if self.dimension == Dimension._3D:
            self.cur_model_node = self.figure_manager.load_figure_model(self.models_order[self.cur_model_num])
        else:
            self.cur_model_node = self.figure_manager.load_figure_model_2D(self.models_order[self.cur_model_num])
            self.cur_model_node.setHpr(180, -90, 0)

        self.cur_model_node.setPos(0, 0, 0)
        self.cur_model_node.setScale(3)
        self.cur_model_node.reparentTo(self.render_fsm_ref.render)

    def wheel_up(self):
        self.camera_p.update_on_mouse_wheel(1)

    def wheel_down(self):
        self.camera_p.update_on_mouse_wheel(-1)

    def middle_click(self):
        self.camera_p.set_default()

    def right_click(self):
        mouse_watcher = base.mouseWatcherNode
        self.camera_p.start_rotating(mouse_watcher.getMouseX(), mouse_watcher.getMouseY())
        self.need_camera_update = True

    def right_release(self):
        self.need_camera_update = False

    def mouse_task(self):
        mouse_watcher = base.mouseWatcherNode
        if mouse_watcher.hasMouse() and self.need_camera_update:
            self.camera_p.update_pos(mouse_watcher.getMouseX(), mouse_watcher.getMouseY())
        return Task.cont