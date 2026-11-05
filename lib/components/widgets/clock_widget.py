import lvgl as lv

from lib.components.widgets.base_widget import BaseWidget


class ClockWidget(BaseWidget):
    def __init__(self, parent, width, height, time_manager):
        super().__init__(parent, width, height)
        self.time_manager = time_manager

        # center both labels in a row
        self.root.set_flex_flow(lv.FLEX_FLOW.ROW)
        self.root.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)

        self.time = lv.label(self.root)
        self.time.set_text("")
        self.ampm = lv.label(self.root)
        self.ampm.set_text("")

    def set_time(self, dt):
        self.time.set_text(f"{dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}")
    
    def set_ampm(self, dt):
        self.ampm.set_text("PM" if dt.hour >= 12 else "AM")

    def activate(self):
        self.time_manager.subscribe(self.set_time, self.time_manager.S)
        self.time_manager.subscribe(self.set_ampm, self.time_manager.H)


    def deactivate(self):
        self.time_manager.unsubscribe(self.set_time, self.time_manager.S)
        self.time_manager.unsubscribe(self.set_ampm, self.time_manager.H)