from .qt_model_selection_area import QtModelSelectionArea
from .qt_upload_data_area import QtUploadArea
from pathlib import Path
from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.gui.models.qt_line_button import QtButtonLineEdit
from src.gui.models.qt_collapsible_box import QtSectionalWidget
from src.gui.models.py_push_button import PyPushButton


class QtEnhancedModelingMenu(QWidget):
    def __init__(
        self, 
        parent=None
    ):
        super().__init__()
        if parent is not None:
            self.setParent(parent)

        themes = Themes()
        self.themes = themes.items
        self._data_file_path = None

        self._setup_widget()

    def _setup_widget(self):
        ########################################
        #### Create the upload data section ####
        ########################################
        sectional_container = QFrame(self)
        sectional_container.setObjectName('sectional_container')
        sectional_container.setFrameShape(QFrame.Shape.NoFrame)
        sectional_container.setFrameShadow(QFrame.Shadow.Plain)
        sectional_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        #section_scroll_area.setWidget(sectional_house)

        upload_area = QtUploadArea()
        self.upload_data_sectional = QtSectionalWidget(
            section_title="Upload Dataset",
            icon_name="test_doc.svg",
            title_font=20,
            collapsed_info=upload_area.get_collapsed_description(),
            expanded_info=upload_area.get_expanded_description(),
            body_font=13,
            icon_size=63,
            use_custom_widget=upload_area,
            parent=self
        )

        ################################
        #### Create Model selection ####
        ################################
        model_area = QtModelSelectionArea()
        self.model_selection_sectional = QtSectionalWidget(
            section_title="Model Selection",
            icon_name="summation_icon.svg",
            title_font=20,
            collapsed_info=model_area.get_collapsed_description(),
            expanded_info=model_area.get_expanded_description(),
            custom_expanded_height=350,
            use_custom_widget=model_area,
            body_font=13,
            icon_size=63,
            parent=self
        )

        sectional_layout = QGridLayout(sectional_container)
        sectional_layout.setObjectName('sectional_layout')
        sectional_layout.setContentsMargins(80, 10, 80, 10)
        sectional_layout.setSpacing(25)
        sectional_layout.addWidget(self.upload_data_sectional)
        sectional_layout.addWidget(self.model_selection_sectional)

        self.submit_data_bttn = PyPushButton(
            text="Submit",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            font_size=18,
            parent=self
        )
        self.submit_data_bttn.setObjectName("submit_data_bttn")
        self.submit_data_bttn.setFixedSize(85, 40)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.addWidget(sectional_container)
        main_layout.addWidget(self.submit_data_bttn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)
