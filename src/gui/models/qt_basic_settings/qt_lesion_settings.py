from functools import partial
from src.core.pyqt_core import *
from src.gui.models import *
from src.gui.models.qt_spinbox import QtNumEntry
from .styles import *
from src.core.json.json_themes import Themes


class LesionSettings(QWidget):
    def __init__(
            self,
            data_dict: dict,
            font_size: int=12,
            header_size: int=12,
            header_color: str="black",
            bg_color: str="black",
            circle_color: str="white",
            active_color: str="lightblue",
            default_plot = True,
            default_simulate = True,
            default_gamma = 0.03,
            default_gamma_mult = 1.0,
            default_delta_mult = 1.0,
            default_res_mult = 1.0,
            default_sens_mult = 1.0,
            default_offset = 0.0,
            parent=None
        ):
        super().__init__()

        themes = Themes()
        self.themes = themes.items

        self._font_size = font_size
        self._header_size = header_size
        self._header_color = header_color
        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color
        self._default_plot = default_plot
        self._default_simulate = default_simulate
        self._default_gamma = default_gamma
        self._default_gamma_mult = default_gamma_mult
        self._default_delta_mult = default_delta_mult
        self._default_res_mult = default_res_mult
        self._default_sens_mult = default_sens_mult
        self._default_offset = default_offset

        self.abbr_list = []
        self.plot_list = []
        self.simulate_list = []
        self.growth_list = []
        self.growth_mult_list = []
        self.drug_mult_list = []
        self.resistance_mult_list = []
        self.sensitivity_mult_list = []
        self.offset_list = []

        self._lesion_names = data_dict['names']
        self._lesion_abbr = data_dict['abbr']
        self._num_lesions = len(self._lesion_names)

        self.setup_widget()

        if parent != None:
            self.setParent(parent)

    def setup_widget(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(17, 17, 17, 17)
        main_layout.setSpacing(5)

        # --- Create Section Header Widgets ---
        name_header = QLabel('Name')
        name_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        plot_header = QLabel('Plot')
        plot_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        simulate_header = QLabel('Simulate')
        simulate_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        growth_header = QLabel('Growth')
        growth_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        growth_mult_header = QLabel('Growth (Mult)')
        growth_mult_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        efficacy_mult_header = QLabel('Drug (Mult)')
        efficacy_mult_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        resistance_mult_header = QLabel('Res. (Mult)')
        resistance_mult_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sensitivity_mult_header = QLabel('Sens. (Mult)')
        sensitivity_mult_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        offset_header = QLabel('Offset')
        offset_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_style = header_template.format(
            _header_color=self._header_color,
            _header_size=self._header_size
        )
        header_frame = QFrame(self)
        header_frame.setFrameShape(QFrame.Shape.NoFrame)
        header_frame.setFrameShadow(QFrame.Shadow.Raised)
        header_frame.setStyleSheet(header_style)

        header_layout = QGridLayout(header_frame)
        header_layout.setContentsMargins(10, 0, 10, 0)
        header_layout.setHorizontalSpacing(5)
        header_layout.addWidget(name_header, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(plot_header, 0, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(simulate_header, 0, 2, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(growth_header, 0, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(growth_mult_header, 0, 4, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(efficacy_mult_header, 0, 5, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(resistance_mult_header, 0, 6, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(sensitivity_mult_header, 0, 7, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(offset_header, 0, 8, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        content_widget = QWidget()
        content_widget.setObjectName(u"content_widget")
        content_widget.setStyleSheet("""
            QWidget#content_widget {
                background: transparent;
                border: none;
            }""")

        self._lesion_content_layout = QVBoxLayout(content_widget)
        # --- Loop through Lesions and create respective widget ---
        for index in range(self._num_lesions):
            lesion_widget = QWidget(content_widget)
            lesion_widget.setObjectName(u"lesion_widget")
            lesion_widget.setContentsMargins(0, 0, 0, 0)
            lesion_widget.setFixedHeight(43)
            custom_template = input_template.format(
                _object_name=lesion_widget.objectName(),
                _bg_color_two="rgba(215, 215, 215, 75)",
                _radius_two=20,
                _border_one="2px solid lightgray"
            )
            lesion_widget.setStyleSheet(custom_template)

            abbr_label = QLabel(text=self._lesion_abbr[index])
            abbr_label.setObjectName(u"abbr_label")
            abbr_label.setToolTip(self._lesion_names[index])
            abbr_label.setCursor(Qt.CursorShape.IBeamCursor)
            # abbr_label.setStyleSheet(data_template.format(_font_size=self._font_size))
            abbr_label.setStyleSheet("""
                    QWidget {{
                        font-size: {_font_size}px;
                        color: {_color};
                    }}
                """.format(_font_size=self._font_size, _color=self._header_color))
            self.abbr_list.append(abbr_label)

            plot_toggle = PyToggle(
                width=28,
                height=16,
                ellipse_y=2,
                bg_color = self._bg_color,
                circle_color = self._circle_color,
                active_color = self._active_color,
                parent=lesion_widget
            )
            plot_toggle.setObjectName(u"plot_toggle")
            plot_toggle.setChecked(True)
            plot_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
            self.plot_list.append(plot_toggle)

            simulate_toggle = PyToggle(
                width=28,
                height=16,
                ellipse_y=2,
                bg_color = self._bg_color,
                circle_color = self._circle_color,
                active_color = self._active_color,
                parent=lesion_widget
            )
            simulate_toggle.setObjectName(u"simulate_toggle")
            simulate_toggle.setChecked(True)
            simulate_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
            self.simulate_list.append(simulate_toggle)

            # Linking simulation checkbox to respective plot checkbox - cannot have a non-plotted lesion and simulate it too
            self.plot_list[-1].toggled.connect(partial(self.validate_linked_simulation, index))

            growth_box = QtNumEntry(
                font_size=self._font_size,
                bg_color=self.themes["app_color"]["dark_one"],
                parent=lesion_widget
            )
            growth_box.setObjectName(u"growth_box")
            growth_box.setDecimals(3)
            growth_box.setRange(0, 0.07)
            growth_box.setSingleStep(0.005)
            growth_box.setValue(0.03)
            self.growth_list.append(growth_box)

            growth_mult_box = QtNumEntry(
                font_size=self._font_size,
                bg_color=self.themes["app_color"]["dark_one"],
                parent=lesion_widget
            )
            growth_mult_box.setObjectName(u"growth_mult_box")
            growth_mult_box.setDecimals(2)
            growth_mult_box.setRange(0, 100)
            growth_mult_box.setSingleStep(0.5)
            growth_mult_box.setValue(1)
            self.growth_mult_list.append(growth_mult_box)

            efficacy_mult_box = QtNumEntry(
                font_size=self._font_size,
                bg_color=self.themes["app_color"]["dark_one"],
                parent=lesion_widget
            )
            efficacy_mult_box.setObjectName(u"efficacy_mult_box")
            efficacy_mult_box.setDecimals(2)
            efficacy_mult_box.setRange(0, 100)
            efficacy_mult_box.setSingleStep(0.5)
            efficacy_mult_box.setValue(1)
            self.drug_mult_list.append(efficacy_mult_box)

            resistance_mult_box = QtNumEntry(
                font_size=self._font_size,
                bg_color=self.themes["app_color"]["dark_one"],
                parent=lesion_widget
            )
            resistance_mult_box.setObjectName(u"resistance_mult_box")
            resistance_mult_box.setDecimals(2)
            resistance_mult_box.setRange(0, 100)
            resistance_mult_box.setSingleStep(0.5)
            resistance_mult_box.setValue(1)
            self.resistance_mult_list.append(resistance_mult_box)

            sensitivity_mult_box = QtNumEntry(font_size=self._font_size,
                                    bg_color=self.themes["app_color"]["dark_one"],
                                    parent=lesion_widget)
            sensitivity_mult_box.setObjectName(u"sensitivity_mult_box")
            sensitivity_mult_box.setDecimals(2)
            sensitivity_mult_box.setRange(0, 100)
            sensitivity_mult_box.setSingleStep(0.5)
            sensitivity_mult_box.setValue(1)
            self.sensitivity_mult_list.append(sensitivity_mult_box)

            offset_box = QtNumEntry(font_size=self._font_size,
                                    bg_color=self.themes["app_color"]["dark_one"],
                                    parent=lesion_widget)
            offset_box.setObjectName(u"offset_box")
            offset_box.setDecimals(2)
            offset_box.setRange(-10, 10)
            offset_box.setSingleStep(0.5)
            offset_box.setValue(0)
            self.offset_list.append(offset_box)

            parameter_layout = QGridLayout(lesion_widget)
            parameter_layout.setObjectName(u"parameter_layout")
            parameter_layout.setContentsMargins(0, 0, 0, 0)
            parameter_layout.setHorizontalSpacing(5)
            parameter_layout.setVerticalSpacing(5)
            parameter_layout.addWidget(abbr_label, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            parameter_layout.addWidget(plot_toggle, 0, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            parameter_layout.addWidget(simulate_toggle, 0, 2, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            parameter_layout.addWidget(growth_box, 0, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            parameter_layout.addWidget(growth_mult_box, 0, 4, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            parameter_layout.addWidget(efficacy_mult_box, 0, 5, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            parameter_layout.addWidget(resistance_mult_box, 0, 6, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            parameter_layout.addWidget(sensitivity_mult_box, 0, 7, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            parameter_layout.addWidget(offset_box, 0, 8, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

            self._lesion_content_layout.addWidget(lesion_widget)

        custom_template = scroll_template.format(
            _bg_color_one="rgba(255, 255, 255, 175)",
            _radius_one=13
        )
        scroll_area = QScrollArea()
        scroll_area.setObjectName(u"scroll_area")
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumHeight(250)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet(custom_template)
        scroll_area.setWidget(content_widget)

        main_layout.addWidget(header_frame)
        main_layout.addWidget(scroll_area)

    def validate_linked_simulation(self, index: int) -> None:
        if self.plot_list[index].isChecked():
            self.simulate_list[index].setEnabled(True)
        else:
            self.simulate_list[index].setChecked(False)
            self.simulate_list[index].setEnabled(False)

    def get_data_dictionary(self) -> dict:
        data_dictionary = {
            "abbr": [],
            "plot": [],
            "simulate": [],
            "growth": [],
            "growth_mults": [],
            "efficacy_mults": [],
            "resistance_mults": [],
            "sensitivity_mults": [],
            "offset": []
        }

        for index in range(self._num_lesions):
            data_dictionary["abbr"].append(self._lesion_abbr[index])
            data_dictionary["plot"].append(self.plot_list[index].isChecked())
            data_dictionary["simulate"].append(self.simulate_list[index].isChecked())
            data_dictionary["growth"].append(self.growth_list[index].value())
            data_dictionary["growth_mults"].append(self.growth_mult_list[index].value())
            data_dictionary["efficacy_mults"].append(self.drug_mult_list[index].value())
            data_dictionary["resistance_mults"].append(self.resistance_mult_list[index].value())
            data_dictionary["sensitivity_mults"].append(self.sensitivity_mult_list[index].value())
            data_dictionary["offset"].append(self.offset_list[index].value())

        return data_dictionary

    def import_settings(self, data: dict):
        widgets = [self._lesion_content_layout.itemAt(index).widget() for index in range(self._lesion_content_layout.count())]

        for lesion_index, lesion_widget in enumerate(widgets):
            param_widgets = lesion_widget.children()

            for param in param_widgets:
                if isinstance(param, QHBoxLayout) or isinstance(param, QLabel):
                    continue
                for key, value_list in data.items():
                    if lesion_index < len(value_list):
                        if "_mults" in key:
                            key_substring = key.split("ults")[0]
                        else:
                            key_substring = key
                        value = value_list[lesion_index]
                        if param.objectName().startswith(key_substring):
                            if isinstance(param, PyToggle):
                                param.setChecked(value)
                            elif isinstance(param, QDoubleSpinBox):
                                param.setValue(float(value))
