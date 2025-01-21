progress_bar_template = """
    QFrame#{_object_name} {{
        border-radius: {_border_radius}px;
        background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90,
        stop:{_stop_one} {_color_one}, stop:{_stop_two} {_color_two});
    }}
"""

circle_background_template = """
    QFrame#{_object_name} {{
        border-radius: {_border_radius}px;
        background-color: {_color_three};
    }}
"""

container_template = """
    QFrame#{_object_name} {{
        border-radius: {_border_radius}px;
        background-color: {_color_four};
    }}
"""

label_template = """
    QLabel#{_object_name} {{
        background-color: none;
        color: {_color_five};
    }}
"""

label_template_two = """
    QLabel#{_object_name} {{
        border-radius: 12px;
        background-color: {_color_six};
        color: {_color_five};
    }}
"""
