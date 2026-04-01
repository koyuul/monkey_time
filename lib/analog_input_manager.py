"""
    Analog input manager: init + asyncio task for MCP23017 inputs.
"""
import uasyncio as asyncio
import utils.mcp23017
from machine import I2C, Pin

_INPUT = 1
_I2C_ID = 0
_SCL_PIN = 25
_SDA_PIN = 32
_FREQ = 400000
_ADDRESS = 0x20
_BUTTON_PINS = [0, 1]
_POLL_INTERVAL_MS = 10

class AnalogInputManager:
    def __init__(self):
        """Initialize I2C and MCP23017 and configure pins as inputs with pull-ups."""
        self.i2c = I2C(_I2C_ID, scl=Pin(_SCL_PIN), sda=Pin(_SDA_PIN), freq=_FREQ)
        self.mcp = utils.mcp23017.MCP23017(self.i2c, address=_ADDRESS)

        # Configure each button pin as input
        for pin in _BUTTON_PINS:
            self.mcp.pin(pin, mode=_INPUT, pullup=True, polarity=1)

        # Configure interrupt
        self.mcp.config(interrupt_polarity=0, interrupt_mirror=1)
    
    async def poll_inputs(self):
        """Continuously poll the configured pins"""
        while True:
            for pin in _BUTTON_PINS:
                if self.mcp.pin(pin):
                    print(f"Button {pin} is pressed")
            await asyncio.sleep_ms(_POLL_INTERVAL_MS)