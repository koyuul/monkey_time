import lvgl as lv


class BaseWidget:
    def __init__(self, parent):
        self.root = lv.obj(parent)

    """
        Build the widget's inner layout based on the given size.
    """
    def show(self):
        self.root.clear_flag(lv.obj.FLAG.HIDDEN)

    def hide(self):
        self.root.add_flag(lv.obj.FLAG.HIDDEN)

    def center(self):
        self.root.center()

    def set_size(self, w, h):
        self.root.set_size(w, h)

    def set_width(self, w):
        self.root.set_width(w)

    def set_height(self, h):
        self.root.set_height(h)

    def delete(self):
        self.root.delete()