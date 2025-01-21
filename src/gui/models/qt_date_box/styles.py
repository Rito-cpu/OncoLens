date_template = """
    QDateEdit {{
        font-size: {_font_size}px;
        background: {_main_bg};
        color: {_color};
        border: none;
        border-radius: {_border_radius}px;
    }}
    QDateEdit::down-arrow {{
        image: url({_img_path}/downloads/white_down_arrow.png);
        width: 14px;
        height: 14px;
    }}
    QDateEdit::drop-down {{
        border-top-right-radius: {_border_radius}px;
        border-bottom-right-radius: {_border_radius}px;
        border-left: 1px solid white;
    }}
"""
