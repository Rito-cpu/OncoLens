import pathlib
import pandas as pd

from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.gui.models.py_push_button import PyPushButton
from src.gui.models.qt_line_button import QtButtonLineEdit
from src.gui.models.qt_message import QtMessage


class QtAbstractFileEntry(QWidget):
    change_scene = pyqtSignal(dict)

    def __init__(
        self,
        font_size: int = 12,
        parent=None
    ):
        super().__init__(parent)

        if parent is not None:
            self.setParent(parent)

        themes = Themes()
        self.themes = themes.items
        self.title = "Abstract Data Upload"
        self._font_size = font_size
        self._valid_extensions = [".csv", ".xlsx", ".xls"]

        self._setup_widget()
        self.submit_data_bttn.clicked.connect(self.validate_entry)
        self.clear_bttn.clicked.connect(self.clear_entry)
        self.enter_bttn.clicked.connect(self.update_text)

    def _setup_widget(self):
        overall_frame = QFrame(self)
        overall_frame.setObjectName('overall_frame')
        overall_frame.setFrameShape(QFrame.Shape.NoFrame)
        overall_frame.setFrameShadow(QFrame.Shadow.Plain)
        
        file_interaction_frame = QFrame(overall_frame)
        file_interaction_frame.setObjectName('file_interaction_frame')
        file_interaction_frame.setFrameShape(QFrame.Shape.NoFrame)
        file_interaction_frame.setFrameShadow(QFrame.Shadow.Plain)
        file_interaction_frame.setStyleSheet(f"QFrame#file_interaction_frame{{border-radius: 8px; background: {self.themes['app_color']['bg_one']}}}")

        line_entry_frame = QFrame(file_interaction_frame)
        line_entry_frame.setObjectName('line_entry_frame')
        line_entry_frame.setFrameShape(QFrame.Shape.NoFrame)
        line_entry_frame.setFrameShadow(QFrame.Shadow.Plain)

        self.data_path_entry = QtButtonLineEdit(
            title="Data File",
            title_color=self.themes["app_color"]["text_foreground"],
            color_three=self.themes["app_color"]["green_two"],
            top_margin=17,
            mode="file",
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
            color=self.themes["app_color"]["bg_three"],
            bg_color=self.themes["app_color"]["icon_color"],
            bg_color_hover=self.themes["app_color"]["icon_hover"],
            bg_color_pressed=self.themes["app_color"]["icon_pressed"],
            parent=button_frame
        )
        self.clear_bttn.setObjectName("clear_bttn")
        self.clear_bttn.setFixedSize(65, 33)

        self.enter_bttn = PyPushButton(
            text="Enter",
            radius=8,
            font_size=13,
            color=self.themes["app_color"]["bg_three"],
            bg_color=self.themes["app_color"]["icon_color"],
            bg_color_hover=self.themes["app_color"]["icon_hover"],
            bg_color_pressed=self.themes["app_color"]["icon_pressed"],
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
        standard_text.setStyleSheet(f'color: {self.themes["app_color"]["text_foreground_two"]}; font-size: {self._font_size}px;')
        standard_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.path_leaf_file = QLabel(path_results_frame)
        self.path_leaf_file.setObjectName('path_leaf_file')
        self.path_leaf_file.setText("None")
        self.path_leaf_file.setStyleSheet(f'color: {self.themes["app_color"]["text_foreground_two"]}; font-size: {self._font_size}px;')
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
            text="Process",
            radius=8,
            font_size=17,
            color=self.themes["app_color"]["text_foreground_two"],
            bg_color=self.themes["app_color"]["green_two"],
            bg_color_hover=self.themes["app_color"]["green"],
            bg_color_pressed=self.themes["app_color"]["green"],
            parent=overall_frame
        )
        self.submit_data_bttn.setObjectName("submit_data_bttn")
        self.submit_data_bttn.setFixedSize(110, 41)

        overall_layout = QVBoxLayout(overall_frame)
        overall_layout.setContentsMargins(0, 0, 0, 0)
        overall_layout.setSpacing(25)
        overall_layout.addWidget(file_interaction_frame)
        overall_layout.addWidget(self.submit_data_bttn, alignment=Qt.AlignmentFlag.AlignCenter)
        overall_frame.setFixedHeight(overall_layout.sizeHint().height() + 10)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(overall_frame)
        
    def clear_entry(self):
        self.data_path_entry.clear_text()
        self.path_leaf_file.setText("None")

    def update_text(self):
        self.path_leaf_file.setText(self.data_path_entry.text())

    def gather_data(self, file_path: pathlib.Path, suffix: str):
        settings = {
            "is_excel": False,
            "sheets": None,
            "excel_obj": None,
            "dtypes": None,
            "fields": None,
            "max_cols": None
        }
        max_cols = None

        if suffix == ".csv":
            main_df = pd.read_csv(str(file_path))
        else:
            main_df = pd.read_excel(str(file_path))
            excel_df = pd.ExcelFile(str(file_path))
            sheet_names = excel_df.sheet_names
            for sheet in sheet_names:
                sheet_df = pd.read_excel(str(file_path), sheet_name=sheet)
                if max_cols is None or len(list(sheet_df.columns)) > max_cols:
                    max_cols = len(list(sheet_df.columns))
            settings["is_excel"] = True
            settings["sheets"] = sheet_names
            settings["excel_obj"] = excel_df
        dtypes = main_df.dtypes.to_dict()
        cols = list(main_df.columns)
        if max_cols is None:
            max_cols = len(cols)
        settings["max_cols"] = max_cols
        settings["fields"] = cols
        settings["dtypes"] = dtypes

        return settings

    def validate_entry(self):
        msg_bttns = {
            "Ok": QMessageBox.ButtonRole.AcceptRole,
        }

        msg_box = QtMessage(
            buttons=msg_bttns,
            color=self.themes["app_color"]["white"],
            bg_color_one=self.themes["app_color"]["dark_one"],
            bg_color_two=self.themes["app_color"]["bg_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        msg_box.setIcon(QMessageBox.Icon.Critical)

        path_entry = pathlib.Path(self.data_path_entry.text())

        if self.data_path_entry.text() == "":
            # Empty text
            msg_box.setText("Empty submission.")
            msg_box.setDetailedText("No text detected. Please provide a full path pointing towards an existing CSV or Excel file to plot.")
            msg_box.exec()
            return
        elif not path_entry.exists():
            # Account for any other error
            msg_box.setText("Encountered error.")
            msg_box.setDetailedText("Submission caused an unexpected error. Please provide a valid file-path of type CSV or Excel.")
            msg_box.exec()
            return
        else:
            if path_entry.is_dir():
                msg_box.setText("Directory provided.")
                msg_box.setDetailedText("Directory path detected. Please provide a full path pointing towards an existing CSV or Excel file to plot.")
                msg_box.exec()
                return
            else:
                # File submission only
                file_extension = path_entry.suffix
                if file_extension not in self._valid_extensions:
                    msg_box.setText("Invalid file type.")
                    msg_box.setDetailedText(f"Unsupported file of type \"{file_extension}\" detected. Please provide a valid data file of type:\n{self._valid_extensions}")
                    msg_box.exec()
                    return
                
                file_settings = self.gather_data(path_entry, file_extension)

                self.change_scene.emit(file_settings)
