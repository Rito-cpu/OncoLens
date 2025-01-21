from datetime import datetime
from functools import partial
from src.core.pyqt_core import *
from src.core.keyword_store import NO_CONE, COMBINATION_CONE, COMPARISON_CONE
from src.core.json.json_themes import Themes
from src.gui.models import PyPushButton
from src.gui.models.py_toggle import PyToggle
from src.gui.models.qt_spinbox import QtNumEntry
from src.gui.models.qt_date_box import QtDateEntry
from src.gui.models.qt_cone_dialog import QtConeDialog
from src.gui.models.qt_message import QtMessage
from .styles import *
from .qt_cone_settings import ConeSettings


class AvailableTxSettings(QWidget):
    def __init__(
            self,
            lesion_names: list[str],
            data_dict: dict,
            font_size: int=12,
            header_size: int=12,
            header_color: str="black",
            treatment_bg: str="lightblue",
            bg_color: str="black",
            circle_color: str="white",
            active_color: str="lightblue",
            parent=None
        ) -> None:
        super().__init__(parent)

        self._lesion_names = lesion_names
        self._font_size = font_size
        self._header_size = header_size
        self._header_color = header_color
        self._treatment_bg = treatment_bg
        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color
        self._available_tx_names = data_dict['Name']
        self._available_tx_abbr = data_dict['Abbr']
        if data_dict['Name'] is None or data_dict['Abbr'] is None:
            self.num_available_tx = 0
        else:
            self.num_available_tx = len(self._available_tx_names)

        themes = Themes()
        self.themes = themes.items

        self._abbr_labels_list = []
        self._active_chbx_list = []
        self._on_dates_list = []
        self._off_dates_list = []
        self._efficacy_boxes = []
        self._res_boxes = []
        self._sens_boxes = []
        self._cone_settings = {
            "method": NO_CONE,
            "data": None,
        }

        self.setup_widget()

    def setup_widget(self):
        # **** Create Header Section ****
        name_header = QLabel('Treatment')
        name_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        active_header = QLabel('Active')
        active_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        date_on_header = QLabel('Date On')
        date_on_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        date_off_header = QLabel('Date Off')
        date_off_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        efficacy_header = QLabel('Efficacy Rate')
        efficacy_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        res_header = QLabel('Resistance')
        res_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sens_header = QLabel('Sensitivity')
        sens_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        header_layout.setContentsMargins(10, 0, 10, 0)
        header_layout.setHorizontalSpacing(5)
        header_layout.addWidget(active_header, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(name_header, 0, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(date_on_header, 0, 2, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(date_off_header, 0, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(efficacy_header, 0, 4, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(res_header, 0, 5, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(sens_header, 0, 6, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        self.content_widget = QWidget()
        self.content_widget.setObjectName(u"content_widget")
        self.content_widget.setStyleSheet("""
            QWidget#content_widget {
                background: transparent;
                border: none;
            }""")

        self.container_widget_layout = QVBoxLayout(self.content_widget)
        self.container_widget_layout.setObjectName(u"content_layout")
        if self.num_available_tx == 0:
            empty_label = QLabel(self.content_widget)
            empty_label.setText("No Available Treatments Found")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet('font-size: 12px;')
            self.container_widget_layout.addWidget(empty_label, alignment=Qt.AlignmentFlag.AlignCenter)
        else:
            for index in range(self.num_available_tx):
                container_test = QWidget(self.content_widget)
                container_test.setObjectName(u"container_test")

                # treatment_frame = QWidget(self.content_widget)
                treatment_frame = QWidget(container_test)
                treatment_frame.setObjectName(u"treatment_frame")
                treatment_frame.setContentsMargins(0, 0, 0, 0)
                treatment_frame.setFixedHeight(43)

                self.available_tx_style = available_tx_toggled.format(
                    _object_name=treatment_frame.objectName(),
                    _bg_color=self._treatment_bg,
                    _border_radius=9
                )

                active_toggle = PyToggle(
                    width=28,
                    height=16,
                    ellipse_y=2,
                    bg_color = self._bg_color,
                    circle_color = self._circle_color,
                    active_color = self._active_color,
                    parent=treatment_frame
                )
                active_toggle.setObjectName(u"active_toggle")
                active_toggle.setChecked(False)
                active_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
                self._active_chbx_list.append(active_toggle)

                abbr_label = QLabel(treatment_frame)
                abbr_label.setObjectName(u"abbr_label")
                abbr_label.setToolTip(self._available_tx_names[index])
                abbr_label.setText(self._available_tx_abbr[index])
                abbr_label.setCursor(Qt.CursorShape.IBeamCursor)
                # abbr_label.setStyleSheet(data_template.format(_font_size=self._font_size))
                abbr_label.setStyleSheet("""
                    QLabel {{
                        font-size: {_font_size}px;
                        color: {_color};
                    }}
                """.format(_font_size=self._font_size, _color=self._header_color))
                self._abbr_labels_list.append(abbr_label)

                today_date = QDate(datetime.today())
                # date_on_label = QDateEdit(treatment_frame)
                date_on_label = QtDateEntry(color_one=self._header_color,
                                            parent=treatment_frame)
                date_on_label.setObjectName(u"date_on_label")
                date_on_label.setDate(today_date)
                date_on_label.setEnabled(False)
                self._on_dates_list.append(date_on_label)

                date_off_label = QtDateEntry(color_one=self._header_color,
                                            parent=treatment_frame)
                date_off_label.setObjectName(u"date_off_label")
                date_off_label.setDate(today_date.addDays(1))
                date_off_label.setEnabled(False)
                self._off_dates_list.append(date_off_label)

                efficacy_box = QtNumEntry(font_size=self._font_size,
                                    bg_color=self.themes["app_color"]["dark_one"],
                                    parent=treatment_frame)
                efficacy_box.setObjectName(u"efficacy_box")
                efficacy_box.setRange(0, 100)
                efficacy_box.setValue(3)
                efficacy_box.setSingleStep(0.25)
                efficacy_box.setEnabled(False)
                self._efficacy_boxes.append(efficacy_box)

                resistance_box = QtNumEntry(font_size=self._font_size,
                                    bg_color=self.themes["app_color"]["dark_one"],
                                    parent=treatment_frame)
                resistance_box.setObjectName(u"resistance_box")
                resistance_box.setDecimals(4)
                resistance_box.setRange(0, 0.04)
                resistance_box.setValue(0.0095)
                resistance_box.setSingleStep(0.001)
                resistance_box.setEnabled(False)
                self._res_boxes.append(resistance_box)

                sensitivity_box = QtNumEntry(font_size=self._font_size,
                                    bg_color=self.themes["app_color"]["dark_one"],
                                    parent=treatment_frame)
                sensitivity_box.setObjectName(u"sensitivity_box")
                sensitivity_box.setDecimals(4)
                sensitivity_box.setRange(0, 0.04)
                sensitivity_box.setValue(0.0095)
                sensitivity_box.setSingleStep(0.001)
                sensitivity_box.setEnabled(False)
                self._sens_boxes.append(sensitivity_box)

                self._active_chbx_list[-1].toggled.connect(partial(self._available_chbx_validator, index))
                self._on_dates_list[-1].dateChanged.connect(partial(self._on_date_check, index))
                self._off_dates_list[-1].dateChanged.connect(partial(self._off_date_check, index))

                # cone_widget = ConeSettings(bg_color=self._treatment_bg,
                #                         text_color=self._header_color,
                #                         header_size=self._font_size,
                #                         circle_color=self._circle_color,
                #                         active_color=self._active_color,
                #                         parent=container_test)
                # cone_widget.setObjectName(u"cone_widget")
                # cone_widget.hide()

                treatment_layout = QGridLayout(treatment_frame)
                treatment_layout.setContentsMargins(0, 0, 0, 0)
                treatment_layout.setHorizontalSpacing(5)
                treatment_layout.setVerticalSpacing(5)
                treatment_layout.addWidget(active_toggle, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
                treatment_layout.addWidget(abbr_label, 0, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
                treatment_layout.addWidget(date_on_label, 0, 2, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
                treatment_layout.addWidget(date_off_label, 0, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
                treatment_layout.addWidget(efficacy_box, 0, 4, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
                treatment_layout.addWidget(resistance_box, 0, 5, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
                treatment_layout.addWidget(sensitivity_box, 0, 6, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

                # container_test_lay = QVBoxLayout(container_test)
                # container_test_lay.addWidget(treatment_frame)
                # container_test_lay.addWidget(cone_widget, alignment=Qt.AlignmentFlag.AlignLeft)

                self.container_widget_layout.addWidget(treatment_frame)
                # self.container_widget_layout.addWidget(container_test)

        scroll_area = QScrollArea(self)
        scroll_area.setObjectName(u"scroll_area")
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumHeight(250)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setWidget(self.content_widget)
        scroll_area.setStyleSheet("""
                QScrollArea {
                background: rgba(255, 255, 255, 175);
                border-radius: 13px;
                border: none;
            }
        """)

        self._cone_settings_bttn = PyPushButton(text="Cone Settings",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent=self
        )
        self._cone_settings_bttn.setObjectName("cone_settings_bttn")
        self._cone_settings_bttn.setFixedSize(110, 29)
        self._cone_settings_bttn.clicked.connect(self.launch_cone_dialog)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(17, 17, 17, 17)
        main_layout.setSpacing(5)
        main_layout.addWidget(header_base)
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(self._cone_settings_bttn, alignment=Qt.AlignmentFlag.AlignCenter)

    def launch_cone_dialog(self):
        available_tx_dict = self.get_current_treatments()

        # TODO: Whenever the state is changed (stateChanged) for a qcheckbox (PyToggle), connect it to a method that updates the current count of treatments turned on
        # for cb in checkbox_list: cb.stateChanged.connect(lambda: count_checked(checkbox_list))
        if len(available_tx_dict) == 0:
            msg = "No available treatment selected."
            detailed_msg = "Please select a treatment, if made available, from the available treatments list before using cone settings."

            error_message = QtMessage(
                buttons={"Ok": QMessageBox.ButtonRole.AcceptRole},
                color=self.themes["app_color"]["white"],
                bg_color_one=self.themes["app_color"]["dark_one"],
                bg_color_two=self.themes["app_color"]["bg_one"],
                bg_color_hover=self.themes["app_color"]["dark_three"],
                bg_color_pressed=self.themes["app_color"]["dark_four"]
            )
            error_message.setIcon(QMessageBox.Icon.Warning)
            error_message.setText(msg)
            error_message.setDetailedText(detailed_msg)
            error_message.exec()
            return

        self.cone_dialog = QtConeDialog(
            lesion_names=self._lesion_names,
            treatments=available_tx_dict,
            bg_color_one=self.themes["app_color"]["blue_one"],
            bg_color_two=self.themes["app_color"]["dark_one"],
            hover_color=self.themes["app_color"]["dark_three"],
            pressed_color=self.themes["app_color"]["dark_four"],
            text_color_one=self.themes["app_color"]["dark_one"],
            text_color_two=self.themes["app_color"]["white"],
            load_data=self._cone_settings,
            parent=self
        )
        result = self.cone_dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            # User clicked Okay
            # If No Cone, do normal process
            # If Targeted, consider the selected treatments and their respective cones
            method, data = self.cone_dialog.submit_method_data()
            self._cone_settings['method'] = method
            self._cone_settings['data'] = data

            avg_param_values = self.cone_dialog.get_average_values()
            self.change_param_values(avg_param_values)
        else:
            # user clicked cancel
            # No need to do anything, settings defaulted to No Cone or will use previously saved option
            pass
            # print("Canceled Cone Settings")

    def _on_date_check(self, index: int):
        if self._on_dates_list[index].date() >= self._off_dates_list[index].date():
            self._off_dates_list[index].setDate(self._on_dates_list[index].date().addDays(1))

    def _off_date_check(self, index: int):
        if self._off_dates_list[index].date() <= self._on_dates_list[index].date():
            self._on_dates_list[index].setDate(self._on_dates_list[index].date().addDays(-1))

    def _available_chbx_validator(self, index: int):
        if self._active_chbx_list[index].isChecked():
            container_widget = self.container_widget_layout.itemAt(index).widget()
            if container_widget.objectName() == "container_test":
                tx_frame = container_widget.findChild(QWidget, "treatment_frame")
                tx_frame.setStyleSheet(self.available_tx_style)
                cone = container_widget.findChild(QWidget, "cone_widget")
                cone.show()
            self._on_dates_list[index].setEnabled(True)
            self._off_dates_list[index].setEnabled(True)
            self._efficacy_boxes[index].setEnabled(True)
            self._res_boxes[index].setEnabled(True)
            self._sens_boxes[index].setEnabled(True)
        else:
            container_widget = self.container_widget_layout.itemAt(index).widget()
            if container_widget.objectName() == "container_test":
                tx_frame = container_widget.findChild(QWidget, "treatment_frame")
                tx_frame.setStyleSheet(None)
                cone = container_widget.findChild(QWidget, "cone_widget")
                cone.hide()
            self._on_dates_list[index].setEnabled(False)
            self._off_dates_list[index].setEnabled(False)
            self._efficacy_boxes[index].setEnabled(False)
            self._res_boxes[index].setEnabled(False)
            self._sens_boxes[index].setEnabled(False)

    def change_param_values(self, treatment_dict: dict):
        for index in range(self.num_available_tx):
            if self._available_tx_abbr[index] in treatment_dict:
                values = treatment_dict[self._available_tx_abbr[index]]
                self._efficacy_boxes[index].setValue(values[0])
                self._res_boxes[index].setValue(values[1])
                self._sens_boxes[index].setValue(values[2])

    def get_current_treatments(self):
        available_tx_dict = {}

        for index in range(self.num_available_tx):
            if self._active_chbx_list[index].isChecked():
                tx_abbr = self._available_tx_abbr[index]
                efficacy = self._efficacy_boxes[index].value()
                resistance = self._res_boxes[index].value()
                sensitivity = self._sens_boxes[index].value()

                available_tx_dict[tx_abbr] = [efficacy, resistance, sensitivity]

        return available_tx_dict
        # return sum(cb.isChecked() for cb in checkbox_list)

    def get_data_dictionary(self) -> dict:
        data_dictionary = {
            "abbr": [],
            "date_on": [],
            "date_off": [],
            "efficacy": [],
            "resistance": [],
            "sensitivity": [],
        }

        for index in range(self.num_available_tx):
            if self._active_chbx_list[index].isChecked():
                data_dictionary["abbr"].append(self._available_tx_abbr[index])
                data_dictionary["date_on"].append(self._on_dates_list[index].date().toPyDate())
                data_dictionary["date_off"].append(self._off_dates_list[index].date().toPyDate())
                data_dictionary["efficacy"].append(self._efficacy_boxes[index].value())
                data_dictionary["resistance"].append(self._res_boxes[index].value())
                data_dictionary["sensitivity"].append(self._sens_boxes[index].value())

        return data_dictionary

    def get_cone_settings(self):
        # If there are no available treatments selected, submit params with no cone
        treatments = self.get_current_treatments()
        if len(treatments) == 0:
            null_dict = {
                "method": NO_CONE,
                "data": None,
            }
            return null_dict

        return self._cone_settings

    def read_all(self):
        data_dictionary = {
            "active": [],
            "abbr": [],
            "date_on": [],
            "date_off": [],
            "efficacy": [],
            "resistance": [],
            "sensitivity": [],
            "cone_on": [],
            "min_efficacy": [],
            "min_resistance": [],
            "min_sensitivity": [],
            "max_efficacy": [],
            "max_resistance": [],
            "max_sensitivity": []
        }

        widgets = [self.container_widget_layout.itemAt(index).widget() for index in range(self.container_widget_layout.count())]

        for treatment_index, treatment_widget in enumerate(widgets):
            # print(f'Container widget: {container_widget.objectName()}')
            # test = container_widget.findChild(QWidget, 'container_test')
            # treatment_widget = container_widget.findChild(QWidget, "treatment_frame")
            treatment_params = treatment_widget.children()

            for param in treatment_params:
                if isinstance(param, QHBoxLayout):
                    continue
                elif isinstance(param, PyToggle):
                    data_dictionary["active"].append(param.isChecked())
                elif isinstance(param, QLabel):
                    data_dictionary["abbr"].append(param.text())
                elif isinstance(param, QDateEdit):
                    if param.objectName() == "date_on_label":
                        data_dictionary["date_on"].append(param.date().toPyDate())
                    elif param.objectName() == "date_off_label":
                        data_dictionary["date_off"].append(param.date().toPyDate())
                elif isinstance(param, QDoubleSpinBox):
                    if param.objectName() == "efficacy_box":
                        data_dictionary["efficacy"].append(param.value())
                    elif param.objectName() == "resistance_box":
                        data_dictionary["resistance"].append(param.value())
                    elif param.objectName() == "sensitivity_box":
                        data_dictionary["sensitivity"].append(param.value())

        return data_dictionary

# TODO: Apply new settings with cone, remember that treatment widget is now a container and has 2 children
    def import_settings(self, data: dict):
        widgets = [self.container_widget_layout.itemAt(index).widget() for index in range(self.container_widget_layout.count())]

        for treatment_index, treatment_widget in enumerate(widgets):
            # print(f"Widget {treatment_index} is {treatment_widget.objectName()}")
            param_widgets = treatment_widget.children()

            for param in param_widgets:
                # print(f"\tParameter is {param.objectName()}")
                if isinstance(param, QHBoxLayout) or isinstance(param, QLabel):
                    continue

                for key, value_list in data.items():
                    if key == "cone_on":
                        break
                    if treatment_index < len(value_list):
                        value = value_list[treatment_index]
                        # print(f"\t\tKey is {key}, Value is {value}")
                        if param.objectName().startswith(key):
                            if isinstance(param, PyToggle):
                                param.setChecked(value)
                            elif isinstance(param, QDateEdit):
                                date = QDate.fromString(value, "MM/dd/yyyy")
                                param.setDate(date)
                            elif isinstance(param, QDoubleSpinBox):
                                param.setValue(float(value))
