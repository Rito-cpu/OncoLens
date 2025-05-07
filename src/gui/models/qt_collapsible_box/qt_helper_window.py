from PyQt6.QtGui import QCloseEvent
from src.core.pyqt_core import *
from src.core.json.json_themes import Themes


class QtHelperWindow(QWidget):
    closed = pyqtSignal(bool)

    def __init__(
        self,
        setting_name: str,
        setting_msg: str,
        font_size: int = 12,
        parent=None
    ):
        super().__init__()

        if parent is not None:
            self.setParent(parent)

        self.setWindowTitle("Setting Information")
        self.setMinimumSize(400, 300)
        self.setMaximumSize(600, 380)

        self._setting_name = setting_name
        self._setting_msg = setting_msg
        self._font_size = font_size

        themes = Themes()
        self.themes = themes.items

        self._setup_widget()

    def _setup_widget(self):
        background_frame = QFrame(self)
        background_frame.setObjectName('background_frame')
        background_frame.setFrameShape(QFrame.Shape.NoFrame)
        background_frame.setFrameShadow(QFrame.Shadow.Raised)
        background_frame.setStyleSheet(f'QFrame#background_frame {{background: {self.themes["app_color"]["white"]}; border: none}};')

        title_text = QLabel(background_frame)
        title_text.setObjectName('title_text')
        title_text.setText(f'{self._setting_name}')
        title_text.setStyleSheet(f'color: {self.themes["app_color"]["white"]}; font-size: 12px; background: {self.themes["app_color"]["bg_one"]}; border-radius: 8px; padding: 8px;')
        title_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.message_area = QTextEdit(background_frame)
        self.message_area.setObjectName('message_area')
        self.message_area.setReadOnly(True)
        self.message_area.setStyleSheet('border: none; border-radius: 8px; background: lightgray;')
        self.message_area.setText(self._setting_msg)
        self.message_area.setAlignment(Qt.AlignmentFlag.AlignCenter)

        frame_layout = QVBoxLayout(background_frame)
        frame_layout.setObjectName('frame_layout')
        frame_layout.setContentsMargins(25, 25, 25, 25)
        frame_layout.setSpacing(15)
        frame_layout.addWidget(title_text, alignment=Qt.AlignmentFlag.AlignCenter)
        frame_layout.addWidget(self.message_area)

        main_layout = QVBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(background_frame)

    def closeEvent(self, a0) -> None:
        self.closed.emit(True)
        return super().closeEvent(a0)
