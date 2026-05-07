import time

import uasyncio as asyncio

_BUTTON_MCP_INPUT = 1
_BUTTON_POLL_INTERVAL_MS = 10

class ButtonHandler:
    def __init__(self, mcp, pin, queue):
        mcp.pin(pin, mode=_BUTTON_MCP_INPUT, pullup=True, polarity=1)
        self.mcp = mcp
        self.pin = pin
        self.queue = queue
        self.last_state = 1
    
    async def run(self):
        while True:
            button_pressed = self.mcp.pin(self.pin)
            if button_pressed == 0 and self.last_state == 1:
                self.queue.append((
                    "button_press",
                    self.pin
                ))
            self.last_state = button_pressed
            await asyncio.sleep_ms(_BUTTON_POLL_INTERVAL_MS)
