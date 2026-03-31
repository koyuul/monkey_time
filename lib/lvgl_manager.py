from micropython import const
import lvgl as lv
import time
import machine
import lcd_bus
import st7796
import task_handler

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

class LVGLManager():
    def __init__(self):
        """Initialize LVGL and set up display/input drivers."""
        spi_bus = machine.SPI.Bus(
            host=_SPI_BUS_HOST,
            mosi=_SPI_BUS_MOSI,
            miso=_SPI_BUS_MISO,
            sck=_SPI_BUS_SCK
        )
        display_bus = lcd_bus.SPIBus(
            spi_bus=spi_bus,
            freq=_DISPLAY_BUS_FREQ,
            dc=_DISPLAY_BUS_DC,
            cs=_DISPLAY_BUS_CS
        )
        display = st7796.ST7796(
            data_bus=display_bus,
            display_width=_DISPLAY_WIDTH,
            display_height=_DISPLAY_HEIGHT,
            backlight_pin=_DISPLAY_BACKLIGHT_PIN,
            backlight_on_state=st7796.STATE_PWM,
            color_space=lv.COLOR_FORMAT.RGB565,
            color_byte_order=st7796.BYTE_ORDER_BGR if _DISPLAY_BGR else st7796.BYTE_ORDER_RGB,
            rgb565_byte_swap=_DISPLAY_RGB565_BYTE_SWAP
        )
        # The rotation table MUST be defined
        display._ORIENTATION_TABLE = (
            _DISPLAY_ROT, # this value sets the rotation
            0x0, # placeholder
            0x0, # placeholder
            0x0 # placeholder
        )



def init_lvgl():
    """Initialize LVGL bindings and register display/input drivers."""
    try:
        lv.init()
    except Exception:
        pass
    
    # Create a simple screen with a centered label
    try:
        scr = lv.scr_act()
        lbl = lv.label(scr)
        lbl.set_text("Monkey Hour")
        try:
            lv.obj.align(lbl, None, lv.ALIGN.CENTER, 0, 0)
        except Exception:
            # alternate API
            lbl.align(None, lv.ALIGN.CENTER, 0, 0)
    except Exception as exc:
        print("init_lvgl: failure in LVGL display", exc)

async def lvgl_task():
    """Run LVGL's Task Handler in the main scheduler loop"""
    prev = time.ticks_ms()
    while True:
        current = time.ticks_ms()
        elapsed = time.ticks_diff(current, prev)
        if elapsed >= 0: # Tick every 10ms
            try:
                lv.tick_inc(elapsed)
            except Exception:
                pass
            prev = current
        
        try:
            lv.task_handler()
        except Exception:
            pass

        await asyncio.sleep_ms(10) # Tick every 10ms
        
