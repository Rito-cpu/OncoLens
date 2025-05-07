from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.gui.models.qt_line_button.styles import *


class EnhancedLineEdit(QLineEdit):
    def __init__(
        self,
        font_size: int = 12,
        bg: str = "white",
        text_color: str = "gray",
        border_color: str = "green",
        border_radius: int = 8,
        parent=None
    ):
        super().__init__()
        if parent is not None:
            self.setParent(parent)

        themes = Themes()
        self.themes = themes.items
        self._font_size = font_size
        self._bg = self.themes["app_color"]["white"]
        self._text_color = self.themes["app_color"]["text_foreground"]
        self._border_color = self.themes["app_color"]["green_two"]
        self._border_radius = border_radius

    def import_sheets(self, focused_style, unfocused_style):
        self._focused_style = focused_style
        self._unfocused_style = unfocused_style

    def configure_self(self):
        custom_focus_style = focused_line_edit.format(
            _font_size=self._font_size,
            _bg=self._bg,
            _text_color=self._text_color,
            _border_color=self._border_color,
            _border_radius=self._border_radius
        )

        custom_unfocused_style = unfocused_line_edit.format(
            _font_size=self._font_size,
            _text_color=self._text_color,
            _border_radius=self._border_radius
        )

        self.setStyleSheet(custom_focus_style)
        self.import_sheets(custom_focus_style, custom_unfocused_style)

    def focusInEvent(self, event):
        self.parent().setStyleSheet(self._focused_style)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.parent().setStyleSheet(self._unfocused_style)
        super().focusOutEvent(event)
