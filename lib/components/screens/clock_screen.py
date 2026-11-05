import lvgl as lv

from lib.components.screens.base_screen import BaseScreen
from lib.components.widgets.clock_widget import ClockWidget


class ClockScreen(BaseScreen):
    def __init__(self, time_manager):
        super().__init__()
        self.time_manager = time_manager
        
    def build(self):
        super().build()
        clock_widget = ClockWidget(self.root, 4, 2, self.time_manager)
        self.place_widget(clock_widget, 2, 1)
        self.add_widget(clock_widget)


    def enter(self):
        super().enter()

    def leave(self):
        super().leave()