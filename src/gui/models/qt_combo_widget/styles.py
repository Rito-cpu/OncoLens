combo_box_template = """
    QComboBox {{
        background: {bg};
        color: {color};
        border: none;
        border-radius: 4px;
        font-size: {font_size}px;
    }}
    QComboBox::drop-down {{
        border-left: 1px solid {color};
    }}
    QComboBox::down-arrow {{
        image: url({path});
        width: 15px;
        height: 15px;
    }}
    QComboBox:on {{
        background-color: {highlight_bg_on};
        color: {highlight_color_on};
    }}
    QComboBox:off {{
        background-color: {highlight_bg_off};
        color: {highlight_color_on};
    }}
    QComboBox QAbstractItemView {{
        background-color: {alternate_bg};
        color: {bg};
        selection-background-color: {highlight_bg_on};
        outline: none;
        min-width: 175px;
        max-height: 200px;
    }}
    QComboBox QAbstractItemView::item {{
        padding: 4px 8px;
    }}
"""