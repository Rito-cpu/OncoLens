from functools import partial
from datetime import datetime
from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.gui.models.qt_spinbox import QtNumEntry
from .styles import *


class TxSettings(QWidget):
    def __init__(self,
                data_dict: dict,
                font_size: int=12,
                header_size: int=12,
                header_color: str="black",
                treatment_bg: str="lightblue",
                border_radius: int=9,
                default_delta: float=1.5,
                default_res: float=0.0095,
                default_sens: float=0.0095,
                parent=None) -> None:
        super().__init__()

        self._font_size = font_size
        self._header_size = header_size
        self._header_color = header_color
        self._treatment_bg = treatment_bg
        self._border_radius = border_radius
        self._default_delta = default_delta
        self._default_res = default_res
        self._default_sens = default_sens

        themes = Themes()
        self.themes = themes.items

        self.treatment_names = data_dict["names"]
        self.treatment_abbr = data_dict["abbr"]
        self.dates_on = data_dict["date_on"]
        self.dates_off = data_dict["date_off"]
        self.num_treatments = len(self.treatment_names)

        self._abbr_labels = []
        self._tx_on_labels = []
        self._tx_off_labels = []
        self._tx_delta_boxes = []
        self._tx_res_boxes = []
        self._tx_sens_boxes = []

        self._tx_exceptions = {
            "Surgery": [],
            "Radiation": []
        }

        # **** Deprecated function: identifying combination drugs
        self._search_duplicate_tx()

        self._setup_widget()

    def _setup_widget(self):
        # --- Create Section Header Widgets ---
        name_header = QLabel('Treatment')
        name_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        date_on_header = QLabel('Date On')
        date_on_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        date_off_header = QLabel('Date Off')
        date_off_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        efficacy_header = QLabel('Efficacy Rate')
        efficacy_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        resistance_header = QLabel('Resistance')
        resistance_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sensitivity_header = QLabel('Sensitivity')
        sensitivity_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_style = header_template.format(
            _header_color=self._header_color,
            _header_size=self._header_size
        )
        header_base = QFrame(self)
        header_base.setObjectName(u"header_base")
        header_base.setFrameShape(QFrame.Shape.NoFrame)
        header_base.setFrameShadow(QFrame.Shadow.Raised)
        header_base.setStyleSheet(header_style)

        header_layout = QGridLayout(header_base)
        header_layout.setContentsMargins(10, 0 ,10, 0)
        header_layout.setHorizontalSpacing(5)
        header_layout.addWidget(name_header, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(date_on_header, 0, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(date_off_header, 0, 2, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(efficacy_header, 0, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(resistance_header, 0, 4, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(sensitivity_header, 0, 5, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        scroll_contents = QWidget()
        scroll_contents.setObjectName(u"scroll_contents")
        scroll_contents.setStyleSheet("""
            QWidget#scroll_contents {
                background: transparent;
                border: none;
            }""")
        # container_widget.setMinimumSize(self._tx_content_layout.sizeHint())

        self._tx_content_layout = QVBoxLayout(scroll_contents)
        self._tx_content_layout.setObjectName(u"content_layout")
        self._tx_content_layout.setContentsMargins(10, 10, 10, 10)
        self._tx_content_layout.setSpacing(13)

        cocktail_dates = [date_pair for date_pair, drugs in self.treatment_dict.items() if len(drugs) > 1]
        # --- Loop that creates treatment widgets ---
        for index in range(self.num_treatments):
            surgery_switch = False

            treatment_widget = QWidget(scroll_contents)
            treatment_widget.setObjectName(u"treatment_widget")
            treatment_widget.setContentsMargins(0, 0, 0, 0)
            treatment_widget.setFixedHeight(43)

            date_pair = (self.dates_on[index], self.dates_off[index])
            if date_pair in cocktail_dates:
                color_holder = "rgba(215, 215, 215, 255)"
            else:
                color_holder = "None"

            treatment_style = treatment_instance_template.format(
                _object_name=treatment_widget.objectName(),
                _bg_color=color_holder,
                _border_radius=self._border_radius,
                _color=self._header_color
            )
            treatment_widget.setStyleSheet(treatment_style)


            abbr_label = QLabel(treatment_widget)
            abbr_label.setObjectName(u"abbr_label")
            abbr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            abbr_label.setToolTip(self.treatment_names[index])
            abbr_label.setCursor(Qt.CursorShape.IBeamCursor)
            abbr_label.setText(self.treatment_abbr[index])
            abbr_label.setStyleSheet(data_template.format(_font_size=self._font_size))
            self._abbr_labels.append(abbr_label)

            temp_date = self.dates_on[index].strftime('%m/%d/%Y')
            date_on_label = QLabel(treatment_widget)
            date_on_label.setObjectName(u"date_on_label")
            date_on_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            date_on_label.setText(temp_date)
            date_on_label.setCursor(Qt.CursorShape.IBeamCursor)
            date_on_label.setStyleSheet(data_template.format(_font_size=self._font_size))
            self._tx_on_labels.append(date_on_label)

            temp_date = self.dates_off[index].strftime('%m/%d/%Y')
            date_off_label = QLabel(treatment_widget)
            date_off_label.setObjectName(u"date_off_label")
            date_off_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            date_off_label.setText(temp_date)
            date_off_label.setCursor(Qt.CursorShape.IBeamCursor)
            date_off_label.setStyleSheet(data_template.format(_font_size=self._font_size))
            self._tx_off_labels.append(date_off_label)

            efficacy_box = QtNumEntry(font_size=self._font_size,
                                    bg_color=self.themes["app_color"]["dark_one"],
                                    parent=treatment_widget)
            efficacy_box.setObjectName(u"efficacy_box")
            efficacy_box.setRange(0, 100)
            efficacy_box.setSingleStep(0.25)
            efficacy_box.setFixedWidth(65)
            if "radiation" in self.treatment_names[index].lower() or "rad" in self.treatment_abbr[index].lower():
                efficacy_box.setValue(100)
                self._tx_exceptions["Radiation"].append(index)
            elif "surgery" in self.treatment_names[index].lower() or "surg" in self.treatment_abbr[index].lower():
                efficacy_box.setValue(0)
                self._tx_exceptions["Surgery"].append(index)
                surgery_switch = True
            else:
                efficacy_box.setValue(3)
            self._tx_delta_boxes.append(efficacy_box)

            resistance_box = QtNumEntry(font_size=self._font_size,
                                    bg_color=self.themes["app_color"]["dark_one"],
                                    parent=treatment_widget)
            resistance_box.setObjectName(u"resistance_box")
            resistance_box.setDecimals(4)
            resistance_box.setRange(0, 0.04)
            resistance_box.setValue(0.0095)
            resistance_box.setSingleStep(0.001)
            resistance_box.setFixedWidth(65)
            self._tx_res_boxes.append(resistance_box)

            sensitivity_box = QtNumEntry(font_size=self._font_size,
                                    bg_color=self.themes["app_color"]["dark_one"],
                                    parent=treatment_widget)
            sensitivity_box.setObjectName(u"sensitivity_box")
            sensitivity_box.setDecimals(4)
            sensitivity_box.setRange(0, 0.04)
            sensitivity_box.setValue(0.0095)
            sensitivity_box.setSingleStep(0.001)
            sensitivity_box.setFixedWidth(65)
            self._tx_sens_boxes.append(sensitivity_box)

            if surgery_switch:
                efficacy_box.setEnabled(False)
                resistance_box.setEnabled(False)
                sensitivity_box.setEnabled(False)

            # if self.duplicate_tx_names is not None and index in self.duplicate_tx_names.keys():
            #     combined_tx_widget = self._create_duplicate_widget(index)
            #
            #     self._tx_content_layout.addWidget(combined_tx_widget)
            #     if index not in self.marked_enablers:
            #         sub_index = index
            #         while sub_index < index + self.duplicate_tx_indexes[index]:
            #             self.marked_enablers.append(sub_index)
            #             sub_index += 1

            treatment_layout = QGridLayout(treatment_widget)
            treatment_layout.setObjectName(u"treatment_layout")
            treatment_layout.setContentsMargins(0, 0, 0, 0)
            treatment_layout.setHorizontalSpacing(5)
            treatment_layout.setVerticalSpacing(5)
            treatment_layout.addWidget(abbr_label, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            treatment_layout.addWidget(date_on_label, 0, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            treatment_layout.addWidget(date_off_label, 0, 2, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            treatment_layout.addWidget(efficacy_box, 0, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            treatment_layout.addWidget(resistance_box, 0, 4, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
            treatment_layout.addWidget(sensitivity_box, 0, 5, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

            # if index in self.marked_enablers:
            #     abbr_label.setEnabled(False)
            #     tx_on_label.setEnabled(False)
            #     tx_off_label.setEnabled(False)
            #     tx_delta_box.setEnabled(False)
            #     tx_res_box.setEnabled(False)
            #     tx_sens_box.setEnabled(False)
            #     self.marked_layout[index] = current_tx_layout
            #     current_tx_frame.setStyleSheet("""
            #         QWidget#TxWidget {
            #             background: rgba(255, 174, 102, 125);
            #             border-radius: 20px;
            #             border: 2px solid gray;
            #         }""")

            self._tx_content_layout.addWidget(treatment_widget)

        # --- Create Containers to add widgets to ---
        scroll_area = QScrollArea(self)
        scroll_area.setObjectName(u"scroll_area")
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumHeight(250)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setWidget(scroll_contents)
        scroll_area.setStyleSheet("""
            QScrollArea {
            background: rgba(255, 255, 255, 175);
            border-radius: 13px;
            border: none;
            }""")

        # Need to implement a restore to default option
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(17, 17, 17, 17)
        main_layout.setSpacing(6)
        main_layout.addWidget(header_base)
        main_layout.addWidget(scroll_area)

    def _search_duplicate_tx(self):
        # **** Find duplicate drug dates and add them to the dictionary with their corresponding drug
        self.treatment_dict = {}
        for index in range(len(self.dates_on)):
            date_pair = (self.dates_on[index], self.dates_off[index])
            if date_pair not in self.treatment_dict:
                self.treatment_dict[date_pair] = [self.treatment_abbr[index]]
            else:
                self.treatment_dict[date_pair].append(self.treatment_abbr[index])

    def _uncombine_duplicate_tx(self, index, combine_checkbox):
        holder_index = index
        parent_widget = combine_checkbox.parentWidget()
        widget_items = parent_widget.findChildren(QWidget)

        if combine_checkbox.isChecked():
            while holder_index < self.duplicate_tx_indexes[index] + index:
                for item in range(self.marked_layout[holder_index].count()):
                    widget = self.marked_layout[holder_index].itemAt(item).widget()
                    widget.setEnabled(False)
                holder_index += 1
            for item in widget_items[1:]:
                if not item.isEnabled():
                    item.setEnabled(True)
        else:
            while holder_index < self.duplicate_tx_indexes[index] + index:
                for item in range(self.marked_layout[holder_index].count()):
                    widget = self.marked_layout[holder_index].itemAt(item).widget()
                    widget.setEnabled(True)
                holder_index += 1
            for item in widget_items[1:]:
                if item.isEnabled():
                    item.setEnabled(False)

    def _create_duplicate_widget(self, index:int) -> QWidget:
        combined_tx_name = QLabel(self.duplicate_tx_names[index])
        combined_tx_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        combine_tx_chbx = QCheckBox()
        combine_tx_chbx.setChecked(True)
        combine_tx_chbx.setCursor(Qt.CursorShape.PointingHandCursor)

        self.combined_tx_chbx_list.append(combine_tx_chbx)
        self.combined_tx_chbx_list[-1].toggled.connect(partial(self._uncombine_duplicate_tx, index, combine_tx_chbx))
        # self.combined_tx_chbx_list[-1].toggled.connect(self.setMatrix)  # TODO: set tx matrix

        temp_date = self.dates_on[index].strftime('%m/%d/%Y')
        combined_tx_date_on = QLabel(temp_date)
        combined_tx_date_on.setAlignment(Qt.AlignmentFlag.AlignCenter)

        temp_date = self.dates_off[index].strftime('%m/%d/%Y')
        combined_tx_date_off = QLabel(temp_date)
        combined_tx_date_off.setAlignment(Qt.AlignmentFlag.AlignCenter)

        combined_tx_delta_box = QDoubleSpinBox()
        combined_tx_delta_box.setRange(0, 100)
        combined_tx_delta_box.setSingleStep(0.25)
        combined_tx_delta_box.setValue(3)
        combined_tx_delta_box.setFixedWidth(65)

        combined_tx_res_box = QDoubleSpinBox()
        combined_tx_res_box.setDecimals(4)
        combined_tx_res_box.setRange(0, 0.04)
        combined_tx_res_box.setValue(0.0095)
        combined_tx_res_box.setSingleStep(0.001)
        combined_tx_res_box.setFixedWidth(65)

        combined_tx_sens_box = QDoubleSpinBox()
        combined_tx_sens_box.setDecimals(4)
        combined_tx_sens_box.setRange(0, 0.04)
        combined_tx_sens_box.setValue(0.0095)
        combined_tx_sens_box.setSingleStep(0.001)
        combined_tx_sens_box.setFixedWidth(65)
        combined_tx_sens_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        combined_tx_frame = QWidget()
        combined_tx_frame.setObjectName('CombWidget')
        combined_tx_frame.setContentsMargins(0, 0, 0, 0)
        combined_tx_frame.setFixedHeight(43)
        combined_tx_frame.setStyleSheet("""
            QWidget#CombWidget {
                background: rgba(255, 174, 102, 125);
                border-radius: 20px;
                border: 2px solid gray;
            }""")

        combined_tx_layout = QHBoxLayout(combined_tx_frame)
        combined_tx_layout.addWidget(combine_tx_chbx)
        combined_tx_layout.addStretch(1)
        combined_tx_layout.addWidget(combined_tx_name)
        combined_tx_layout.addStretch(4)
        combined_tx_layout.addWidget(combined_tx_date_on)
        combined_tx_layout.addStretch(3)
        combined_tx_layout.addWidget(combined_tx_date_off)
        combined_tx_layout.addStretch(4)
        combined_tx_layout.addWidget(combined_tx_delta_box)
        combined_tx_layout.addStretch(4)
        combined_tx_layout.addWidget(combined_tx_res_box)
        combined_tx_layout.addStretch(3)
        combined_tx_layout.addWidget(combined_tx_sens_box)
        combined_tx_layout.addStretch(2)

        return combined_tx_frame

    def get_data_dictionary(self) -> dict:
        data_dictionary = {
            "abbr": [],
            "date_on": [],
            "date_off": [],
            "efficacy": [],
            "resistance": [],
            "sensitivity": [],
        }

        for index in range(self._tx_content_layout.count()):
            data_dictionary["abbr"].append(self._abbr_labels[index].text())
            data_dictionary["date_on"].append(datetime.strptime(self._tx_on_labels[index].text(), "%m/%d/%Y").date())
            data_dictionary["date_off"].append(datetime.strptime(self._tx_off_labels[index].text(), "%m/%d/%Y").date())
            data_dictionary["efficacy"].append(self._tx_delta_boxes[index].value())
            data_dictionary["resistance"].append(self._tx_res_boxes[index].value())
            data_dictionary["sensitivity"].append(self._tx_sens_boxes[index].value())

        return data_dictionary

    def import_settings(self, data: dict):
        widgets = [self._tx_content_layout.itemAt(index).widget() for index in range(self._tx_content_layout.count())]

        for treatment_index, treatment_widget in enumerate(widgets):
            param_widgets = treatment_widget.children()

            for param in param_widgets:
                if isinstance(param, QHBoxLayout) or isinstance(param, QLabel):
                    continue

                for key, value_list in data.items():
                    if treatment_index < len(value_list):
                        value = value_list[treatment_index]
                        if param.objectName().startswith(key):
                            if isinstance(param, QDoubleSpinBox):
                                param.setValue(float(value))
