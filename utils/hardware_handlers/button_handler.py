import time

import uasyncio as asyncio

_BUTTON_MCP_INPUT = 1
_BUTTON_POLL_INTERVAL_MS = 10

class ButtonHandler:
    def __init__(self, mcp, pin, queue, button_id=None):
        mcp.pin(pin, mode=_BUTTON_MCP_INPUT, pullup=True, polarity=1)
        self.mcp = mcp
        self.pin = pin
        self.queue = queue
        self.id = button_id if button_id is not None else pin
        self.last_state = 1
    
    async def run(self):
        while True:
            try:
                button_pressed = self.mcp.pin(self.pin)
            except OSError:
                await asyncio.sleep_ms(_BUTTON_POLL_INTERVAL_MS)
                continue
            if button_pressed == 0 and self.last_state == 1:
                self.queue.append((
                    "button_press",
                    {
                        "id": self.id,
                        "pin": self.pin,
                    }
                ))
            self.last_state = button_pressed
            await asyncio.sleep_ms(_BUTTON_POLL_INTERVAL_MS)
                                                                                                    