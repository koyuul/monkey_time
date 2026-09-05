import lvgl as lv


class BaseScreen:

    def __init__(self):
        self.root = lv.obj()
        self.widgets = []

    def build(self):
        pass

    # Use for per-screen functions on screen switch (eg: animations)
    def enter(self):
        for widget in self.widgets:
            widget.activate()

    # Use for per-screen functions on screen leave (eg: exit animation or save state)
    def leave(self):
        for widget in self.widgets:
            widget.deactivate

    # Use to add widgets to automatically activate/deactivate on enter/leave
    def add_widget(self, widget):
        self.widgets.append(widget)

    # Use for per-screen functions on a loop call (eg: idle screen timer)
    def update(self):
        pass