from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.gui.models.py_push_button import PyPushButton
from .qt_general_settings import GeneralSettings
from .qt_settings_frame import SettingsGroupBox


class QtBasicSettingsWidget(QWidget):
    def __init__(
        self,
        parent=None
    ):
        super().__init__(parent)
        
        if parent is not None:
            self.setParent(parent)

        themes = Themes()
        self.themes = themes.items

        self._setup_widget()

    def _setup_widget(self):
        outer_frame = QFrame(self)
        outer_frame.setObjectName("outer_frame")
        outer_frame.setFrameShape(QFrame.Shape.NoFrame)
        outer_frame.setFrameShadow(QFrame.Shadow.Plain)

        self.general_settings_box = GeneralSettings(
            header_color=self.themes["app_color"]["dark_four"],
            toggle_bg_color=self.themes["app_color"]["dark_two"],
            circle_color=self.themes["app_color"]["white"],    # icon_color
            active_color=self.themes["app_color"]["context_color"],
            parent=outer_frame
        )
        self.general_settings_box.setObjectName(u"general_groupbox")
        # self.general_groupbox.apply.connect(lambda: MainFunctions.load_etb_settings(self))

        self.lesion_scans_box = SettingsGroupBox(
            title="  Lesion Settings",
            color=self.themes["app_color"]["dark_one"],
            parent=outer_frame
        )
        self.lesion_scans_box.setObjectName("lesion_groupbox")
        self.lesion_scans_box.set_empty()

        self.historical_treatments_box = SettingsGroupBox(
            title="  Historical Treatments",
            color=self.themes["app_color"]["dark_one"],
            parent=outer_frame
        )
        self.historical_treatments_box.setObjectName("historical_groupbox")
        self.historical_treatments_box.set_empty()

        self.available_treatments_box = SettingsGroupBox(
            title="  Available Treatments",
            color=self.themes["app_color"]["dark_one"],
            parent=outer_frame
        )
        self.available_treatments_box.setObjectName("available_groupbox")
        self.available_treatments_box.set_empty()

        outer_layout = QVBoxLayout(outer_frame)
        outer_layout.setObjectName("outer_layout")
        outer_layout.setContentsMargins(0, 0, 0, 0)
        
        self.submit_parameters_bttn = PyPushButton(
            text="Submit",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            font_size=14,
            parent=self
        )
        self.submit_parameters_bttn.setObjectName(u"submit_parameters_bttn")
        self.submit_parameters_bttn.setMinimumSize(120, 40)
        self.submit_parameters_bttn.clicked.connect(self.start_table_window)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(outer_frame)

    def collapse_settings(self):
        if self.lesion_scans_box.is_expanded():
            self.lesion_scans_box.collapse_widget()
        if self.historical_treatments_box.is_expanded():
            self.historical_treatments_box.collapse_widget()
        if self.available_treatments_box.is_expanded():
            self.available_treatments_box.collapse_widget()
