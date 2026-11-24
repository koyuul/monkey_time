import lvgl as lv

from lib.styles.theme import PALETTES


class BaseWidget:
    def __init__(self, parent, width, height, palette=PALETTES["LIGHT_MODE"]):
        self.root = lv.obj(parent)
        self.width = width
        self.height = height

        # Load some fonts
        self.fonts = {
            "space_mono_lg": lv.binfont_create("K:space_mono_96.bin"),
            "space_sans_serif_md": lv.binfont_create("K:space_sans_serif_16.bin")
        }
        self.root.set_style_text_font(self.fonts["space_sans_serif_md"], 0)
        
        # Default widget styling (visible border for visual bounds)
        self.palette = dict(palette)
        self.root.set_style_bg_opa(0, 0)
        self.root.set_style_border_width(0, 0)
        self.root.set_style_text_color(palette["NEUTRAL"], 0)

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
