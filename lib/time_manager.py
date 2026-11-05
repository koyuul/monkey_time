import random
import time

import utils.urtc as urtc

WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

class DummyRTC:
    """Mock RTC that generates a randomized reasonable datetime and ticks forward in real time."""
    class DateTime:
        def __init__(self, t):
            self.year, self.month, self.day, self.hour, self.minute, self.second, self.weekday = t[:7]

    def __init__(self):
        year = random.randint(2024, 2026)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        initial_secs = time.mktime((year, month, day, hour, minute, second, 0, 0))
        self._offset_secs = initial_secs - time.time()

    def datetime(self, val=None):
        if val is not None:
            return
        now_secs = int(time.time() + self._offset_secs)
        return self.DateTime(time.localtime(now_secs))

    def get_temperature(self):
        return 22.5
class TimeManager:
    H = "hour"
    M = "minute"
    S = "second"

    # Initialize either RTC or dummy RTC if doing a no peripheral run
    def __init__(self, i2c=None):
        if i2c is not None:
            self.rtc = urtc.DS3231(i2c)
        else:
            self.rtc = DummyRTC()
        self.subscribers = {
            "second": [],
            "minute": [],
            "hour": []
        }
        self.prev_minute = -1
        self.prev_hour = -1

    def subscribe(self, callback, timing):
        self.subscribers[timing].append(callback)

    def unsubscribe(self, callback, timing):
        self.subscribers[timing].remove(callback)

    def notify(self):
        now = self.get_time()
        for callback in self.subscribers["second"]:
            callback(now)

        if now.minute != self.prev_minute:
            for callback in self.subscribers["minute"]:
                callback(now)
            self.prev_minute = now.minute

        if now.hour != self.prev_hour:
            for callback in self.subscribers["hour"]:
                callback(now)
            self.prev_hour = now.hour
    
    # Time should be in format:(Y, M, D, wk_day, h, m, s, ms)
    def set_time(self, event, time_tuple):
        self.rtc.datetime(time_tuple)
    
    # Time returned as a datetime
    def get_time(self):
        current_datetime = self.rtc.datetime()
        return current_datetime
    
    # Get the current weekday as a string
    def get_weekday(self):
        current_datetime = self.rtc.datetime()
        return WEEK[current_datetime.weekday]
    
    # RTC has a temperature sensor, so this is a free gimme
    def get_temperature(self):
        return self.rtc.get_temperature()

