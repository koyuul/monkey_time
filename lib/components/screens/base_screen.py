import lvgl as lv


class BaseScreen:

    def __init__(self):
        self.root = lv.obj()

    def build(self):
        pass

    # Use for per-screen functions on screen switch (eg: animations)
    def enter(self):
        pass

    # Use for per-screen functions on screen leave (eg: exit animation or save state)
    def leave(self):
        pass

    # Use for per-screen functions on a loop call (eg: idle screen timer)
    def update(self):
        pass