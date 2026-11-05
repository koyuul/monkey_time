import lvgl as lv


class BaseScreen:
    COLS = 6
    ROWS = 4
    CELL_PX = 80

    GRID_COLS = ([ CELL_PX ] * COLS) + [ lv.GRID_TEMPLATE_LAST ]
    GRID_ROWS = ([ CELL_PX ] * ROWS) + [ lv.GRID_TEMPLATE_LAST ]

    def __init__(self):
        self.root = lv.obj()
        self.cells = []
        self.widgets = []

    def build(self):
        # Create a grid content obj within the current active screen
        self.root.set_style_grid_column_dsc_array(self.GRID_COLS, 0)
        self.root.set_style_grid_row_dsc_array(self.GRID_ROWS, 0)
        self.root.set_style_layout(lv.LAYOUT.GRID, 0)
        self.root.set_size((self.COLS * self.CELL_PX), (self.ROWS * self.CELL_PX))

        # Remove container padding, borders, and grid gaps
        self.root.set_style_pad_all(0, 0)
        self.root.set_style_pad_row(0, 0)       # Remove gap between rows
        self.root.set_style_pad_column(0, 0)    # Remove gap between columns
        self.root.set_style_border_width(0, 0)
        self.root.remove_flag(lv.obj.FLAG.SCROLLABLE)  # Prevent scrollbars from popping up

        # self._build_grid_overlay() # Uncomment for debugging

    # Use for per-screen functions on screen switch (eg: animations)
    def enter(self):
        for widget in self.widgets:
            widget.activate()

    # Use for per-screen functions on screen leave (eg: exit animation or save state)
    def leave(self):
        for widget in self.widgets:
            widget.deactivate()

    # Use to add widgets to automatically activate/deactivate on enter/leave
    def add_widget(self, widget):
        self.widgets.append(widget)
        return widget

    def place_widget(self, widget, top_left_x, top_left_y):
        widget.root.set_grid_cell(
            lv.GRID_ALIGN.STRETCH, top_left_x, widget.width,
            lv.GRID_ALIGN.STRETCH, top_left_y, widget.height
        )

    def _build_grid_overlay(self):
        self.grid_overlay = lv.obj(self.root)
        self.grid_overlay.set_size(self.COLS * self.CELL_PX, self.ROWS * self.CELL_PX)
        self.grid_overlay.set_style_grid_column_dsc_array(self.GRID_COLS, 0)
        self.grid_overlay.set_style_grid_row_dsc_array(self.GRID_ROWS, 0)
        self.grid_overlay.set_style_layout(lv.LAYOUT.GRID, 0)
        
        # Transparent overlay container, zero padding, ignore clicks
        self.grid_overlay.set_style_bg_opa(0, 0)
        self.grid_overlay.set_style_border_width(0, 0)
        self.grid_overlay.set_style_pad_all(0, 0)
        self.grid_overlay.set_style_pad_row(0, 0)
        self.grid_overlay.set_style_pad_column(0, 0)
        self.grid_overlay.remove_flag(lv.obj.FLAG.CLICKABLE)
        self.grid_overlay.remove_flag(lv.obj.FLAG.SCROLLABLE)

        # Populate with transparent, bordered cells
        for r in range(self.ROWS):
            for c in range(self.COLS):
                cell = lv.obj(self.grid_overlay)
                cell.set_grid_cell(
                    lv.GRID_ALIGN.STRETCH, c, 1,
                    lv.GRID_ALIGN.STRETCH, r, 1
                )
                cell.set_style_bg_opa(0, 0)
                cell.set_style_border_width(1, 0)
                cell.set_style_border_color(lv.color_hex(0x00FFCC), 0)  # Bright cyan/green for high contrast
                cell.set_style_border_opa(128, 0)                       # 50% opacity so it doesn't blind you
                cell.remove_flag(lv.obj.FLAG.CLICKABLE)

    # Use for per-screen functions on a loop call (eg: idle screen timer)
    def update(self):
        pass