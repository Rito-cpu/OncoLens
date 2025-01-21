from src.core.pyqt_core import *
from src.gui.models import PyToggle
from src.gui.models.qt_spinbox import QtNumEntry
from .styles import *
from functools import partial


class ConeSettings(QWidget):
    def __init__(self,
                bg_color: str="lightblue",
                text_color: str="black",
                circle_color: str="",
                active_color: str="",
                header_size: int=12,
                parent=None) -> None:
        super().__init__()

        self._bg_color = bg_color
        self._text_color = text_color
        self._header_size = header_size
        self._circle_color = circle_color
        self._active_color = active_color

        if parent != None:
            self.setParent(parent)

        self.setFixedHeight(143)
        self.setFixedWidth(550)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # **** Setup the widget with its functionalities ****
        self.setup_widget()

        # add slots to signals
        self.use_toggle.toggled.connect(self.toggle_style)
        self._min_efficacy.valueChanged.connect(partial(self.check_efficacy_boundaries, self._min_efficacy))
        self._max_efficacy.valueChanged.connect(partial(self.check_efficacy_boundaries, self._max_efficacy))

    def setup_widget(self):
        self._container_frame = QFrame(self)
        self._container_frame.setObjectName(u"container_frame")
        self._container_frame.setFrameShape(QFrame.Shape.NoFrame)
        self._container_frame.setFrameShadow(QFrame.Shadow.Raised)

        efficacy_header = QLabel(self._container_frame)
        efficacy_header.setText("Efficacy Rate")
        efficacy_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        efficacy_header.setStyleSheet("color: {_color}; font-weight: bold; font-size: {_font_size}px;".format(_color=self._text_color, _font_size=self._header_size-1))

        resistance_header = QLabel(self._container_frame)
        resistance_header.setText("Resistance Rate")
        resistance_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        resistance_header.setStyleSheet("color: {_color}; font-weight: bold; font-size: {_font_size}px;".format(_color=self._text_color, _font_size=self._header_size-1))

        sensitivity_header = QLabel(self._container_frame)
        sensitivity_header.setText("Sensitivity Rate")
        sensitivity_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sensitivity_header.setStyleSheet("color: {_color}; font-weight: bold; font-size: {_font_size}px;".format(_color=self._text_color, _font_size=self._header_size-1))

        min_label = QLabel(self._container_frame)
        min_label.setText("Min")
        min_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        min_label.setStyleSheet("""
            QLabel {{
                color: {_color};
                font-weight: bold;
                font-size: {_font_size}px;
            }}
        """.format(_color=self._text_color, _font_size=self._header_size))

        self._min_efficacy = QtNumEntry(font_size=self._header_size,
                                    bg_color=self._text_color,
                                    parent=self._container_frame)
        self._min_efficacy.setObjectName(u"min_efficacy")
        self._min_efficacy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._min_efficacy.setDecimals(2)
        self._min_efficacy.setSingleStep(0.25)
        self._min_efficacy.setValue(3.00)

        self._min_resistance = QtNumEntry(font_size=self._header_size,
                                    bg_color=self._text_color,
                                    parent=self._container_frame)
        self._min_resistance.setObjectName(u"min_resistance")
        self._min_resistance.setDecimals(4)
        self._min_resistance.setSingleStep(0.0010)
        self._min_resistance.setValue(0.0095)

        self._min_sensitivity = QtNumEntry(font_size=self._header_size,
                                    bg_color=self._text_color,
                                    parent=self._container_frame)
        self._min_sensitivity.setObjectName(u"min_sensitivity")
        self._min_sensitivity.setDecimals(4)
        self._min_sensitivity.setSingleStep(0.0010)
        self._min_sensitivity.setValue(0.0095)

        max_label = QLabel(self._container_frame)
        max_label.setText(u"Max")
        max_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        max_label.setStyleSheet("color: {_color}; font-weight: bold; font-size: {_font_size}px;".format(_color=self._text_color, _font_size=self._header_size))

        self._max_efficacy = QtNumEntry(font_size=self._header_size,
                                    bg_color=self._text_color,
                                    parent=self._container_frame)
        self._max_efficacy.setObjectName(u"max_efficacy")
        self._max_efficacy.setDecimals(2)
        self._max_efficacy.setSingleStep(0.25)
        self._max_efficacy.setValue(3.00)

        self._max_resistance = QtNumEntry(font_size=self._header_size,
                                    bg_color=self._text_color,
                                    parent=self._container_frame)
        self._max_resistance.setObjectName(u"max_resistance")
        self._max_resistance.setDecimals(4)
        self._max_resistance.setSingleStep(0.0010)
        self._max_resistance.setValue(0.0095)

        self._max_sensitivity = QtNumEntry(font_size=self._header_size,
                                    bg_color=self._text_color,
                                    parent=self._container_frame)
        self._max_sensitivity.setObjectName(u"max_sensitivity")
        self._max_sensitivity.setDecimals(4)
        self._max_sensitivity.setSingleStep(0.0010)
        self._max_sensitivity.setValue(0.0095)

        self.t_frame = QFrame(self._container_frame)
        self.t_frame.setFrameShape(QFrame.Shape.NoFrame)

        self.cone_label = QLabel(self.t_frame)
        self.cone_label.setObjectName(u"cone_label")
        self.cone_label.setText("Use Cone")
        self.cone_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cone_label.setStyleSheet("""
            QLabel {{
                color: {_color};
                font-size: {_font_size}px;
            }}
        """.format(_color=self._text_color, _font_size=11))

        self.use_toggle = PyToggle(
            width=28,
            height=16,
            ellipse_y=2,
            bg_color = self._text_color,
            circle_color = self._circle_color,
            active_color = self._active_color,
            parent=self.t_frame
        )
        self.use_toggle.setChecked(False)

        lay = QVBoxLayout(self.t_frame)
        lay.addWidget(self.cone_label, alignment=Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.use_toggle, alignment=Qt.AlignmentFlag.AlignCenter)

        grid_lay = QGridLayout(self._container_frame)
        grid_lay.setContentsMargins(0, 0, 0, 0)
        grid_lay.setHorizontalSpacing(5)
        grid_lay.setVerticalSpacing(5)
        grid_lay.addWidget(self.t_frame, 0, 0, 3, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid_lay.addWidget(efficacy_header, 0, 2, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid_lay.addWidget(resistance_header, 0, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid_lay.addWidget(sensitivity_header, 0, 4, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid_lay.addWidget(min_label, 1, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid_lay.addWidget(self._min_efficacy, 1, 2, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid_lay.addWidget(self._min_resistance, 1, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid_lay.addWidget(self._min_sensitivity, 1, 4, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid_lay.addWidget(max_label, 2, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid_lay.addWidget(self._max_efficacy, 2, 2, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid_lay.addWidget(self._max_resistance, 2, 3, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        grid_lay.addWidget(self._max_sensitivity, 2, 4, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self._container_frame)
        self.toggle_style(False)

    def toggle_style(self, toggled):
        if toggled:
            self._container_frame.setStyleSheet("""
                QFrame#container_frame {{
                    background: {_bg_color};
                    border-radius: 9;
                }}
            """.format(_bg_color=self._bg_color))

            self.enable_entries()
        else:
            self._container_frame.setStyleSheet("""
                QFrame#container_frame {{
                    background: {_bg_color};
                    border-radius: 9;
                }}
            """.format(_bg_color="rgba(215, 215, 215, 255)"))

            self.disable_entries()

    def disable_entries(self):
        self._min_efficacy.setEnabled(False)
        self._min_resistance.setEnabled(False)
        self._min_sensitivity.setEnabled(False)
        self._max_efficacy.setEnabled(False)
        self._max_resistance.setEnabled(False)
        self._max_sensitivity.setEnabled(False)

    def enable_entries(self):
        self._min_efficacy.setEnabled(True)
        self._min_resistance.setEnabled(True)
        self._min_sensitivity.setEnabled(True)
        self._max_efficacy.setEnabled(True)
        self._max_resistance.setEnabled(True)
        self._max_sensitivity.setEnabled(True)

    def remove_toggle(self):
        self.t_frame.hide()

    def check_efficacy_boundaries(self, widget: QtNumEntry):
        value = widget.value()

        if widget.objectName() == "min_efficacy":
            if value >= self._max_efficacy.value():
                widget.setValue(self._max_efficacy.value() - 0.01)
        elif widget.objectName() == "max_efficacy":
            if value <= self._min_efficacy.value():
                widget.setValue(self._max_efficacy.value() + 0.01)

    def get_min_values(self):
        return [self._min_efficacy.value(), self._min_resistance.value(), self._min_sensitivity.value()]

    def set_min_values(self, values):
        if len(values) == 3:
            self._min_efficacy.setValue(values[0])
            self._min_resistance.setValue(values[1])
            self._min_sensitivity.setValue(values[2])

    def get_max_values(self):
        return [self._max_efficacy.value(), self._max_resistance.value(), self._max_sensitivity.value()]

    def set_max_values(self, values):
        if len(values) == 3:
            self._max_efficacy.setValue(values[0])
            self._max_resistance.setValue(values[1])
            self._max_sensitivity.setValue(values[2])

    def get_rates(self):
        min_rates = self.get_min_values()
        max_rates = self.get_max_values()

        return [min_rates, max_rates]

    def is_active(self):
        return self.use_toggle.isChecked()

    def set_active(self, active):
        self.use_toggle.setChecked(True) if active else self.use_toggle.setChecked(False)
