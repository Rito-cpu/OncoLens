from pathlib import Path
from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.gui.models.qt_line_button import QtButtonLineEdit
from src.gui.models.py_push_button import PyPushButton


class QtUploadArea(QWidget):
    def __init__(
        self,
        parent=None
    ):
        super().__init__()
        if parent is not None:
            self.setParent(parent)
        
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        themes = Themes()
        self.themes = themes.items
        self.collapsed_description = """Upload patient biological dataset here. Please ensure that the dataset follows proper formatting to be successfuly received. Click to expand."""
        self.expanded_description = """"""

        self._setup_widget()
        self.enter_file_bttn.clicked.connect(self.file_entry_submitted)
        self.clear_file_button.clicked.connect(self.clear_file_submission)

    def _setup_widget(self):
        upload_frame = QFrame(self)
        upload_frame.setObjectName("upload_frame")
        upload_frame.setFrameShape(QFrame.Shape.NoFrame)
        upload_frame.setFrameShadow(QFrame.Shadow.Plain)
        upload_frame.setStyleSheet(f"""
            QFrame#upload_frame {{
                background: {self.themes['app_color']['white']};
                border: none;
                border-radius: 8px;
            }}
        """)

        file_entry_frame = QFrame(upload_frame)
        file_entry_frame.setObjectName("file_entry_frame")
        file_entry_frame.setFrameShape(QFrame.Shape.NoFrame)
        file_entry_frame.setFrameShadow(QFrame.Shadow.Plain)

        self.etb_file_entry = QtButtonLineEdit(
            title="File Search",
            title_color=self.themes["app_color"]["text_foreground"],
            top_margin=19,
            parent=file_entry_frame
        )
        self.etb_file_entry.setObjectName("etb_file_entry")
        #self.etb_file_entry.setMinimumWidth(350)

        button_container = QFrame(file_entry_frame)
        button_container.setObjectName("button_container")
        button_container.setFrameShape(QFrame.Shape.NoFrame)
        button_container.setFrameShadow(QFrame.Shadow.Plain)

        self.clear_file_button = PyPushButton(
            text="Clear",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            font_size=14,
            parent=button_container
        )
        self.clear_file_button.setObjectName("clear_file_button")
        self.clear_file_button.setFixedSize(65, 33)

        self.enter_file_bttn = PyPushButton(
            text="Enter",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            font_size=14,
            parent=button_container
        )
        self.enter_file_bttn.setObjectName("enter_file_bttn")
        self.enter_file_bttn.setFixedSize(65, 33)

        button_container_layout = QHBoxLayout(button_container)
        button_container_layout.setObjectName("button_container_layout")
        button_container_layout.setContentsMargins(0, 18, 0, 0)
        button_container_layout.setSpacing(7)
        button_container_layout.addWidget(self.clear_file_button)
        button_container_layout.addWidget(self.enter_file_bttn)

        file_entry_layout = QHBoxLayout(file_entry_frame)
        file_entry_layout.setObjectName("file_entry_layout")
        file_entry_layout.setContentsMargins(40, 0, 15, 0)
        file_entry_layout.addWidget(self.etb_file_entry)
        file_entry_layout.addWidget(button_container)

        file_label_container = QFrame(upload_frame)
        file_label_container.setObjectName("file_label_container")
        file_label_container.setFrameShape(QFrame.Shape.NoFrame)
        file_label_container.setFrameShadow(QFrame.Shadow.Plain)
        file_label_container.setStyleSheet(f"""
            QFrame#file_label_container {{
                background: {self.themes['app_color']['dark_three']};
                border-radius: 6px;
            }}
        """)

        intro_text = QLabel(file_label_container)
        intro_text.setObjectName("intro_text")
        intro_text.setStyleSheet(f"color: {self.themes['app_color']['white']}; font-size: 12px;")
        intro_text.setText("Uploaded File:")
        intro_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.uploaded_file_label = QLabel(file_label_container)
        self.uploaded_file_label.setObjectName("uploaded_file_label")
        self.uploaded_file_label.setStyleSheet(f"color: {self.themes['app_color']['white']}; font-size: 12px; font-weight: bold;")
        self.uploaded_file_label.setText("None")
        self.uploaded_file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        file_label_layout = QHBoxLayout(file_label_container)
        file_label_layout.setObjectName("file_label_layout")
        file_label_layout.setContentsMargins(5, 3, 3, 3)
        file_label_layout.setSpacing(8)
        file_label_layout.addWidget(intro_text, alignment=Qt.AlignmentFlag.AlignLeft)
        file_label_layout.addWidget(self.uploaded_file_label, alignment=Qt.AlignmentFlag.AlignLeft)
        file_label_layout.addStretch(1)
        file_label_container.setFixedSize(400, file_label_layout.sizeHint().height() + 5)

        upload_layout = QVBoxLayout(upload_frame)
        upload_layout.setObjectName("upload_layout")
        upload_layout.setContentsMargins(10, 10, 10, 10)
        upload_layout.setSpacing(15)
        upload_layout.addStretch(1)
        upload_layout.addWidget(file_entry_frame)
        upload_layout.addWidget(file_label_container, alignment=Qt.AlignmentFlag.AlignCenter)
        upload_layout.addStretch(1)

        main_layout = QVBoxLayout(self)
        main_layout.setObjectName("main_layout")
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(upload_frame)

    def file_entry_submitted(self):
        file_path = self.etb_file_entry.text()
        file_path = Path(file_path)

        if file_path.exists() and file_path != "":
            self._data_file_path = file_path
            uploaded_file_name = file_path.name
            self.uploaded_file_label.setText(uploaded_file_name)

    def clear_file_submission(self):
        self._data_file_path = None
        self.uploaded_file_label.setText("None")
        self.etb_file_entry.clear_text()

    def get_collapsed_description(self):
        return self.collapsed_description
    
    def get_expanded_description(self):
        return self.expanded_description
