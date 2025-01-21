from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.gui.models.qt_spinbox.qt_num_entry import QtNumEntry


class QtConeWidget(QWidget):
    def __init__(
            self,
            header: str = '',
            hide_header: bool = False,
            averages: list = None,
            param_mult: float = 0.5,
            font_size: int = 12,
            parent=None
        ):
        super().__init__()

        if parent != None:
            self.setParent(parent)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setObjectName('QtConeWidget')

        # *** Handle Argument Variables ***
        default_efficacy = 3.00
        default_resistance = 0.0095
        default_sensitivity = 0.0095

        self._header = header
        self._hide_header = hide_header
        self._param_mult = param_mult
        self._font_size = font_size
        self._avg_efficacy = averages[0] if averages else default_efficacy
        self._avg_resistance = averages[1] if averages else default_resistance
        self._avg_sensitivity = averages[2] if averages else default_sensitivity

        # *** Set Up Theme Colors ***
        themes = Themes()
        self.themes = themes.items

        self.setup_widget()
        self.setStyleSheet("""
            QWidget#QtConeWidget {{
                background-color: {bg};
                border-radius: 8px;
            }}
        """.format(bg=self.themes["app_color"]["blue_one"]))

    def setup_widget(self):
        # *** Create Header Labels ***
        header_frame = QFrame(self)
        header_frame.setObjectName('header_frame')
        header_frame.setFrameShape(QFrame.Shape.NoFrame)
        header_frame.setFrameShadow(QFrame.Shadow.Raised)
        header_frame.setStyleSheet('QFrame#header_frame {border-radius: 7px; border: 1px solid black;}')

        category_label = QLabel(header_frame)
        category_label.setObjectName('category_label')
        category_label.setText('Lesion')
        category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        category_label.setStyleSheet('font-size: {f}px; color: {color}'.format(f=self._font_size, color=self.themes['app_color']['dark_one']))

        self.header_label = QLabel(header_frame)
        self.header_label.setObjectName(u'header_label')
        self.header_label.setText(self._header)
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setStyleSheet('font-size: {f}px; color: {color}; font-weight: bold;'.format(f=self._font_size, color=self.themes['app_color']['dark_one']))

        header_layout = QVBoxLayout(header_frame)
        header_layout.setObjectName('header_layout')
        header_layout.setContentsMargins(5, 5, 5, 5)
        header_layout.setSpacing(3)
        header_layout.addWidget(category_label, alignment=Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.header_label, alignment=Qt.AlignmentFlag.AlignCenter)

        if self._hide_header:
            header_frame.hide()

        # *** Create Labels ***
        range_label_frame = QFrame(self)
        range_label_frame.setObjectName('range_label_frame')
        range_label_frame.setFrameShape(QFrame.Shape.NoFrame)
        range_label_frame.setFrameShadow(QFrame.Shadow.Raised)
        range_label_frame.setStyleSheet("""
            QFrame#range_label_frame {{
                border: none;
                border-right: 1px solid black;
                border-radius: 0px;
            }}
            QFrame QLabel {{
                font-size: {_font_size}px;
                color: {color};
            }}
        """.format(_font_size=self._font_size, color=self.themes['app_color']['dark_one']))

        min_label = QLabel(range_label_frame)
        min_label.setObjectName('min_label')
        min_label.setText('Min')
        min_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        avg_label = QLabel(range_label_frame)
        avg_label.setObjectName('avg_label')
        avg_label.setText('Avg')
        avg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        max_label = QLabel(range_label_frame)
        max_label.setObjectName('max_label')
        max_label.setText('Max')
        max_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        range_label_layout = QVBoxLayout(range_label_frame)
        range_label_layout.setObjectName('range_label_layout')
        range_label_layout.setContentsMargins(5, 5, 5, 5)
        range_label_layout.setSpacing(15)
        range_label_layout.addWidget(min_label, alignment=Qt.AlignmentFlag.AlignCenter)
        range_label_layout.addWidget(avg_label, alignment=Qt.AlignmentFlag.AlignCenter)
        range_label_layout.addWidget(max_label, alignment=Qt.AlignmentFlag.AlignCenter)

        param_label_frame = QFrame(self)
        param_label_frame.setObjectName('param_label_frame')
        param_label_frame.setFrameShape(QFrame.Shape.NoFrame)
        param_label_frame.setFrameShadow(QFrame.Shadow.Raised)
        param_label_frame.setStyleSheet("""
            QFrame#param_label_frame {{
                border: none;
                border-bottom: 1px solid black;
                border-radius: 0px;
            }}
            QFrame QLabel {{
                font-size: {_font_size}px;
                color: {color};
            }}
        """.format(_font_size=self._font_size, color=self.themes['app_color']['dark_one']))

        efficacy_label = QLabel(param_label_frame)
        efficacy_label.setObjectName('efficacy_label')
        efficacy_label.setText('Efficacy')
        efficacy_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        resistance_label = QLabel(param_label_frame)
        resistance_label.setObjectName('resistance_label')
        resistance_label.setText('Resistance')
        resistance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sensitivity_label = QLabel(param_label_frame)
        sensitivity_label.setObjectName('sensitivity_label')
        sensitivity_label.setText('Sensitivity')
        sensitivity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        param_label_layout = QHBoxLayout(param_label_frame)
        param_label_layout.setObjectName('param_label_layout')
        param_label_layout.setContentsMargins(5, 5, 5, 5)
        param_label_layout.setSpacing(20)
        param_label_layout.addWidget(efficacy_label, alignment=Qt.AlignmentFlag.AlignCenter)
        param_label_layout.addWidget(resistance_label, alignment=Qt.AlignmentFlag.AlignCenter)
        param_label_layout.addWidget(sensitivity_label, alignment=Qt.AlignmentFlag.AlignCenter)

        param_label_frame.setFixedHeight(param_label_layout.sizeHint().height())

        # *** Create Min Inputs ***
        min_input_space = QFrame(self)
        min_input_space.setObjectName('min_input_space')
        min_input_space.setFrameShape(QFrame.Shape.NoFrame)
        min_input_space.setFrameShadow(QFrame.Shadow.Raised)

        mult_holder = self._avg_efficacy * self._param_mult
        self.min_efficacy_box = QtNumEntry(
            font_size=self._font_size,
            bg_color=self.themes['app_color']['dark_one'],
            parent=min_input_space
        )
        self.min_efficacy_box.setObjectName('min_efficacy_box')
        self.min_efficacy_box.setDecimals(2)
        self.min_efficacy_box.setRange(0, 100)
        self.min_efficacy_box.setValue(mult_holder)
        self.min_efficacy_box.setFixedSize(60, 28)

        self.min_resistance_box = QtNumEntry(
            font_size=self._font_size,
            bg_color=self.themes['app_color']['dark_one'],
            parent=min_input_space
        )
        self.min_resistance_box.setObjectName('min_resistance_box')
        self.min_resistance_box.setDecimals(4)
        self.min_resistance_box.setRange(0, 10)
        self.min_resistance_box.setValue(0.0095)
        self.min_resistance_box.setFixedSize(60, 28)

        self.min_sensitivity_box = QtNumEntry(
            font_size=self._font_size,
            bg_color=self.themes['app_color']['dark_one'],
            parent=min_input_space
        )
        self.min_sensitivity_box.setObjectName('min_sensitivity_box')
        self.min_sensitivity_box.setDecimals(4)
        self.min_sensitivity_box.setRange(0, 10)
        self.min_sensitivity_box.setValue(0.0095)
        self.min_sensitivity_box.setFixedSize(60, 28)

        min_input_space_layout = QHBoxLayout(min_input_space)
        min_input_space_layout.setObjectName('min_input_space_layout')
        min_input_space_layout.setContentsMargins(0, 0, 0, 0)
        min_input_space_layout.setSpacing(20)
        min_input_space_layout.addWidget(self.min_efficacy_box, alignment=Qt.AlignmentFlag.AlignCenter)
        min_input_space_layout.addWidget(self.min_resistance_box, alignment=Qt.AlignmentFlag.AlignCenter)
        min_input_space_layout.addWidget(self.min_sensitivity_box, alignment=Qt.AlignmentFlag.AlignCenter)

        # *** Create Average Inputs ***
        avg_input_space = QFrame(self)
        avg_input_space.setObjectName('avg_input_space')
        avg_input_space.setFrameShape(QFrame.Shape.NoFrame)
        avg_input_space.setFrameShadow(QFrame.Shadow.Raised)

        self.avg_efficacy_box = QtNumEntry(
            font_size=self._font_size,
            bg_color=self.themes['app_color']['dark_one'],
            parent=avg_input_space
        )
        self.avg_efficacy_box.setObjectName('avg_efficacy_box')
        self.avg_efficacy_box.setDecimals(2)
        self.avg_efficacy_box.setRange(0, 100)
        self.avg_efficacy_box.setValue(self._avg_efficacy)
        self.avg_efficacy_box.setFixedSize(60, 28)

        self.avg_resistance_box = QtNumEntry(
            font_size=self._font_size,
            bg_color=self.themes['app_color']['dark_one'],
            parent=avg_input_space
        )
        self.avg_resistance_box.setObjectName('avg_resistance_box')
        self.avg_resistance_box.setDecimals(4)
        self.avg_resistance_box.setRange(0, 10)
        self.avg_resistance_box.setValue(self._avg_resistance)
        self.avg_resistance_box.setFixedSize(60, 28)

        self.avg_sensitivity_box = QtNumEntry(
            font_size=self._font_size,
            bg_color=self.themes['app_color']['dark_one'],
            parent=avg_input_space
        )
        self.avg_sensitivity_box.setObjectName('min_sensitivity_box')
        self.avg_sensitivity_box.setDecimals(4)
        self.avg_sensitivity_box.setRange(0, 10)
        self.avg_sensitivity_box.setValue(self._avg_sensitivity)
        self.avg_sensitivity_box.setFixedSize(60, 28)

        avg_input_space_layout = QHBoxLayout(avg_input_space)
        avg_input_space_layout.setObjectName('avg_input_space_layout')
        avg_input_space_layout.setContentsMargins(0, 0, 0, 0)
        avg_input_space_layout.setSpacing(20)
        avg_input_space_layout.addWidget(self.avg_efficacy_box, alignment=Qt.AlignmentFlag.AlignCenter)
        avg_input_space_layout.addWidget(self.avg_resistance_box, alignment=Qt.AlignmentFlag.AlignCenter)
        avg_input_space_layout.addWidget(self.avg_sensitivity_box, alignment=Qt.AlignmentFlag.AlignCenter)

        # *** Create Max Inputs ***
        max_input_space = QFrame(self)
        max_input_space.setObjectName('max_input_space')
        max_input_space.setFrameShape(QFrame.Shape.NoFrame)
        max_input_space.setFrameShadow(QFrame.Shadow.Raised)
        max_input_space.setStyleSheet("""
            QFrame#max_input_space > QLabel {{
                color: red;
            }}
        """)

        mult_holder = self._avg_efficacy + (self._avg_efficacy * self._param_mult)
        self.max_efficacy_box = QtNumEntry(
            font_size=self._font_size,
            bg_color=self.themes['app_color']['dark_one'],
            parent=max_input_space
        )
        self.max_efficacy_box.setObjectName('max_efficacy_box')
        self.max_efficacy_box.setDecimals(2)
        self.max_efficacy_box.setRange(0, 100)
        self.max_efficacy_box.setValue(mult_holder)
        self.max_efficacy_box.setFixedSize(60, 28)

        self.max_resistance_box = QtNumEntry(
            font_size=self._font_size,
            bg_color=self.themes['app_color']['dark_one'],
            parent=max_input_space
        )
        self.max_resistance_box.setObjectName('max_resistance_box')
        self.max_resistance_box.setDecimals(4)
        self.max_resistance_box.setRange(0, 10)
        self.max_resistance_box.setValue(0.0095)
        self.max_resistance_box.setFixedSize(60, 28)

        self.max_sensitivity_box = QtNumEntry(
            font_size=self._font_size,
            bg_color=self.themes['app_color']['dark_one'],
            parent=max_input_space
        )
        self.max_sensitivity_box.setObjectName('max_sensitivity_box')
        self.max_sensitivity_box.setDecimals(4)
        self.max_sensitivity_box.setRange(0, 10)
        self.max_sensitivity_box.setValue(0.0095)
        self.max_sensitivity_box.setFixedSize(60, 28)

        max_input_space_layout = QHBoxLayout(max_input_space)
        max_input_space_layout.setObjectName('max_input_space_layout')
        max_input_space_layout.setContentsMargins(0, 0, 0, 0)
        max_input_space_layout.setSpacing(20)
        max_input_space_layout.addWidget(self.max_efficacy_box, alignment=Qt.AlignmentFlag.AlignCenter)
        max_input_space_layout.addWidget(self.max_resistance_box, alignment=Qt.AlignmentFlag.AlignCenter)
        max_input_space_layout.addWidget(self.max_sensitivity_box, alignment=Qt.AlignmentFlag.AlignCenter)

        # *** Put Everything Together ***
        main_layout = QGridLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(header_frame, 0, 0, 4, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(range_label_frame, 1, 1, 3, 1)
        main_layout.addWidget(param_label_frame, 0, 2, 1, 3)
        main_layout.addWidget(min_input_space, 1, 2, 1, 3)
        main_layout.addWidget(avg_input_space, 2, 2, 1, 3)
        main_layout.addWidget(max_input_space, 3, 2, 1, 3)

        self.setMinimumSize(main_layout.sizeHint().width() + 15, main_layout.sizeHint().height() + 5)

    def set_param_mult(self, new_mult: float):
        self._param_mult = new_mult

    def reassign_values(self, new_values, mult_rs: bool = False):
        avg_d, avg_r, avg_s = new_values

        self.min_efficacy_box.setValue(avg_d * self._param_mult)
        self.max_efficacy_box.setValue(avg_d + (avg_d * self._param_mult))
        if mult_rs:
            self.min_resistance_box.setValue(avg_r * self._param_mult)
            self.min_sensitivity_box.setValue(avg_s * self._param_mult)
            self.max_resistance_box.setValue(avg_r + (avg_r * self._param_mult))
            self.max_sensitivity_box.setValue(avg_s + (avg_s * self._param_mult))

    def set_min_values(self, min_values: list):
        self.min_efficacy_box.setValue(min_values[0])
        self.min_resistance_box.setValue(min_values[1])
        self.min_sensitivity_box.setValue(min_values[2])

    def set_max_values(self, max_values: list):
        self.max_efficacy_box.setValue(max_values[0])
        self.max_resistance_box.setValue(max_values[1])
        self.max_sensitivity_box.setValue(max_values[2])

    def get_min_values(self) -> list:
        return [self.min_efficacy_box.value(), self.min_resistance_box.value(), self.min_sensitivity_box.value()]

    def get_max_values(self) -> list:
        return [self.max_efficacy_box.value(), self.max_resistance_box.value(), self.max_sensitivity_box.value()]

    def get_rates(self):
        min_rates = self.get_min_values()
        max_rates = self.get_max_values()

        return [min_rates, max_rates]

    def get_average_values(self):
        return [self.avg_efficacy_box.value(), self.avg_resistance_box.value(), self.avg_sensitivity_box.value()]

    def get_header(self):
        return self._header

    def set_regiment(self, new_regiment: str):
        self.header_label.setText(new_regiment)

    def check_efficacy_boundaries(self, widget: QtNumEntry):
        value = widget.value()

        if widget.objectName() == "min_efficacy_box":
            if value >= self.max_efficacy_box.value():
                widget.setValue(self.max_efficacy_box.value() - 0.01)
        elif widget.objectName() == "max_efficacy_box":
            if value <= self.min_efficacy_box.value():
                widget.setValue(self.max_efficacy_box.value() + 0.01)

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, o, p, self)
