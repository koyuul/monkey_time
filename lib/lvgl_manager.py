"""
    LVGL manager: init + asyncio task for LVGL display.
"""
import lcd_bus
import lvgl as lv
import machine
import st7796
import uasyncio as asyncio
from micropython import const

_DISPLAY_WIDTH = const(480)
_DISPLAY_HEIGHT = const(320)
_DISPLAY_ROT = const(0xE0)
_DISPLAY_BGR = const(1)
_DISPLAY_RGB565_BYTE_SWAP = const(1)

_SPI_BUS_HOST = const(1)
_SPI_BUS_MOSI = const(13)
_SPI_BUS_MISO = const(12)
_SPI_BUS_SCK = const(14)
_DISPLAY_BUS_FREQ = const(24000000)
_DISPLAY_BUS_DC = const(2)
_DISPLAY_BUS_CS = const(15)
_DISPLAY_BACKLIGHT_PIN = const(27)

class LVGLManager:
    def __init__(self):
        """Initialize LVGL and set up display/input drivers."""
        # Initialize hardware setup
        spi_bus = machine.SPI.Bus(host=_SPI_BUS_HOST, mosi=_SPI_BUS_MOSI, miso=_SPI_BUS_MISO, sck=_SPI_BUS_SCK)
        display_bus = lcd_bus.SPIBus(spi_bus=spi_bus, freq=_DISPLAY_BUS_FREQ, dc=_DISPLAY_BUS_DC, cs=_DISPLAY_BUS_CS)
        display = st7796.ST7796(
            data_bus=display_bus,
            display_width=_DISPLAY_WIDTH,
            display_height=_DISPLAY_HEIGHT,
            backlight_pin=_DISPLAY_BACKLIGHT_PIN,
            backlight_on_state=st7796.STATE_PWM,
            color_space=lv.COLOR_FORMAT.RGB565,
            color_byte_order=_DISPLAY_BGR,
            rgb565_byte_swap=_DISPLAY_RGB565_BYTE_SWAP
        )
        display._ORIENTATION_TABLE = (_DISPLAY_ROT, 0x0, 0x0, 0x0)
        display.set_rotation(lv.DISPLAY_ROTATION._0)
        display.set_power(True)
        display.init()
        display.set_backlight(100)

        # Initialize LVGL
        lv.init()
        self.scr = lv.screen_active()
        setup_main_ui(self.scr)

    async def update_display(self):
        """Run LVGL's Task Handler in the main scheduler loop"""
        while True:
            lv.tick_inc(5)
            lv.task_handler()
            await asyncio.sleep_ms(10)
        
def setup_main_ui(scr):
    """Build UI here or call your Rect/Label setup functions"""
    scr.set_style_bg_color(lv.color_black(), lv.PART.MAIN)
    
    lbl = lv.label(scr)
    lbl.set_text("Monkey Hour")
    lbl.align(lv.ALIGN.CENTER, 0, 0)
    lbl.set_style_text_color(lv.color_white(), 0)