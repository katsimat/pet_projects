from tkinter import Button


class Square(Button):
    def __init__(self, root, *args, **kwargs):
        Button.__init__(self, root, *args, **kwargs)
        self.x = None
        self.y = None
