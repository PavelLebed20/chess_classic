from direct.gui.DirectButton import DirectButton
from direct.gui.DirectEntry import DirectEntry
from direct.gui.DirectOptionMenu import DirectOptionMenu
from direct.gui.DirectRadioButton import DirectRadioButton
from direct.gui.OnscreenText import OnscreenText

class ScreenAtributes:
    def __init__(self):
        self.buttons = {}
        self.text_fields = {}
        self.screen_texts = {}
        self.option_lists = {}
        self.extra_objects = {}
        self.radio_buttons = {}

        self.scene_nodes = []


class ScreenState:
    def __init__(self):
        self.screen_atributes = ScreenAtributes()
        self.gui_text_fields = {}
        self.radio_button_var = [0]

    def initialize_button_links(self):
        pass

    def render(self, render_fsm):
        self.render_text_fields()
        self.render_buttons(render_fsm)
        self.render_screen_texts()
        self.render_option_lists()
        self.render_radio_buttons()

    def render_buttons(self, render_fsm):
        for button_key in self.screen_atributes.buttons.keys():
            button = self.screen_atributes.buttons[button_key]
            pos = button.position

            if button.command is not None and button.link_key is not None:
                commad_and_link = lambda render_fsm_, link_key_, button_: (button_.command(), render_fsm.change_state(render_fsm_, link_key_))

                gui_button = DirectButton(text=button.title, scale=0.2,
                                          command=commad_and_link,
                                          extraArgs=[render_fsm, button.link_key, button],
                                          pos=(pos[0], pos[1], pos[2]))
                self.screen_atributes.scene_nodes.append(gui_button)

            elif button.command is not None:
                gui_button = DirectButton(text=button.title, scale=0.2,
                                          command=button.command,
                                          pos=(pos[0], pos[1], pos[2]))
                self.screen_atributes.scene_nodes.append(gui_button)

            elif button.link_key is not None:
                gui_button = DirectButton(text=button.title, scale=0.2,
                                          command=render_fsm.change_state,
                                          extraArgs=[render_fsm, button.link_key],
                                          pos=(pos[0], pos[1], pos[2]))
                self.screen_atributes.scene_nodes.append(gui_button)

            elif button.command is None and button.link_key is None:
                gui_button = DirectButton(text=button.title, scale=0.2,
                                          pos=(pos[0], pos[1], pos[2]))
                self.screen_atributes.scene_nodes.append(gui_button)

    def render_text_fields(self):
        for text_field_key in self.screen_atributes.text_fields.keys():
            text_field = self.screen_atributes.text_fields[text_field_key]
            pos = text_field.position

            gui_text_field = DirectEntry(initialText=text_field.initial_text, scale=0.1,
                                      pos=(pos[0], pos[1], pos[2]), numLines=2)
            self.gui_text_fields[text_field.title] = gui_text_field

    def render_screen_texts(self):
        for screen_text_key in self.screen_atributes.screen_texts.keys():
            screen_text = self.screen_atributes.screen_texts[screen_text_key]
            pos = screen_text.position

            gui_screen_text = OnscreenText(text=screen_text.text, pos=(pos[0], pos[1]))

            self.screen_atributes.scene_nodes.append(gui_screen_text)

    def render_option_lists(self):
        for option_list_key in self.screen_atributes.option_lists.keys():
            option_list = self.screen_atributes.option_lists[option_list_key]
            pos = option_list.position

            command = lambda str_res_, option_list_: (option_list_.command(str_res_))
            gui_option_list = DirectOptionMenu(text=option_list.text, scale = 0.1, pos=(pos[0], pos[1], pos[2]),
                                               command=command)

            self.screen_atributes.scene_nodes.append(gui_option_list)

    def render_radio_buttons(self):
        gui_radio_buttons = []

        i = 0
        for radio_button_key in self.screen_atributes.radio_buttons.keys():
            radio_button = self.screen_atributes.radio_buttons[radio_button_key]
            pos = radio_button.position
            gui_radio_button = DirectRadioButton(text=radio_button.title, scale = 0.1, pos=(pos[0], pos[1], pos[2]), variable=self.radio_button_var, value=[i])

            self.screen_atributes.scene_nodes.append(gui_radio_button)
            gui_radio_buttons.append(gui_radio_button)
            i = i + 1

        for button in gui_radio_buttons:
            button.setOthers(gui_radio_buttons)

    def clear(self):
        for node in self.screen_atributes.scene_nodes:
            node.removeNode()
        for key in self.gui_text_fields.keys():
            self.gui_text_fields[key].removeNode()

    def mouse_task(self):
        pass

    def mouse_press(self):
        pass

    def mouse_release(self):
        pass
