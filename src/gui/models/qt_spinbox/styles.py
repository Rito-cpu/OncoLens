box_template = """
    QDoubleSpinBox {{
        font-size: {_font_size}px;
        color: {_color};
        background: {_bg_color};
        border-radius: 6px;
    }}
    QDoubleSpinBox::up-button {{
        border: 1px solid {_border_color};
        border-top: none;
        border-right: none;
        image: url({_img_path}/downloads/white_plus.png);
        width: 14px;
        height: 14px;
    }}
    QDoubleSpinBox::down-button{{
        border: 1px solid {_border_color};
        border-bottom: none;
        border-top: none;
        border-right: none;
        image: url({_img_path}/downloads/white_minus.png);
        width: 14px;
        height: 14px;
    }}
"""
