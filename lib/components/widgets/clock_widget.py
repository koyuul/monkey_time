import lvgl as lv
from lib.components.widgets.base_widget import BaseWidget


class ClockWidget(BaseWidget):
    def __init__(self, base, time_manager):
        super().__init__(base)

        time_manager.subscribe(self.set_time, time_manager.S)

        self.time = lv.label(self.root)
        self.ampm = lv.label(self.root)

        self.root.set_layout(lv.LAYOUT.FLEX)
        self.root.set_flex_flow(lv.FLEX_FLOW.COLUMN)

    def set_time(self, dt):
        self.time.set_text(f"{dt.hour}:{dt.minute}:{dt.second}")
    
    def set_ampm(self, ampm):
        self.ampm.set_text(ampm)

    