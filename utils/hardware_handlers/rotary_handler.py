import uasyncio as asyncio

_ROTARY_POLL_INTERVAL_MS = 2

class RotaryHandler:
    def __init__(self, mcp, port, pins, queue):
        self.mcp = mcp
        self.port = port
        self.pins = pins
        self.queue = queue

        self.value = 0
        self.min_val = 0
        self.max_val = 10
        
        pin_mask = (1 << pins["clk"]) | (1 << pins["dt"])
        if "sw" in pins:
            pin_mask |= (1 << pins["sw"])
        
        self.port.mode |= pin_mask
        self.port.pullup |= pin_mask

        val = self.port.gpio
        clk = (val >> pins["clk"]) & 1
        dt  = (val >> pins["dt"]) & 1
        self.prev_state = (clk << 1) | dt

        self.sw_state = (val >> pins["sw"]) & 1 if "sw" in pins else 0
        self._transitions = [
             0, -1, +1,  0,
            +1,  0,  0, -1,
            -1,  0,  0, +1,
             0, +1, -1,  0
        ]
        self._accum = 0  # accumulate steps before committing
    
    def _enqueue_turn_event(self, clockwise):
        direction = 1 if clockwise else -1
        if clockwise:
            self.value = min(self.max_val, self.value + direction)
        else:
            self.value = max(self.min_val, self.value - direction)
        
        self.queue.append((
            "rotary_turn",
            {
                "direction": direction,
                "value": self.value,
            }
        ))
        self._accum = 0

    async def run(self):
        while True:
            val = self.port.gpio
            clk = (val >> self.pins["clk"]) & 1
            dt  = (val >> self.pins["dt"]) & 1
            curr_state = (clk << 1) | dt

            # transition lookup
            idx = (self.prev_state << 2) | curr_state
            delta = self._transitions[idx]

            if delta != 0:
                self._accum += delta

                # one full detent = 4 transitions
                if self._accum >= 4:
                    self._enqueue_turn_event(clockwise=True)
                elif self._accum <= -4:
                    self._enqueue_turn_event(clockwise=False)

            self.prev_state = curr_state

            # handle button
            if "sw" in self.pins:
                sw = (val >> self.pins["sw"]) & 1
                if sw != self.sw_state:
                    self.sw_state = sw

                    if sw == 0:  # pressed
                        self.queue.append((
                            "rotary_press",
                            {
                                "value": self.value
                            }
                        ))
            await asyncio.sleep_ms(_ROTARY_POLL_INTERVAL_MS)