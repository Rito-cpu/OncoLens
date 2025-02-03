header_template = """
    QLabel {{
        color: {_header_color};
        font-size: {_header_size}px;
    }}"""

scroll_template = """
QScrollArea {{
    background: {_bg_color_one};
    border-radius: {_radius_one}px;
    border: none;
}}
"""

input_template = """
QWidget{_object_name} {{
    background: {_bg_color_two};
    border-radius: {_radius_two}px;
    border: {_border_one};
}}
"""

groupbox_gradient_template = """
    QScrollArea {{
        border: none;
        border-radius: {_radius}px;
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                        stop:0 {_bg_color_one}, stop:0.19186 {_bg_color_two}, stop:1 {_bg_color_three});
    }}
"""

groupbox_template = """
    QScrollArea {{
        border: none;
        border-radius: {_radius}px;
        background-color: {_bg_color_one};
    }}
"""

data_template = """
    QWidget {{
        font-size: {_font_size}px;
    }}
"""

general_groupbox = """
    QGroupBox {{
        font-size: {_font_size}px;
        background-color: {_bg_color};
        border: none;
        border-radius: {_border_radius}px;
        margin-top: {_top_margin}px;
        color: {_color};
    }}
    QGroupBox:title {{
        subcontrol-origin: margin;
        left: {_left_margin}px;
    }}
"""

current_file_template = """
    QWidget{{
        font-size: {_font_size}px;
        background: {_bg_color};
        border-radius: {_border_radius}px;
    }}
"""

treatment_instance_template = """
    QWidget#{_object_name} {{
        background: {_bg_color};
        border-radius: {_border_radius}px;
        border: none;
    }}
    QWidget#{_object_name} > QLabel {{
        color: {_color};
    }}
    QWidget#{_object_name} > QDoubleSpinBox {{
        color: {_color};
    }}
"""

available_tx_toggled = """
    QWidget#{_object_name} {{
        background: {_bg_color};
        border-radius: {_border_radius}px;
        border: none;
    }}
"""
