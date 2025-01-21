import os

from src.core.pyqt_core import *
from src.core.keyword_store import NO_CONE, COMPARISON_CONE
from src.core.app_config import IMG_RSC_PATH
from src.core.json.json_themes import Themes
from src.gui.models.py_push_button import PyPushButton
from src.gui.models.qt_settings_box.qt_cone_settings import ConeSettings
from .qt_comparison_widget import QtComparisonConeWidget
from .styles import frame_template


class QtConeDialog(QDialog):
    def __init__(
            self,
            lesion_names: list[str],
            treatments: dict,
            bg_color_one: str="lightgray",
            bg_color_two: str="black",
            hover_color: str="black",
            pressed_color: str="black",
            text_color_one: str="black",
            text_color_two: str="white",
            font_size: int=14,
            load_data: dict=None,
            parent=None
        ):
        super(QtConeDialog, self).__init__(parent)

        if parent != None:
            self.setParent(parent)

        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)

        # *** Handle Argument Variables ***
        self._lesion_names = lesion_names
        self._treatments = treatments
        self._bg_color_one = bg_color_one
        self._bg_color_two = bg_color_two
        self._hover_color = hover_color
        self._pressed_color = pressed_color
        self._text_color_one = text_color_one
        self._text_color_two = text_color_two
        self._font_size = font_size
        self._load_data = load_data

        themes = Themes()
        self.themes = themes.items

        self.setMinimumSize(725, 550)

        self.setup_widget()
        if self._load_data:
            self.load_settings()

        # add slots/signals
        self._comparison_cone_radio.toggled.connect(self.show_comparison_settings)
        self._ok_button.clicked.connect(self.accept)
        self._cancel_button.clicked.connect(self.reject)

    def setup_widget(self):
        dialog_style = frame_template.format(
            _bg_color=self._bg_color_one,
            _label_color=self._text_color_one,
            _label_size=self._font_size
        )
        self.setStyleSheet(dialog_style)

        header_frame = QFrame(self)
        header_frame.setObjectName("header_frame")
        header_frame.setFrameShape(QFrame.Shape.NoFrame)
        header_frame.setFrameShadow(QFrame.Shadow.Raised)
        header_frame.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        cone_header = QLabel(header_frame)
        cone_header.setText("Cone Type")
        cone_header.setObjectName("cone_header")
        cone_header.setStyleSheet("color: {_color}; font-size: {_font_size}px; font-weight: bold;".format(_color=self._text_color_one, _font_size=18))
        cone_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_layout = QHBoxLayout(header_frame)
        header_layout.addWidget(cone_header)

        container_frame = QFrame()
        container_frame.setObjectName("container_frame")
        container_frame.setFrameShape(QFrame.Shape.NoFrame)
        container_frame.setFrameShadow(QFrame.Shadow.Raised)

        # **** No Cone Radio option ****
        self._no_cone_radio = QRadioButton(container_frame)
        self._no_cone_radio.setObjectName("no_cone_radio")
        self._no_cone_radio.setText(NO_CONE)
        self._no_cone_radio.setChecked(True)
        self._no_cone_radio.setCursor(Qt.CursorShape.PointingHandCursor)

        # **** Comparison Cone Radio option ****
        self._comparison_cone_radio = QRadioButton(container_frame)
        self._comparison_cone_radio.setObjectName("comparison_cone_radio")
        self._comparison_cone_radio.setText(COMPARISON_CONE)
        self._comparison_cone_radio.setChecked(False)
        self._comparison_cone_radio.setCursor(Qt.CursorShape.PointingHandCursor)

        self._comparison_cone_settings = QtComparisonConeWidget(
            lesion_names=self._lesion_names,
            treatments=self._treatments,
            num_lesions=len(self._lesion_names),
            num_drugs=len(self._treatments),
            bg_color=self._bg_color_two,
            text_color=self._text_color_two,
            parent=container_frame
        )
        self._comparison_cone_settings.hide()

        # **** LHS Sampling data ****
        sampling_box = QFrame(container_frame)
        sampling_box.setFrameShape(QFrame.Shape.NoFrame)
        sampling_box.setFrameShadow(QFrame.Shadow.Raised)

        self._num_samples_lhs = QSpinBox(sampling_box)
        self._num_samples_lhs.setMinimum(1)
        self._num_samples_lhs.setValue(10)

        lhs_samples_label = QLabel("Number of Samples (LHS): ", sampling_box)

        self._n_lhs = QFrame(sampling_box)
        self._n_lhs.setFrameShape(QFrame.Shape.NoFrame)
        self._n_lhs.setFrameShadow(QFrame.Shadow.Raised)
        self._n_lhs.hide()

        lhs_lay = QHBoxLayout(self._n_lhs)
        lhs_lay.addStretch(1)
        lhs_lay.addWidget(lhs_samples_label)
        lhs_lay.addWidget(self._num_samples_lhs)
        lhs_lay.addStretch(1)

        self._num_samples_stratified = QSpinBox(sampling_box)
        self._num_samples_stratified.setMinimum(1)
        self._num_samples_stratified.setValue(10)

        stratified_samples_label = QLabel("Number of Samples (Stratified): ", sampling_box)

        self._n_stratified = QFrame(sampling_box)
        self._n_stratified.setFrameShape(QFrame.Shape.NoFrame)
        self._n_stratified.setFrameShadow(QFrame.Shadow.Raised)
        self._n_stratified.hide()

        stratified_lay = QHBoxLayout(self._n_stratified)
        stratified_lay.addStretch(1)
        stratified_lay.addWidget(stratified_samples_label)
        stratified_lay.addWidget(self._num_samples_stratified)
        stratified_lay.addStretch(1)

        sampling_box_layout = QHBoxLayout(sampling_box)
        sampling_box_layout.setContentsMargins(0, 0, 0, 0)
        sampling_box_layout.setSpacing(5)
        sampling_box_layout.addWidget(self._n_lhs)
        sampling_box_layout.addWidget(self._n_stratified)

        # **** Dialog Confirmation Buttons ****
        self._ok_button = PyPushButton(text="Ok",
            radius=8,
            color=self._text_color_two,
            bg_color=self._bg_color_two,
            bg_color_hover=self._hover_color,
            bg_color_pressed=self._pressed_color,
            parent=self
        )
        self._ok_button.setObjectName("ok_button")
        self._ok_button.setFixedSize(55, 35)
        self._ok_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self._cancel_button = PyPushButton(text="Cancel",
            radius=8,
            color=self._text_color_two,
            bg_color=self._bg_color_two,
            bg_color_hover=self._hover_color,
            bg_color_pressed=self._pressed_color,
            parent=self
        )
        self._cancel_button.setObjectName("cancel_button")
        self._cancel_button.setFixedSize(55, 35)
        self._cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self._button_box = QDialogButtonBox(self)
        self._button_box.addButton(self._ok_button, QDialogButtonBox.ButtonRole.AcceptRole)
        self._button_box.addButton(self._cancel_button, QDialogButtonBox.ButtonRole.RejectRole)

        # **** Setting Layouts ****
        frame_layout = QVBoxLayout(container_frame)
        frame_layout.setContentsMargins(5, 10, 5, 10)
        frame_layout.setSpacing(50)
        frame_layout.addWidget(self._no_cone_radio)
        frame_layout.addWidget(self._comparison_cone_radio)
        frame_layout.addWidget(self._comparison_cone_settings, alignment=Qt.AlignmentFlag.AlignCenter)
        frame_layout.addWidget(sampling_box)

        scroll_area = QScrollArea(self)
        scroll_area.setObjectName(u"scroll_area")
        scroll_area.setWidgetResizable(True)
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setWidget(container_frame)
        scroll_area.setStyleSheet("""
            QScrollArea {{
                background: {bg};
                border: none;
                border-radius: 8px;
            }}
        """.format(bg=self.themes['app_color']['bg_two']))

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.addWidget(header_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(self._button_box)

    def show_comparison_settings(self, is_toggled):
        if is_toggled:
            self._comparison_cone_settings.show()
        else:
            self._comparison_cone_settings.hide()

    def show_sampling(self, is_toggled):
        if is_toggled:
            self._n_lhs.hide()
            self._n_stratified.hide()
        else:
            self._n_lhs.show()
            self._n_stratified.show()

    def get_selected_cone_type(self):
        if self._no_cone_radio.isChecked():
            return NO_CONE
        else:
            return COMPARISON_CONE

    def get_data(self):
        if self._no_cone_radio.isChecked():
            return None
        else:
            # *** Gather cone rates and target lesion ***
            data = self._comparison_cone_settings.get_comparison_settings()

            return data

    def get_sampling(self):
        if self._no_cone_radio.isChecked():
            return None
        else:
            sampling = {
                "n_lhs": self._num_samples_lhs.value(),
                "n_stratified": self._num_samples_stratified.value()
            }

            return sampling

    def get_average_values(self):
        return self._comparison_cone_settings.get_average_values()

    def submit_method_data(self):
        method = self.get_selected_cone_type()
        data = self.get_data()

        if not data:
            method = NO_CONE

        return method, data

    def load_settings(self):
        # TODO:Implement load settings
        # print(self._load_data)

        if self._load_data["method"] == COMPARISON_CONE:
            pass
            # print(f"Opted to load in targeted settings: need to configure what to do.")
