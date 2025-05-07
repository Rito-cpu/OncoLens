from pathlib import Path
from src.core.app_config import EXCEL_EXTENSIONS
from src.core.pyqt_core import *
from src.core.image_functions import Functions
from src.core.json.json_themes import Themes
from src.gui.models.qt_line_button import QtButtonLineEdit
from src.gui.models.py_push_button import PyPushButton
from src.gui.models.qt_clickable_icon import QtMenuIcon
from src.gui.models.qt_message import QtMessage


class QtUploadMainWidget(QWidget):
    def __init__(
        self,
        font_size: int = 13,
        icon_size: int = 310,
        parent=None
    ):
        super().__init__(parent)
        if parent is not None:
            self.setParent(parent)

        themes = Themes()
        self.themes = themes.items
        self._font_size = font_size
        self._icon_size = icon_size
        self._icon_path = Functions.set_svg_icon("db_import.svg")
        self._current_path = None
        self._current_file = None

        self._setup_widget()
        self.enter_bttn.clicked.connect(self.enter_path)
        self.clear_bttn.clicked.connect(self.clear_path_entry)

    def _setup_widget(self):
        # Add your widget setup code here
        icon_frame = QFrame(self)
        icon_frame.setObjectName('icon_frame')
        icon_frame.setFrameShape(QFrame.Shape.NoFrame)
        icon_frame.setFrameShadow(QFrame.Shadow.Plain)

        #f4ac3c
        self.section_icon = QtMenuIcon(
            icon_name=self._icon_path,
            icon_size=self._icon_size,
            color=self.themes["app_color"]["dark_one"],
            set_checkable=False,
            parent=icon_frame
        )
        self.section_icon.setObjectName('sectional_icon')

        icon_layout = QVBoxLayout(icon_frame)
        icon_layout.setObjectName('icon_layout')
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.addWidget(self.section_icon, alignment=Qt.AlignmentFlag.AlignCenter)

        lower_frame = QFrame(self)
        lower_frame.setObjectName('lower_frame')
        lower_frame.setFrameShape(QFrame.Shape.NoFrame)
        lower_frame.setFrameShadow(QFrame.Shadow.Plain)

        file_interaction_frame = QFrame(lower_frame)
        file_interaction_frame.setObjectName('file_interaction_frame')
        file_interaction_frame.setFrameShape(QFrame.Shape.NoFrame)
        file_interaction_frame.setFrameShadow(QFrame.Shadow.Plain)
        file_interaction_frame.setStyleSheet(f"QFrame#file_interaction_frame{{border-radius: 8px; background: {self.themes['app_color']['bg_one']}}}")

        line_entry_frame = QFrame(file_interaction_frame)
        line_entry_frame.setObjectName('line_entry_frame')
        line_entry_frame.setFrameShape(QFrame.Shape.NoFrame)
        line_entry_frame.setFrameShadow(QFrame.Shadow.Plain)

        self.data_path_entry = QtButtonLineEdit(
            title="GDRS Data",
            title_color=self.themes["app_color"]["text_foreground"],
            color_three=self.themes["app_color"]["green_two"],
            top_margin=17,
            parent=line_entry_frame
        )
        self.data_path_entry.setObjectName("data_path_entry")
        self.data_path_entry.setMinimumWidth(350)

        button_frame = QFrame(line_entry_frame)
        button_frame.setObjectName('button_frame')
        button_frame.setFrameShape(QFrame.Shape.NoFrame)
        button_frame.setFrameShadow(QFrame.Shadow.Plain)

        self.clear_bttn = PyPushButton(
            text="Clear",
            radius=8,
            font_size=13,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent=button_frame
        )
        self.clear_bttn.setObjectName("clear_bttn")
        self.clear_bttn.setFixedSize(65, 33)

        self.enter_bttn = PyPushButton(
            text="Enter",
            radius=8,
            font_size=13,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent=button_frame
        )
        self.enter_bttn.setObjectName("submit_bttn")
        self.enter_bttn.setFixedSize(65, 33)

        button_layout = QHBoxLayout(button_frame)
        button_layout.setObjectName("button_layout")
        button_layout.setContentsMargins(0, 20, 0, 0)
        button_layout.setSpacing(7)
        button_layout.addWidget(self.clear_bttn, alignment=Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.enter_bttn, alignment=Qt.AlignmentFlag.AlignCenter)

        line_entry_layout = QHBoxLayout(line_entry_frame)
        line_entry_layout.setObjectName("line_entry_layout")
        line_entry_layout.setContentsMargins(50, 0, 50, 0)
        line_entry_layout.setSpacing(10)
        line_entry_layout.addWidget(self.data_path_entry)
        line_entry_layout.addWidget(button_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        path_results_frame = QFrame(file_interaction_frame)
        path_results_frame.setObjectName('path_results_frame')
        path_results_frame.setFrameShape(QFrame.Shape.NoFrame)
        path_results_frame.setFrameShadow(QFrame.Shadow.Plain)
        path_results_frame.setStyleSheet(f"QFrame#path_results_frame{{background: {self.themes['app_color']['bg_three']}; border-radius: 8px;}}")

        standard_text = QLabel(path_results_frame)
        standard_text.setObjectName('standard_text')
        standard_text.setText("Uploaded File: ")
        standard_text.setStyleSheet(f'font-size: {self._font_size}px; color: {self.themes["app_color"]["dark_three"]};')
        standard_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.path_leaf_file = QLabel(path_results_frame)
        self.path_leaf_file.setObjectName('path_leaf_file')
        self.path_leaf_file.setText("None")
        self.path_leaf_file.setStyleSheet(f'font-size: {self._font_size}px; color: {self.themes["app_color"]["dark_three"]}')
        self.path_leaf_file.setAlignment(Qt.AlignmentFlag.AlignCenter)

        path_results_layout = QHBoxLayout(path_results_frame)
        path_results_layout.setObjectName("path_results_layout")
        path_results_layout.setContentsMargins(10, 3, 3, 3)
        path_results_layout.setSpacing(13)
        path_results_layout.addWidget(standard_text, alignment=Qt.AlignmentFlag.AlignCenter)
        path_results_layout.addWidget(self.path_leaf_file, alignment=Qt.AlignmentFlag.AlignCenter)
        path_results_layout.addStretch(1)
        path_results_frame.setFixedHeight(path_results_layout.sizeHint().height() + 5)

        file_interaction_layout = QVBoxLayout(file_interaction_frame)
        file_interaction_layout.setObjectName('file_interaction_layout')
        file_interaction_layout.setContentsMargins(15, 15, 15, 15)
        file_interaction_layout.setSpacing(7)
        file_interaction_layout.addWidget(line_entry_frame)
        file_interaction_layout.addWidget(path_results_frame)
        file_interaction_frame.setFixedHeight(file_interaction_layout.sizeHint().height() + 10)

        self.submit_data_bttn = PyPushButton(
            text="Submit",
            radius=8,
            font_size=17,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent=lower_frame
        )
        self.submit_data_bttn.setObjectName("submit_data_bttn")
        self.submit_data_bttn.setFixedSize(110, 41)

        lower_layout = QVBoxLayout(lower_frame)
        lower_layout.setObjectName('lower_layout')
        lower_layout.setContentsMargins(0, 0, 0, 0)
        lower_layout.setSpacing(25)
        lower_layout.addWidget(file_interaction_frame)
        lower_layout.addWidget(self.submit_data_bttn, alignment=Qt.AlignmentFlag.AlignCenter)
        lower_frame.setFixedHeight(lower_layout.sizeHint().height() + 10)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 50, 30, 15)
        main_layout.setSpacing(60)
        main_layout.addWidget(icon_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(lower_frame)

    def enter_path(self):
        path_entry = self.data_path_entry.text()
        path_entry = Path(path_entry)

        _ = self.check_file_entry(path_entry)

    def clear_path_entry(self):
        self.data_path_entry.clear_text()
        self.path_leaf_file.setText("None")
        self._current_path = None
        self._current_file = None

    def get_data_path(self):
        return self._current_path
    
    def check_file_entry(self, entry: Path):
        exit_buttons = {
            "Ok": QMessageBox.ButtonRole.AcceptRole,
        }

        exit_message_box = QtMessage(
            buttons=exit_buttons,
            color=self.themes["app_color"]["white"],
            bg_color_one=self.themes["app_color"]["dark_one"],
            bg_color_two=self.themes["app_color"]["bg_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        exit_message_box.setIcon(QMessageBox.Icon.Critical)

        if entry.exists() and entry.is_file():
            extension = entry.suffix.lower()
            if extension in EXCEL_EXTENSIONS:
                self._current_path = entry
                self._current_file = entry.name
                self.path_leaf_file.setText(self._current_file)

                return True
            else:
                exit_message_box.setText("Incorrect type.")
                exit_message_box.setDetailedText("A file was found, but the file type is not supported. Please provide an excel file. ")
                exit_message_box.exec()
                self.clear_path_entry()

                return False
        else:
            exit_message_box.setText("No file found.")
            exit_message_box.setDetailedText(f"No file was found at the provided path. Please submit a valid file path of excel-type.")
            exit_message_box.exec()
            self.clear_path_entry()

            return False

    def submit_menu_data(self):
        # Evaluate from saved path
        if self._current_path is not None:
            valid_path = self.check_file_entry(self._current_path)
            if valid_path:
                return self.get_data_path()
            else:
                return None
        # Evaluate from provided line entry
        elif self._current_path is None and self.data_path_entry.text():
            line_entry = Path(self.data_path_entry.text())
            valid_path = self.check_file_entry(line_entry)
            if valid_path:
                return self.get_data_path()
            else:
                return None
        else:
            exit_buttons = {
                "Ok": QMessageBox.ButtonRole.AcceptRole,
            }

            exit_message_box = QtMessage(
                buttons=exit_buttons,
                color=self.themes["app_color"]["white"],
                bg_color_one=self.themes["app_color"]["dark_one"],
                bg_color_two=self.themes["app_color"]["bg_one"],
                bg_color_hover=self.themes["app_color"]["dark_three"],
                bg_color_pressed=self.themes["app_color"]["dark_four"]
            )
            exit_message_box.setIcon(QMessageBox.Icon.Critical)
            exit_message_box.setText("No file selected.")
            exit_message_box.setDetailedText("Please select an excel file to submit.")
            exit_message_box.exec()
            return None

