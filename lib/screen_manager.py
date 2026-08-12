import lvgl as lv

"""
    Screen Manager is responsible for:
        - registering new screens
        - switching between existing screens
        - keeping track of current screen
        - updating current screen
"""

class ScreenManager:
    def __init__(self):
        self.screens = {}
        self.current = None

    def register(self, name, screen):
        screen.build()
        self.screens[name] = screen

    def show(self, name):
        # Catch edge case
        if name not in self.screens:
            raise ValueError(f"Screen '{name}' is not registered")
        
        # Deactivate current screen
        if self.current:
            self.current.leave()

        # Load a new screen
        screen = self.screens[name]
        lv.screen_load(screen.root)
        screen.enter()
        self.current = screen
    
    def update(self):
        if self.current:
            self.current.update()
