import utils.urtc as urtc

WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

class TimeManager:
    H = "hour"
    M = "minute"
    S = "second"
    
    def __init__(self, i2c):
        self.rtc = urtc.DS3231(i2c)
        self.subscribers = {
            "second": [],
            "minute": [],
            "hour": []
        }
        self.prev_minute = -1
        self.prev_hour = -1

    def subscribe(self, callback, timing):
        self.subscribers[timing].append(callback)

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

