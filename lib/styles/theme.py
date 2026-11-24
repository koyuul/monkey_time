import sys

import lvgl as lv


def _color(rgb_hex):
    # In Linux SDL simulation, SDL expects BGR byte order,
    # so Red and Blue channels are swapped (0xRRGGBB -> 0xBBGGRR).
    if sys.platform == "linux":
        r = (rgb_hex >> 16) & 0xFF
        g = (rgb_hex >> 8) & 0xFF
        b = rgb_hex & 0xFF
        rgb_hex = (b << 16) | (g << 8) | r
    return lv.color_hex(rgb_hex)


COLORS = {
    "teracotta": _color(0xB5552D),
    "terracotta": _color(0xB5552D),
    "ivory": _color(0xF2EBE1),
    "forest": _color(0x3C4A3B),
    "slate": _color(0x1D1D1B),
}

PALETTES = {
    "LIGHT_MODE": {
        "BACKGROUND": COLORS["ivory"],
        "NEUTRAL": COLORS["slate"],
        "ACCENT": COLORS["teracotta"],
        "STATUS": COLORS["forest"],
    },
    "DARK_MODE": {
        "BACKGROUND": COLORS["slate"],
        "NEUTRAL": COLORS["ivory"],
        "ACCENT": COLORS["teracotta"],
        "STATUS": COLORS["forest"],
    },
}