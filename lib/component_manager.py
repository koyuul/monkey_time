import lvgl as lv
import uasyncio as asyncio
from lib.analog_input_manager import BUTTON_0, BUTTON_1, ROTARY_1, ROTARY_2


class ComponentManager:
    """
        Serves a middle layer between analog_input_manager and LVGL UI/UX.
        Handles LVGL navigation w/ encoder/buttons as inputs
    """                 
    def __init__(self, analog_input_manager, lvgl_manager, nav_encoder_id=ROTARY_1, click_buttons=None):
        self.analog_input_manager = analog_input_manager
        self.lvgl_manager = lvgl_manager
        self.group = lv.group_create()

        # Designate which encoder controls LVGL focus navigation
        self.nav_encoder_id = nav_encoder_id

        # Buttons/switches mapped to click the currently focused widget
        if click_buttons is None:
            # Default: Button 0 and the navigation rotary knob's push switch
            self.click_buttons = {BUTTON_0, 0, ROTARY_1}
        else:
            self.click_buttons = set(click_buttons)

        self.encoder_delta = 0
        self.button_pressed = False

        # Specific action callbacks mapped by source ID
        self.button_callbacks = {}
        self.encoder_callbacks = {}

        self.analog_input_manager.register_callback(
            "rotary_turn",
            self._on_rotary,
        )
        self.analog_input_manager.register_callback(
            "rotary_press",
            self._on_rotary_press,
        )
        self.analog_input_manager.register_callback(
            "button_press",
            self._on_button,
        )

    def add_component(self, component):
        """Add object to LVGL focus group."""
        self.group.add_obj(component)

    def remove_component(self, component):
        """Remove object from LVGL focus group."""
        self.group.remove_obj(component)

    def get_group(self):
        """Return the LVGL focus group."""
        return self.group

    def set_button_callback(self, button_id, callback):
        """
        Register a custom callback for a specific button or rotary push switch.
        Callback signature: callback(payload)
        """
        self.button_callbacks[button_id] = callback

    def set_encoder_callback(self, encoder_id, callback):
        """
        Register a custom callback for a specific rotary encoder turn.
        Callback signature: callback(direction, payload)
        """
        self.encoder_callbacks[encoder_id] = callback

    def set_nav_encoder(self, encoder_id):
        """Set which encoder controls UI focus navigation."""
        self.nav_encoder_id = encoder_id

    def _on_rotary(self, event):
        payload = event[1] if len(event) > 1 else {}
        if isinstance(payload, dict):
            encoder_id = payload.get("id")
            direction = payload.get("direction", 0)
        else:
            encoder_id = None
            direction = payload

        if not isinstance(direction, int):
            return

        # Trigger custom encoder callback if registered
        if encoder_id in self.encoder_callbacks:
            self.encoder_callbacks[encoder_id](direction, payload)

        # Apply navigation if this encoder is the designated navigation encoder
        if self.nav_encoder_id is None or encoder_id == self.nav_encoder_id:
            self.encoder_delta += direction
            print("nav rotary direction:", direction, "encoder:", encoder_id, "delta:", self.encoder_delta)

    def _on_rotary_press(self, event):
        payload = event[1] if len(event) > 1 else {}
        encoder_id = payload.get("id") if isinstance(payload, dict) else payload

        # Check for registered custom action callback
        if encoder_id in self.button_callbacks:
            self.button_callbacks[encoder_id](payload)
        elif encoder_id in self.click_buttons:
            self.button_pressed = True

    def _on_button(self, event):
        payload = event[1] if len(event) > 1 else {}
        if isinstance(payload, dict):
            btn_id = payload.get("id")
            pin = payload.get("pin")
        else:
            btn_id = payload
            pin = payload

        # Check for registered custom callback
        if btn_id in self.button_callbacks:
            self.button_callbacks[btn_id](payload)
        elif pin in self.button_callbacks:
            self.button_callbacks[pin](payload)
        elif btn_id in self.click_buttons or pin in self.click_buttons:
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
