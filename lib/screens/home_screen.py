import lvgl as lv


def build(scr, component_manager):
    scr.clean()

    scr.set_style_bg_color(
        lv.color_black(),
        lv.PART.MAIN
    )

    title = lv.label(scr)
    title.set_text("Monkey Hour")
    title.align(lv.ALIGN.TOP_MID, 0, 20)

    # Default button style.
    normal_selector = lv.PART.MAIN | lv.STATE.DEFAULT
    # Encoder-selected button style.
    focused_selector = lv.PART.MAIN | lv.STATE.FOCUSED

    def style_menu_button(button):
        button.set_style_radius(10, normal_selector)
        button.set_style_bg_color(lv.palette_main(lv.PALETTE.GREY), normal_selector)
        button.set_style_bg_opa(lv.OPA.COVER, normal_selector)
        button.set_style_border_width(1, normal_selector)
        button.set_style_border_color(lv.palette_darken(lv.PALETTE.GREY, 2), normal_selector)
        button.set_style_transform_width(0, normal_selector)
        button.set_style_transform_height(0, normal_selector)
        button.set_style_anim_duration(120, lv.PART.MAIN)

        button.set_style_bg_color(lv.palette_main(lv.PALETTE.ORANGE), focused_selector)
        button.set_style_transform_width(10, focused_selector)
        button.set_style_transform_height(6, focused_selector)

        button.set_style_text_color(lv.color_white(), lv.PART.MAIN)

    def create_menu_button(text, y_offset, callback):
        button = lv.button(scr)
        button.set_size(200, 50)
        button.align(lv.ALIGN.CENTER, 0, y_offset)
        style_menu_button(button)

        label = lv.label(button)
        label.set_text(text)
        label.center()

        button.add_event_cb(callback, lv.EVENT.CLICKED, None)
        component_manager.add_component(button)
        return button

    clock_button = create_menu_button(
        "Clock",
        -60,
        lambda e : print("Clock_clicked"),
    )

    create_menu_button(
        "Settings",
        0,
        lambda e : print("Settings_clicked"),
    )

    create_menu_button(
        "About",
        60,
        lambda e : print("About_clicked"),
    )

    lv.group_focus_obj(clock_button)