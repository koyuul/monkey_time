"""
    Source of truth clock for the rest of the system.
    Initializes time, keeps it ticking, and provide an interface
    for other components to query the current time.
"""
def initialize():
    """Called on boot to start task"""
    pass

def set_time(new_time, source):
    """Set/adjust time from various external sources"""
    pass

def get_time():
    pass

def subscribe(callback):
    pass

def timekeeper_task():
    return 0