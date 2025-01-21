from src.core.pyqt_core import *
from src.core.app_config import IMG_RSC_PATH
from .styles import box_template


class QtNumEntry(QDoubleSpinBox):
    def __init__(self,
                font_size: int=11,
                font_color: str="white",
                bg_color: str="lightblue",
                parent=None
                ):
        super().__init__()
        if parent != None:
            self.setParent(parent)

        self.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setFixedSize(55, 28)

        self._font_size = font_size
        self._font_color = font_color
        self._bg_color = bg_color

        self.set_style()

    def set_style(self):
        box_style = box_template.format(
            _font_size=self._font_size,
            _color=self._font_color,
            _border_color=self._font_color,
            _bg_color=self._bg_color,
            _img_path=IMG_RSC_PATH
        )

        self.setStyleSheet(box_style)
