"""
    Analog input manager: init + asyncio task for MCP23017 inputs.
"""
from machine import I2C, Pin
import uasyncio as asyncio
import utils.mcp23017

INPUT = 1

I2C_ID = 0
SCL_PIN = 25
SDA_PIN = 32
FREQ = 400000
ADDRESS = 0x20
BUTTON_PINS = [0, 1]
POLL_INTERVAL_S = 0.2

class AnalogInputManager():
    def __init__(self):
        """Initialize I2C and MCP23017 and configure pins as inputs with pull-ups."""
        self.i2c = I2C(I2C_ID, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=FREQ)
        self.mcp = utils.mcp23017.MCP23017(self.i2c, address=ADDRESS)

        # Configure each button pin as input
        for pin in BUTTON_PINS:
            self.mcp.pin(pin, mode=INPUT, pullup=True, polarity=1)

        # Configure interrupt
        self.mcp.config(interrupt_polarity=0, interrupt_mirror=1)
    
    async def poll_inputs(self):
        """Continuously poll the configured pins"""
        while True:
            for pin in BUTTON_PINS:
                if self.mcp.pin(pin):
                    print(f"Button {pin} is pressed")
            await asyncio.sleep(POLL_INTERVAL_S)