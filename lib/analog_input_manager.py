"""
    Analog input manager: init + asyncio task for MCP23017 inputs.
"""
import time

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
_BUTTON_DEBOUNCE_MS = 50
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

        # Set up call backs to have other apps be notified of inputs
        self._callbacks = {pin: [] for pin in _BUTTON_PINS}
        self._last_state =  {pin: False for pin in _BUTTON_PINS}
        self._last_change = {pin: time.ticks_ms() for pin in _BUTTON_PINS}
        self._debounce_ms = _BUTTON_DEBOUNCE_MS
    
    def get_i2c(self):
        """Return the I2C instance for external use."""
        return self.i2c
    
    def register_callback(self, pin, callback, *args, **kwargs):
        """Register a callback for a specific pin."""
        if pin in self._callbacks:
            self._callbacks[pin].append((callback, args, kwargs))
    
    def unregister_callback(self, pin, callback):
        """Unregister a callback for a specific pin."""
        if pin in self._callbacks and callback in self._callbacks[pin]:
            self._callbacks[pin].remove(callback)

    async def poll_inputs(self):
        """Continuously poll the configured pins"""
        while True:
            now = time.ticks_ms()
            for pin in _BUTTON_PINS:
                # Read current state of the pin and register an event if any button pressed
                pressed = bool(self.mcp.pin(pin))
                if (
                    pressed != self._last_state[pin] and 
                    time.ticks_diff(now, self._last_change[pin]) > self._debounce_ms
                ):
                    self._last_state[pin] = pressed
                    self._last_change[pin] = now
                    if pressed:
                        event = {"pin": pin, "timestamp": now}
                        print(f"Button press: {event}")
                        
                        # Handle callbacks
                        for callback, args, kwargs in self._callbacks[pin]:
                            try: 
                                # Call the callback
                                result = callback(event, *args, **kwargs)

                                # Handle if callback is async
                                if hasattr(result, "__await__"):
                                    asyncio.create_task(result)
                            except Exception as e:
                                print("Callback error:", e)

            await asyncio.sleep_ms(_POLL_INTERVAL_MS)