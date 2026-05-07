"""
    Analog input manager: init + asyncio task for MCP23017 inputs.
"""
import time

import uasyncio as asyncio
import utils.mcp23017
from machine import I2C, Pin
from utils.hardware_handlers.button_handler import ButtonHandler
from utils.hardware_handlers.rotary_handler import RotaryHandler

_MCP_I2C_ID = 0
_MCP_SCL_PIN = 25
_MCP_SDA_PIN = 32
_MCP_FREQ = 400000
_MCP_ADDRESS = 0x20
_MCP_POLL_INTERVAL_MS = 1

_ROTARY_1_PINS = {
    "sw": 5,
    "dt": 4,
    "clk": 3,
}

class AnalogInputManager:
    def __init__(self):
        """Initialize I2C and MCP23017 and configure pins as inputs with pull-ups."""
        self.i2c = I2C(_MCP_I2C_ID, scl=Pin(_MCP_SCL_PIN), sda=Pin(_MCP_SDA_PIN), freq=_MCP_FREQ)
        self.mcp = utils.mcp23017.MCP23017(self.i2c, address=_MCP_ADDRESS)
        self.mcp.config(interrupt_polarity=0, interrupt_mirror=1)

        self.queue = []

        self.handlers = [
            ButtonHandler(self.mcp, 0, self.queue),
            ButtonHandler(self.mcp, 1, self.queue),
            RotaryHandler(self.mcp, self.mcp.porta, _ROTARY_1_PINS, self.queue),
        ]

        self.callbacks = {}

    def register_callback(self, event_type, callback, *args, **kwargs):
        if event_type not in self.callbacks:
            self.callbacks[event_type] = []
        self.callbacks[event_type].append((callback, args, kwargs))

    async def _run_handlers(self):
        for handler in self.handlers:
            asyncio.create_task(handler.run())

    def get_i2c(self):
        """Return the I2C instance for external use."""
        return self.i2c
    
    async def _event_loop(self):
        while True:
            if self.queue:
                event = self.queue.pop(0)
                event_type = event[0]
                if event_type in self.callbacks:
                    for cb, args, kwargs in self.callbacks[event_type]:
                        result = cb(event, *args, **kwargs)

                        # handle async callbacks too
                        if hasattr(result, "__await__"):
                            asyncio.create_task(result)
            else:
                await asyncio.sleep_ms(_MCP_POLL_INTERVAL_MS)

    async def run(self):
        await self._run_handlers()
        await self._event_loop()