class TextFieldFsm:

    def __init__(self, title, position, need_hide=False, initial_text=""):
        self.title = title
        self.position = position
        self.need_hide = need_hide
        self.initial_text = initial_text
