from src.core.pyqt_core import *


class PyPushButton(QPushButton):
    bttn_template = """
    QPushButton {{
        border: none;
        padding-left: 10px;
        padding-right: 5px;
        color: {_color};
        border-radius: {_radius};
        background-color: {_bg_color};
        font-size: {_font_size}px;
    }}
    QPushButton:hover {{
        background-color: {_bg_color_hover};
    }}
    QPushButton:pressed {{
        background-color: {_bg_color_pressed};
    }}
    """

    highlight_style = """
    QPushButton {{
        border: 3px solid {_highlight};
        padding-left: 10px;
        padding-right: 5px;
        color: {_color};
        border-radius: {_radius};
        background-color: {_bg_color};
        font-size: {_font_size}px;
    }}
    QPushButton:hover {{
        background-color: {_bg_color_hover};
    }}
    QPushButton:pressed {{
        background-color: {_bg_color_pressed};
    }}
    """

    disabled_template = """
        QPushButton {{
            border: none;
            padding-left: 10px;
            padding-right: 5px;
            color: {_color};
            border-radius: {_radius};
            background-color: {_bg_color};
            font-size: {_font_size}px;
        }}
        QPushButton:hover {{
            background-color: {_bg_color_hover};
        }}
        QPushButton:pressed {{
            background-color: {_bg_color_pressed};
        }}
        QPushButton:disabled {{
            background-color: {_disabled_bg};
            color: {_disabled_color};
        }}
        """

    def __init__(
        self,
        text,
        radius,
        color,
        bg_color,
        bg_color_hover,
        bg_color_pressed,
        highlight = None,
        disabled_bg = None,
        disabled_color = None,
        font_size: int = 12,
        parent = None,
    ):
        super().__init__()

        # SET PARAMETRES
        self.setText(text)
        if parent is not None:
            self.setParent(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._can_highlight = highlight is not None

        # SET STYLESHEET
        self.default_style = self.bttn_template.format(
            _color = color,
            _radius = radius,
            _bg_color = bg_color,
            _bg_color_hover = bg_color_hover,
            _bg_color_pressed = bg_color_pressed,
            _font_size=font_size
        )
        self.setStyleSheet(self.default_style)

        if self._can_highlight:
            self.highlight_template = self.highlight_style.format(
                _highlight=highlight,
                _color=color,
                _radius=radius,
                _bg_color=bg_color,
                _bg_color_hover=bg_color_hover,
                _bg_color_pressed=bg_color_pressed,
                _font_size=font_size
            )

        if disabled_bg and disabled_color:
            self.default_template = self.disabled_template.format(
                _color = color,
                _radius = radius,
                _bg_color = bg_color,
                _bg_color_hover = bg_color_hover,
                _bg_color_pressed = bg_color_pressed,
                _font_size=font_size,
                _disabled_bg=disabled_bg,
                _disabled_color=disabled_color,
            )
            self.setStyleSheet(self.default_template)
        else:
            # SET DEFAULT STYLESHEET
            self.default_template = self.bttn_template.format(
                _color = color,
                _radius = radius,
                _bg_color = bg_color,
                _bg_color_hover = bg_color_hover,
                _bg_color_pressed = bg_color_pressed,
                _font_size=font_size
            )
            self.setStyleSheet(self.default_template)

    def set_highlight(self):
        if self._can_highlight:
            self.setStyleSheet(self.highlight_template)

    def remove_highlight(self):
        self.setStyleSheet(self.default_template)

    def set_disabled_color(self):
        pass
