import lvgl as lv

from lib.components.widgets.base_widget import BaseWidget
from lib.time_manager import WEEK


class ClockWidget(BaseWidget):
    def __init__(self, parent, width, height, time_manager):
        super().__init__(parent, width, height)
        self.time_manager = time_manager

        # Root layout: column flow (day on top, time below)
        # Horizontally right-aligned (FLEX_ALIGN.END), vertically centered (FLEX_ALIGN.CENTER)
        self.root.set_flex_flow(lv.FLEX_FLOW.COLUMN)
        self.root.set_flex_align(
            lv.FLEX_ALIGN.CENTER,  # Vertical: centered within widget height
            lv.FLEX_ALIGN.END,     # Horizontal: right-aligned
            lv.FLEX_ALIGN.END
        )
        self.root.set_style_pad_right(16, 0)  # Inset from right border
        self.root.set_style_pad_row(2, 0)     # Spacing between day and time

        # 1. Day of the week (smaller font, on top)
        self.weekday = lv.label(self.root)
        self.weekday.set_style_text_font(self.fonts["space_sans_serif_md"], 0)
        self.weekday.set_style_text_color(self.palette["ACCENT"], 0)
        self.weekday.set_text("")

        # 2. Time (enlarged font, below the day)
        self.time = lv.label(self.root)
        self.time.set_style_text_font(self.fonts["space_mono_lg"], 0)
        self.time.set_style_text_color(self.palette["NEUTRAL"], 0)
        self.time.set_text("")

    def set_time(self, dt):
        self.time.set_text(f"{dt.hour:02d}:{dt.minute:02d}")

    def set_weekday(self, dt):
        month_str = self.time_manager.get_month(dt.month)
        weekday_str = self.time_manager.get_weekday(dt.weekday)
        self.weekday.set_text(f"{month_str} {dt.day}, {weekday_str}")

    def activate(self):
        # Update immediately on activation so labels aren't blank
        current = self.time_manager.get_time()
        self.set_time(current)
        self.set_weekday(current)

        self.time_manager.subscribe(self.set_time, self.time_manager.S)
        self.time_manager.subscribe(self.set_weekday, self.time_manager.H)

    def deactivate(self):
        self.time_manager.unsubscribe(self.set_time, self.time_manager.S)
        self.time_manager.unsubscribe(self.set_weekday, self.time_manager.H)
