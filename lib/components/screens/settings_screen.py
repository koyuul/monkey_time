import lvgl as lv
from lib.components.screens.base_screen import BaseScreen


class SettingsScreen(BaseScreen):
    def build(self):
        # Set bg color
        self.root.set_style_bg_color(lv.color_hex(0xFF8500), 0)

        text = lv.label(self.root)
        text.set_text("settings page yo")
        text.center()

    def enter(self):
        print("SettingsScreen entered")

    def leave(self):
        print("SettingsScreen left")