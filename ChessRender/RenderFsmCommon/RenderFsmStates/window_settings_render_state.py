from direct.gui.DirectScrollBar import DirectScrollBar

from ChessRender.RenderFsmCommon.button_fsm import ButtonFsm
from ChessRender.RenderFsmCommon.radio_button_fsm import RadioButtonFsm
from ChessRender.RenderFsmCommon.screen_states import ScreenState
from ChessRender.RenderFsmCommon.screen_text_fsm import ScreenTextFsm
from direct.showbase.ShowBase import ShowBase, WindowProperties

DEFAULT16x9SCREEN_W = 1280
DEFAULT16x9SCREEN_H = 720

DEFAULT4x3SCREEN_W = 1024
DEFAULT4x3SCREEN_H = 768

class FsmStateWindowSettings(ScreenState):
    def __init__(self, render_fsm):
        ScreenState.__init__(self)
        self.button_sizes = (-3, 3, -0.4, 0.8)
        self.render_fsm_ref = render_fsm

        self.screen_atributes.screen_texts["screen_text:Title"] = ScreenTextFsm("Windows params:", (0, 0.2))

        self.screen_atributes.radio_buttons["rb:WinSize 16:9"] = RadioButtonFsm("16:9", (-0.2, 0, 0), self.confirm_command)
        self.screen_atributes.radio_buttons["rb:WinSize 4:3"] = RadioButtonFsm("4:3", (0.2, 0, 0), self.confirm_command)

        self.screen_atributes.buttons["but:Confirm"] = ButtonFsm("Confirm", (0, 0, -0.5))
        self.screen_atributes.buttons["but:Back"] = ButtonFsm("Back", (0, 0, -0.8))

        self.initialize_button_links()

        # sound bar
        self.sound_value = int(render_fsm.sound.get_volume() * 100)
        self.screen_atributes.screen_texts["screen_text:sound"] = ScreenTextFsm("Sound volume:", (0, 0.7))

        self.sound_bar = DirectScrollBar(range=(0, 100),
                                         value=self.sound_value,
                                         pageSize=3, command=self.on_sound_change)

        self.sound_bar.setPos(0.0, 0.0, 0.5)
        self.screen_atributes.screen_texts["screen_text:sound_volume"] = ScreenTextFsm(str(self.sound_value), (0, 0.4))


    def on_sound_change(self):
        self.sound_value = int(self.sound_bar.getValue())
        self.render_fsm_ref.sound.set_volume(self.sound_value / 100.0)
        # sound bar
        self.screen_atributes.screen_texts["screen_text:sound_volume"] = ScreenTextFsm(str(self.sound_value), (0, 0.4))
        self.clear_nodes()
        self.render(self.render_fsm_ref)

    def initialize_button_links(self):
        self.screen_atributes.buttons["but:Confirm"].add_link("fsm:MainMenu")
        self.screen_atributes.buttons["but:Confirm"].add_command(self.confirm_command)
        self.screen_atributes.buttons["but:Back"].add_link("fsm:MainMenu")

    def confirm_command(self):
        # 16:9
        if self.radio_button_var[0] == 0:
            props = WindowProperties()
            props.clearSize()
            props.setTitle('Chess Classic')
            props.setSize(DEFAULT16x9SCREEN_W, DEFAULT16x9SCREEN_H)
            props.setFixedSize(True)
            self.render_fsm_ref.win.requestProperties(props)

        # 4:3
        if self.radio_button_var[0] == 1:
            props = WindowProperties()
            props.clearSize()
            props.setTitle('Chess Classic')
            props.setSize(DEFAULT4x3SCREEN_W, DEFAULT4x3SCREEN_H)
            props.setFixedSize(True)
            self.render_fsm_ref.win.requestProperties(props)

    def clear(self):
        for node in self.screen_atributes.scene_nodes:
            node.removeNode()
        for key in self.gui_text_fields.keys():
            self.gui_text_fields[key].removeNode()
        self.sound_bar.destroy()

    def clear_nodes(self):
        for node in self.screen_atributes.scene_nodes:
            node.removeNode()
        for key in self.gui_text_fields.keys():
            self.gui_text_fields[key].removeNode()
