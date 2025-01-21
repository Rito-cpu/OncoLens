from src.core.pyqt_core import *
from src.core.json.json_themes import Themes


class QtModelSelector(QWidget):
    def __init__(
        self,
        parent=None
    ):
        super().__init__()
        if parent is not None:
            self.setParent(parent)

        self._setup_widget()

    def _setup_widget(self):
        main_layout = QVBoxLayout(self)

        self.setLayout(main_layout)
