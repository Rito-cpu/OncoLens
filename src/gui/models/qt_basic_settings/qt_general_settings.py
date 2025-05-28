from functools import partial
from src.core.pyqt_core import *
from src.gui.models import *
from src.gui.models.qt_line_button.qt_button_line_edit import QtButtonLineEdit
from .styles import *


class GeneralSettings(QGroupBox):
    apply = pyqtSignal()

    def __init__(self,
                title: str="General Settings",
                file: str=None,
                font_size: int=14,
                header_size: int=17,
                header_color: str="black",
                bg_color: str="rgba(29, 209, 167, 255)",
                border_radius: int=13,
                top_margin: int=23,
                color="black",
                left_margin: int=23,
                toggle_bg_color: str="black",
                circle_color: str="white",
                active_color: str="lightblue",
                parent=None):
        super().__init__()

        if parent != None:
            self.setParent(parent)

        groupbox_style = general_groupbox.format(
            _font_size=header_size,
            _bg_color=bg_color,
            _border_radius=border_radius,
            _top_margin=top_margin,
            _color=color,
            _left_margin=left_margin
        )
        self.setStyleSheet(groupbox_style)
        self.setTitle(title)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self._file = file
        self._font_size = font_size
        self._header_color = header_color
        self._toggle_bg_color = toggle_bg_color
        self._circle_color = circle_color
        self._active_color = active_color

        self.setup_widget()

        self.apply_button.clicked.connect(self.apply_clicked)

    def setup_widget(self):
        content_widget = QWidget(self)
        content_widget.setObjectName(u"content_widget")
        # content_widget.setFixedHeight(125)

        clean_label = QLabel(text="Clean Lesions:")
        clean_label.setStyleSheet(data_template.format(_font_size=self._font_size))

        self._clean_lesions_toggle = PyToggle(
            width=34,
            height=20,
            ellipse_y=2,
            bg_color = self._toggle_bg_color,
            circle_color = self._circle_color,
            active_color = self._active_color
        )
        self._clean_lesions_toggle.setChecked(False)
        self._clean_lesions_toggle.setCursor(Qt.CursorShape.PointingHandCursor)

        lesion_form_layout = QFormLayout()
        lesion_form_layout.addRow(clean_label, self._clean_lesions_toggle)

        form_layout = QHBoxLayout()
        form_layout.addLayout(lesion_form_layout)

        label_style = current_file_template.format(
            _font_size=12,
            _bg_color="rgba(255, 255, 255, 175)",
            _border_radius=9
        )
        self._file_in_use = QLabel("<b>Current Patient File:</b> {}".format(self._file))
        self._file_in_use.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._file_in_use.setStyleSheet(label_style)

        self.saved_settings_line = QtButtonLineEdit(
            title="Settings File",
            title_color=self._toggle_bg_color,
            border_color=self._active_color,
            color_three=self._active_color,
            top_margin=19,
            parent=content_widget
        )
        self.saved_settings_line.setObjectName(u"saved_settings_line")

        self.apply_button = PyPushButton(
            text="Apply",
            radius=8,
            color=self._circle_color,
            bg_color=self._toggle_bg_color,
            bg_color_hover=self._toggle_bg_color,
            bg_color_pressed=self._toggle_bg_color,
            parent=content_widget
        )
        self.apply_button.setObjectName(u"apply_button")
        self.apply_button.setFixedSize(65, 31)

        apply_bttn_holder = QVBoxLayout()
        apply_bttn_holder.setObjectName(u'apply_bttn_holder')
        apply_bttn_holder.setContentsMargins(0, 22, 0, 0)
        apply_bttn_holder.addWidget(self.apply_button, alignment=Qt.AlignmentFlag.AlignCenter)

        line_edit_layout = QHBoxLayout()
        line_edit_layout.setContentsMargins(50, 0, 50, 0)
        line_edit_layout.setSpacing(25)
        line_edit_layout.addWidget(self.saved_settings_line)
        line_edit_layout.addLayout(apply_bttn_holder)

        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(25)
        content_layout.addLayout(form_layout)
        content_layout.addLayout(line_edit_layout)
        content_layout.addWidget(self._file_in_use)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(17, 17, 17, 17)
        main_layout.setSpacing(5)
        main_layout.addWidget(content_widget)

        self.setFixedHeight(250)

    def set_patient_file(self, new_text: str):
        self._file = new_text
        self._file_in_use.setText("<b>Current Patient File:</b> {}".format(new_text))

    def set_clean_lesions(self):
        self._clean_lesions_toggle.setChecked(True)

    def get_patient_file(self):
        return self._file

    def get_settings_file(self):
        return self.saved_settings_line.text()

    def get_data_dictionary(self) -> dict:
        general_settings_dict = {
            "file": self.get_patient_file(),
            "clean_lesions": self._clean_lesions_toggle.isChecked()
        }

        return general_settings_dict

    def apply_clicked(self):
        self.apply.emit()
