
class ButtonFsm:
    def __init__(self, title, position, command=None, link_key=None, new_size=None, image_sizes=None, scale=0.15):
        self.title = title
        self.command = command
        self.link_key = link_key
        self.position = position
        self.new_size = new_size
        self.image_sizes = image_sizes
        self.scale = scale

    def add_link(self, link_key):
        self.link_key = link_key

    def add_command(self, command):
        self.command = command
