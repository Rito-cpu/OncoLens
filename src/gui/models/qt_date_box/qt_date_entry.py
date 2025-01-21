from src.core.pyqt_core import *
from src.core.app_config import IMG_RSC_PATH
from .styles import date_template


class QtDateEntry(QDateEdit):
    def __init__(self,
                color_one: str="black",
                color_two: str="white",
                font_size: int=11,
                parent=None):
        super().__init__()
        if parent != None:
            self.setParent(parent)

        self._color_one = color_one
        self._color_two = color_two
        self._font_size = font_size

        self.setFixedSize(100, 25)
        self.setCalendarPopup(True)
        self.setDisplayFormat("MM/dd/yyyy")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # **** Set Style Sheet ****
        self.set_style()

    def set_style(self):
        date_style = date_template.format(
            _font_size=11,
            _main_bg=self._color_one,
            _color=self._color_two,
            _img_path=IMG_RSC_PATH,
            _border_radius=8
        )
        self.setStyleSheet(date_style)
