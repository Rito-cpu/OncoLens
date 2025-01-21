from src.core.pyqt_core import *
from .styles import message_template
from src.gui.models import PyPushButton


class QtMessage(QMessageBox):
    def __init__(
        self,
        buttons: dict,
        color: str="white",
        bg_color_one: str="black",
        bg_color_two: str="gray",
        bg_color_hover: str="black",
        bg_color_pressed: str="black"
    ):
        super().__init__()

        self._border_radius = 11
        self._color = color
        self._bg_color = bg_color_one
        self._bg_color_hover = bg_color_hover
        self._bg_color_pressed = bg_color_pressed
        self._detailed_text_set = False

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setMask(self.get_mask())

        message_style = message_template.format(
            _bg=bg_color_two,
            _color=color
        )

        self.setStyleSheet(message_style)

        self.setup_widget(buttons)

    def setup_widget(self, buttons: dict):
        self.buttons = {}

        for text, role in buttons.items():
            button = PyPushButton(
                text=text,
                radius=8,
                color=self._color,
                bg_color=self._bg_color,
                bg_color_hover=self._bg_color_hover,
                bg_color_pressed=self._bg_color_pressed
            )
            button.setFixedSize(60, 30)
            self.addButton(button, role)
            self.buttons[text] = button

    def setDetailedText(self, text):
        super().setDetailedText(text)
        self._detailed_text_set = True

    def showEvent(self, event):
        super().showEvent(event)

        if self._detailed_text_set:
            child_bttns = self.findChildren(QPushButton)
            details_bttn = None

            for bttn in child_bttns:
                if bttn.text() == 'Show Details...':
                    details_bttn = bttn
                else:
                    normal_bttn = bttn

            if details_bttn:
                details_bttn.setCursor(Qt.CursorShape.PointingHandCursor)
                details_bttn.setStyleSheet(normal_bttn.default_template)
                details_bttn.setMinimumSize(120, 30)

    def get_mask(self):
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), self._border_radius, self._border_radius)
        return QRegion(path.toFillPolygon().toPolygon())

    def resizeEvent(self, event):
        self.setMask(self.get_mask())
        super().resizeEvent(event)
