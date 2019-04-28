
class ButtonFsm:
    def __init__(self, title, position, command=None, link_key=None):
        self.title = title
        if command is not None:
            self.command = command
        self.link_key = link_key
        self.position = position

    def add_link(self, link_key):
        self.link_key = link_key

    def add_command(self, command):
        self.command = command

    def command(self):
        pass
