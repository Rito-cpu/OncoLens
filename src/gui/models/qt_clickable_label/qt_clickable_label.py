from src.core.pyqt_core import *
from src.core.json.json_themes import Themes


class QtClickableLabel(QLabel):
    clicked = pyqtSignal(str)

    def __init__(
        self,
        text: str,
        font_size: int = 11,
        font_color: str = "blue",
        underline: bool = True,
        italicized: bool = True,
        bold: bool = False,
        hyperlink_label: bool = True,
        parent=None
    ):
        super().__init__()

        if parent is not None:
            self.parent = parent

        self._text = text
        self._font_size = font_size
        self._font_color = font_color
        self._underline = 'underline' if underline else 'none'
        self._italicized = 'italic' if italicized else 'none'
        self._bold = 'bold' if bold else 'none'
        themes = Themes()
        self.themes = themes.items

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if hyperlink_label:
            self.setStyleSheet(f"""
                QLabel{{
                    background: none;
                    border: none;
                    color: {self._font_color};
                    font-size: {self._font_size}px;
                    font-style: {self._italicized};
                    text-decoration: {self._underline};
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QLabel{{
                    background: none;
                    border: none;
                    color: {self.themes['app_color']['dark_three']};
                    font-size: {self._font_size}px;
                    font-weight: {self._bold};
                }}
            """)
            self.setText(text)

    def setHyperLink(self, new_link: str):
        self.setText(f"<a href='{new_link}'>{self._text}</a>")

    def mousePressEvent(self, event):
        self.clicked.emit(self.objectName())
        return super().mousePressEvent(event)