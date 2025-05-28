from src.core.pyqt_core import *
from src.core.json.json_themes import Themes


class QtAbstractPlot(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        if parent is not None:
            self.setParent(parent)

        themes = Themes()
        self.themes = themes.items
        self.title = "Abstract Plot Visual"

        self._setup_widget()

    def _setup_widget(self):
        overall_frame = QFrame(self)
        overall_frame.setObjectName('overall_frame')
        overall_frame.setFrameShape(QFrame.Shape.NoFrame)
        overall_frame.setFrameShadow(QFrame.Shadow.Plain)

        overall_layout = QVBoxLayout(overall_frame)
        overall_layout.setContentsMargins(0, 0, 0, 0)
        overall_layout.setSpacing(15)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(overall_frame)
