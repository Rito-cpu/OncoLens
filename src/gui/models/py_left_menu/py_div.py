from src.core.pyqt_core import *

# CUSTOM LEFT MENU
class PyDiv(QWidget):
    def __init__(self, color):
        super().__init__()

        self.frame_line = QFrame()
        self.frame_line.setStyleSheet(f"background: {color};")
        self.frame_line.setMaximumHeight(1)
        self.frame_line.setMinimumHeight(1)

        self._main_layout = QHBoxLayout(self)
        self._main_layout.setContentsMargins(5,0,5,0)
        self._main_layout.addWidget(self.frame_line)

        self.setMaximumHeight(1)
