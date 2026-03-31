from micropython import const
import lvgl as lv
import time
import machine
import lcd_bus
import st7796
import task_handler
from machine import Timer


# ============== Customize settings ============== #
# The following values need to be customized.

# Switch width and height for portrait mode.
_DISPLAY_WIDTH = const(480)
_DISPLAY_HEIGHT = const(320)
# Try different values from rotation table, see below.
_DISPLAY_ROT = const(0xE0)
# Set to True if red and blue are switched.
_DISPLAY_BGR = const(1)
# May have to be set to 0 if both RGB / BGR mode give bad results.
_DISPLAY_RGB565_BYTE_SWAP = const(1)

'''
MADCTL_TABLE = {
    (False, 0): 0x80, # mirroring = False
    (False, 90): 0xE0,
    (False, 180): 0x40,
    (False, 270): 0x20,
    (True, 0): 0xC0, # mirroring = True
    (True, 90): 0x60,
    (True, 180): 0x00,
    (True, 270): 0xA0
}
'''


# ============== Display / Indev initialization ============== #
# no need to change anything below here
_SPI_BUS_HOST = const(1)
_SPI_BUS_MOSI = const(13)
_SPI_BUS_MISO = const(12)
_SPI_BUS_SCK = const(14)
_DISPLAY_BUS_FREQ = const(24000000)
_DISPLAY_BUS_DC = const(2)
_DISPLAY_BUS_CS = const(15)
_DISPLAY_BACKLIGHT_PIN = const(27)

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

# lv.DISPLAY_ROTATION._0 uses the first value from the
# display._ORIENTATION_TABLE to set display rotation
display.set_rotation(lv.DISPLAY_ROTATION._0)
display.set_power(True)
display.init()
display.set_backlight(100)


task_handler.TaskHandler()

# ============== End of display / touch (indev) setup ============== #


def palette_color(c, shade = 0):
    '''
    Returns a color from LVGL's main palette and
    lightens or darkens the color by a specified shade.
    
    Palette Colors:
    RED, PINK, PURPLE, DEEP_PURPLE, INDIGO, BLUE,
    LIGHT_BLUE, CYAN, TEAL, GREEN, LIGHT_GREEN, LIME, 
    YELLOW, AMBER, ORANGE, DEEP_ORANGE, BROWN, BLUE_GREY, GREY
    '''
    attr = getattr(lv.PALETTE, c.upper(), 'Undefined')
    if attr != 'Undefined':
        if not (shade in range(-4, 6)): return lv.color_black()
        if shade == 0:
            return lv.palette_main(attr)
        elif shade > 0:
            return lv.palette_lighten(attr, shade)
        elif shade < 0:
            return lv.palette_darken(attr, abs(shade))
    else:
        return lv.color_black()

class RectStyle(lv.style_t):
    def __init__(self, bg_color=lv.color_black()):
        super().__init__()
        self.set_bg_opa(lv.OPA._100)
        self.set_bg_color(bg_color)
        self.set_text_opa(lv.OPA._100)
        self.set_text_color(lv.color_black())


class Rect():
    def __init__(self, align, color, parent):
        self.align = align
        self.color = palette_color(color)
        self.parent = parent
        
        self.lvalign = getattr(lv.ALIGN, self.align, 'Undefined')
        
        s = self.align.split('_') # Remove undersore from align value and
        self.text = s[0][0] + s[1][0] # converts e.g. TOP_LEFT to TL as shortcut
        
        self.rect = lv.obj(parent)
        self.rect.remove_style_all()
        self.rect.set_size(35, 35)
        self.rect.align(self.lvalign, 0, 0)
        self.rect.add_style(RectStyle(bg_color = self.color), lv.PART.MAIN)
        self.rect.add_style(RectStyle(bg_color = lv.color_white()), lv.PART.MAIN | lv.STATE.PRESSED)
        self.rect.add_event_cb(lambda e: self._cb(), lv.EVENT.CLICKED, None)
        
        self.lbl = lv.label(self.rect)
        self.lbl.remove_style_all()
        self.lbl.set_text(self.text)
        self.lbl.center()
        
    
    def _cb(self):
        status_lbl.set_text(f'{self.align.replace("_", " ")} obj clicked!')
        status_lbl.set_style_text_color(self.color, 0)
        
class FlexRowStyle(lv.style_t):
    def __init__(self):
        super().__init__()
        
        self.set_text_align(lv.TEXT_ALIGN.CENTER)
        
        self.set_flex_flow(lv.FLEX_FLOW.ROW_WRAP)
        self.set_flex_main_place(lv.FLEX_ALIGN.SPACE_EVENLY)
        self.set_layout(lv.LAYOUT.FLEX)


# ========== Start UI  ========== #

# Create a screen
scr = lv.screen_active()
scr.set_style_bg_color(lv.color_black(), lv.PART.MAIN)
scr.remove_flag(lv.obj.FLAG.SCROLLABLE)

# This label will display touch coordinates / clicked object
status_lbl = lv.label(scr)
status_lbl.set_text('Click Test,\nClick Anywhere.')
status_lbl.align(lv.ALIGN.CENTER, 0, -40)
status_lbl.set_style_text_color(lv.color_white(), 0)
status_lbl.set_style_text_align(lv.TEXT_ALIGN.CENTER, 0)

# Container provides margin from display edge for the rects
rect_container = lv.obj(scr)
rect_container.remove_style_all()
rect_container.set_size(lv.pct(100), lv.pct(100))
rect_container.align(lv.ALIGN.TOP_LEFT, 0, 0)
rect_container.set_style_pad_all(10, 0)

# Create rectangular objets as touch targets
align = ['BOTTOM_LEFT', 'BOTTOM_MID', 'BOTTOM_RIGHT', 'LEFT_MID',
         'RIGHT_MID', 'TOP_LEFT', 'TOP_MID', 'TOP_RIGHT']

colors = ['CYAN', 'DEEP_PURPLE', 'GREEN', 'ORANGE',
          'PINK', 'LIME', 'RED', 'YELLOW']

for a, c in zip(align, colors):
    r = Rect(a, c, rect_container)

# Container for color display test
# It will display three rects in red, green and blue with labels
color_container = lv.obj(rect_container)
color_container.remove_style_all()
color_container.set_size(132, 40)
color_container.align(lv.ALIGN.CENTER, 0, 30)
color_container.add_style(RectStyle(bg_color = lv.color_black()), lv.PART.MAIN)
color_container.add_style(FlexRowStyle(), lv.PART.MAIN)

for l, c in (zip('RGB', (0xF00, 0x0F0, 0x00F))):
    color_rect = lv.obj(color_container)
    color_rect.remove_style_all()
    color_rect.set_size(lv.pct(30), lv.pct(100))
    color_rect.add_style(RectStyle(bg_color = lv.color_hex3(c)), lv.PART.MAIN)
    
    color_lbl = lv.label(color_rect)
    color_lbl.remove_style_all()
    color_lbl.set_text(l)
    color_lbl.center()
    color_lbl.set_style_text_color(lv.color_black(), 0)
    
    
color_container_lbl = lv.label(rect_container)
color_container_lbl.remove_style_all()
color_container_lbl.set_text('Color Test.')
color_container_lbl.align_to(color_container, lv.ALIGN.OUT_TOP_MID, 0, -5)
color_container_lbl.set_style_text_color(lv.color_white(), 0)

# Print LVGL version info and available fonts
print(f'--- LVGL Version: {lv.version_major()}.{lv.version_minor()}. ---')
print('Available LVGL fonts:')
print(', '.join([f'lv.{m}' for m in dir(lv) if 'font_montserrat' in m or 'font_unscii' in m]))


while True:
    time.sleep(1)