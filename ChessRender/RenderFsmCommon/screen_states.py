from direct.gui.DirectButton import DirectButton
from direct.gui.DirectEntry import DirectEntry
from direct.gui.OnscreenText import OnscreenText


class ScreenAtributes:
    def __init__(self):
        self.buttons = {}
        self.text_fields = {}
        self.screen_texts = {}
        self.extra_objects = {}

        self.scene_nodes = []


class ScreenState:
    def __init__(self):
        self.screen_atributes = ScreenAtributes()
        self.gui_text_fields = {}

    def initialize_button_links(self):
        pass

    def render(self, render_fsm):
        self.render_text_fields()
        self.render_buttons(render_fsm)
        self.render_screen_texts()

    def render_buttons(self, render_fsm):
        for button_key in self.screen_atributes.buttons.keys():
            button = self.screen_atributes.buttons[button_key]
            pos = button.position

            if button.command is not None and button.link_key is not None:
                commad_and_link = lambda render_fsm_, link_key_: (button.command(), render_fsm.change_state(render_fsm_, link_key_))

                gui_button = DirectButton(text=button.title, scale=0.2,
                                          command=commad_and_link,
                                          extraArgs=[render_fsm, button.link_key],
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
                                      pos=(pos[0], pos[1], pos[2]))
            self.gui_text_fields[text_field.title] = gui_text_field

    def render_screen_texts(self):
        for screen_text_key in self.screen_atributes.screen_texts.keys():
            screen_text = self.screen_atributes.screen_texts[screen_text_key]
            pos = screen_text.position

            gui_screen_text = OnscreenText(text=screen_text.text, pos=(pos[0], pos[1], pos[2]))

            self.screen_atributes.scene_nodes.append(gui_screen_text)

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
