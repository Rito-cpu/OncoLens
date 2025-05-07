focused_template = """
    QGroupBox {{
        font: bold;
        font-size: {_title_size}px;
        background: transparent;
        color: {_color_one};
        border: 2px solid {_color_three};
        border-radius: {_border_radius}px;
        margin-top: {_top_margin}px;
        background: {_bg};
    }}
    QGroupBox:title {{
        subcontrol-origin: margin;
        left: {_left_spacing}px;
        color: {_title_color}
    }}
    QLineEdit {{
            font-size: {_text_size}px;
            background: transparent;
            padding-right: {_right_padding}px;
    }}
"""

focused_line_edit = """
    QLineEdit {{
        font-size: {_font_size}px;
        background: {_bg};
        color: {_text_color};
        border: 2px solid {_border_color};
        border-radius: {_border_radius}px;
        padding-left: 5px;
        padding-right: 5px;
    }}
"""

unfocused_template = """
    QGroupBox {{
        font: bold;
        font-size: {_title_size}px;
        background: transparent;
        color: {_color_two};
        border: 2px solid {_color_two};
        border-radius: {_border_radius}px;
        margin-top: {_top_margin}px;
    }}
    QGroupBox:title {{
        subcontrol-origin: margin;
        left: {_left_spacing}px;
    }}
    QLineEdit {{
        font-size: {_text_size}px;
        background: transparent;
        padding-right: {_right_padding}px;
    }}
"""

unfocused_line_edit = """
    QLineEdit {{
        font-size: {_font_size}px;
        background: transparent;
        color: {_text_color};
        border: 2px solid {_text_color};
        border-radius: {_border_radius}px;
        padding-left: 5px;
        padding-right: 5px;
    }}
"""