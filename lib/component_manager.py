import lvgl as lv
import uasyncio as asyncio


class ComponentManager:
    """
        Serves a middle layer between analog_input_manager and LVGL UI/UX.
        Handles LVGL navigation w/ encoder/buttons as inputs
    """                 
    def __init__(self, analog_input_manager, lvgl_manager):
        self.analog_input_manager = analog_input_manager
        self.lvgl_manager = lvgl_manager
        self.group = lv.group_create()

        self.encoder_delta = 0
        self.button_pressed = False

        self.analog_input_manager.register_callback(
            "rotary_turn",
            self._on_rotary,
        )
        self.analog_input_manager.register_callback(
            "button_press",
            self._on_button
        )

    def add_component(self, component):
        """
        Add object to LVGL focus group.
        """
        self.group.add_obj(component)

    def _on_rotary(self, event):
        payload = event[1]
        direction = payload.get("direction", 0) if isinstance(payload, dict) else payload
        if not isinstance(direction, int):
            return
        self.encoder_delta += direction
        print("rotary direction:", direction, "delta:", self.encoder_delta)
    
    def _on_button(self, event):
        button = event[1]
        if button == 0:
            self.button_pressed = True

    async def handle_input(self):
        """Handle input within asyncio format"""
        while True:
            if self.encoder_delta > 0:
                self.group.focus_next()
                self.encoder_delta -= 1
            elif self.encoder_delta < 0:
                self.group.focus_prev()
                self.encoder_delta += 1
            
            if self.button_pressed:
                focused = self.group.get_focused()
                if focused:
                    focused.send_event(lv.EVENT.CLICKED, None)
                self.button_pressed = False

            await asyncio.sleep_ms(10)
