import lvgl as lv


class BaseWidget:
    def __init__(self, parent, width, height):
        self.root = lv.obj(parent)
        self.width = width
        self.height = height

        # Default widget styling (visible border for visual bounds)
        self.root.set_style_bg_opa(255, 0)
        self.root.set_style_border_width(2, 0)
        self.root.set_style_border_color(lv.color_make(255, 255, 255), 0)
        self.root.set_style_border_side(lv.BORDER_SIDE.FULL, 0)

    def build(self):
        raise NotImplementedError

    def show(self):
        self.root.clear_flag(lv.obj.FLAG.HIDDEN)

    def hide(self):
        self.root.add_flag(lv.obj.FLAG.HIDDEN)

    def center(self):
        self.root.center()

    # All sizing is in cells units of the grid
    def set_size(self, w, h):
        self.width = w
        self.height = h

    def delete(self):
        self.root.delete()

    def activate(self):
        pass

    def deactivate(self):
        pass
