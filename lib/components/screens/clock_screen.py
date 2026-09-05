import lvgl as lv
from lib.components.screens.base_screen import BaseScreen
from lib.components.widgets.clock_widget import ClockWidget


class ClockScreen(BaseScreen):
    def __init__(self, time_manager):
        super().__init__()
        self.time_manager = time_manager
        self.clock = None
        
    def build(self):
        # Set bg color
        self.root.set_style_bg_color(lv.color_black(), 0)

        # Create and center clock
        self.clock = self.add_widget(ClockWidget(self.root, self.time_manager))
        self.clock.center()

    def enter(self):
        self.clock.activate()

    def leave(self):
        self.clock.deactivate()