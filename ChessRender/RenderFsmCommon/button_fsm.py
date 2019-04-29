
class ButtonFsm:
    def __init__(self, title, position, command=None, link_key=None, call_back_obj=None):
        self.title = title
        self.command = command
        self.call_back_obj = call_back_obj
        self.link_key = link_key
        self.position = position

    def add_link(self, link_key):
        self.link_key = link_key

    def add_command(self, command):
        self.command = command
