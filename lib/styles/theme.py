import lvgl as lv

COLORS = {
    "teracotta": lv.color_hex(0xB5552D),
    "ivory": lv.color_hex(0xF2EBE1),
    "forest": lv.color_hex(0x3C4A3B),
    "slate": lv.color_hex(0x1D1D1B),
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