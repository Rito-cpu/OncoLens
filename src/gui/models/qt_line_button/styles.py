focused_template = """
    QGroupBox {{
        font: bold;
        font-size: {_title_size}px;
        background: transparent;
        color: {_color_one};
        border: {_border_color};
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