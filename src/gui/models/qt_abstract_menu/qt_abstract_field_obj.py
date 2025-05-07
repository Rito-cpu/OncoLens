from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.gui.models.qt_line_button import QtButtonLineEdit, EnhancedLineEdit
from src.gui.models.qt_combo_widget import QtComboBox
from src.gui.models import PyToggle


class QtAbstractFieldWidget(QWidget):
    def __init__(
        self,
        setting_name: str,
        sheet_list: list,
        data_types: list = ["DateTime", "Float", "Integer", "String"],
        measurement_units: list = [],
        font_size: int = 12,
        plot_option: bool = False,
        parent=None
    ):
        super().__init__(parent)

        if parent is not None:
            self.setParent(parent)

        themes = Themes()
        self.themes = themes.items
        self._setting_name = setting_name
        self._sheet_list = sheet_list
        self._data_types = data_types
        self._measurement_units = measurement_units
        self._plot_option = plot_option
        self._font_size = font_size

        self._setup_widget()

    def _setup_widget(self):
        title_frame = QFrame(self)
        title_frame.setObjectName('title_frame')
        title_frame.setFrameShape(QFrame.Shape.NoFrame)
        title_frame.setFrameShadow(QFrame.Shadow.Plain)
        title_frame.setStyleSheet(f"""
            QFrame#title_frame {{
                border: none;
                background: {self.themes['app_color']['icon_active']};
                border-top-right-radius: 8px;
                border-top-left-radius: 8px;
            }}
        """)

        title_label = QLabel(title_frame)
        title_label.setObjectName('title_label')
        title_label.setText(self._setting_name)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(f'color: {self.themes["app_color"]["dark_one"]}; font-size: 15px; font-weight: bold;')

        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(5, 5, 5, 5)
        title_layout.addWidget(title_label)
        title_frame.setFixedHeight(title_layout.sizeHint().height() + 5)
        title_frame.setFixedWidth(title_layout.sizeHint().width() + 5)

        outer_frame = QFrame(self)
        outer_frame.setObjectName('outer_frame')
        outer_frame.setFrameShape(QFrame.Shape.NoFrame)
        outer_frame.setFrameShadow(QFrame.Shadow.Plain)
        outer_frame.setStyleSheet(f"""
            QFrame#outer_frame {{
                border: none;
                border-radius: 8px;
                background: {self.themes['app_color']['icon_active']};
            }}
        """)

        field_frame = QFrame(outer_frame)
        field_frame.setObjectName('field_frame')
        field_frame.setFrameShape(QFrame.Shape.NoFrame)
        field_frame.setFrameShadow(QFrame.Shadow.Plain)

        field_label = QLabel(field_frame)
        field_label.setObjectName('field_label')
        field_label.setText('Field Name:')
        field_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        field_label.setStyleSheet(f'font-size: {self._font_size}px; color: {self.themes["app_color"]["text_title"]};')

        #self.field_entry = QtButtonLineEdit(
        #    title="",
        #    title_color=self.themes["app_color"]["text_foreground"],
        #    color_three=self.themes['app_color']['green_two'],
        #    top_margin=18,
        #    parent=field_frame
        #)
        self.field_entry = EnhancedLineEdit(parent=field_frame)
        self.field_entry.setFixedHeight(28)
        self.field_entry.setMinimumWidth(140)
        self.field_entry.setPlaceholderText("Enter field name")
        self.field_entry.setCursor(Qt.CursorShape.IBeamCursor)
        self.field_entry.configure_self()

        field_layout = QHBoxLayout(field_frame)
        field_layout.setContentsMargins(0, 0, 0, 0)
        field_layout.setSpacing(7)
        field_layout.addWidget(field_label)
        field_layout.addWidget(self.field_entry)

        # FIXME: ONLY for excel
        sheet_frame = QFrame(outer_frame)
        sheet_frame.setObjectName('sheet_frame')
        sheet_frame.setFrameShape(QFrame.Shape.NoFrame)
        sheet_frame.setFrameShadow(QFrame.Shadow.Plain)

        sheet_label = QLabel(sheet_frame)
        sheet_label.setObjectName('sheet_label')
        sheet_label.setText("Source Sheet:")
        sheet_label.setStyleSheet(f'font-size: {self._font_size}px; color: {self.themes["app_color"]["text_foreground"]};')
        sheet_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.source_sheet_combo = QtComboBox(
            bg_color=self.themes["app_color"]["dark_three"],
            text_color=self.themes["app_color"]["white"],
            parent=sheet_frame
        )
        self.source_sheet_combo.setObjectName('source_sheet_combo')
        self.source_sheet_combo.addItems(self._sheet_list)
        self.source_sheet_combo.setCurrentIndex(0)
        self.source_sheet_combo.setFixedHeight(23)
        self.source_sheet_combo.setMinimumWidth(100)
        self.source_sheet_combo.setCursor(Qt.CursorShape.PointingHandCursor)

        sheet_layout = QHBoxLayout(sheet_frame)
        sheet_layout.setContentsMargins(0, 0, 0, 0)
        sheet_layout.setSpacing(7)
        sheet_layout.addWidget(sheet_label)
        sheet_layout.addWidget(self.source_sheet_combo)

        data_type_frame = QFrame(outer_frame)
        data_type_frame.setObjectName('data_type_frame')
        data_type_frame.setFrameShape(QFrame.Shape.NoFrame)
        data_type_frame.setFrameShadow(QFrame.Shadow.Plain)

        data_type_label = QLabel(data_type_frame)
        data_type_label.setObjectName('data_type_label')
        data_type_label.setText("Data Type:")
        data_type_label.setStyleSheet(f'font-size: {self._font_size}px; color: {self.themes["app_color"]["text_foreground"]};')
        data_type_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.data_type_combo = QtComboBox(
            bg_color=self.themes["app_color"]["dark_three"],
            text_color=self.themes["app_color"]["white"],
            parent=data_type_frame
        )
        self.data_type_combo.setObjectName('data_type_combo')
        self.data_type_combo.addItems(self._data_types)
        self.data_type_combo.setCurrentIndex(0)
        self.data_type_combo.setFixedHeight(23)
        self.data_type_combo.setMinimumWidth(100)
        self.data_type_combo.setCursor(Qt.CursorShape.PointingHandCursor)

        data_type_layout = QHBoxLayout(data_type_frame)
        data_type_layout.setContentsMargins(0, 0, 0, 0)
        data_type_layout.setSpacing(7)
        data_type_layout.addWidget(data_type_label)
        data_type_layout.addWidget(self.data_type_combo)

        unit_frame = QFrame(outer_frame)
        unit_frame.setObjectName('unit_frame')
        unit_frame.setFrameShape(QFrame.Shape.NoFrame)
        unit_frame.setFrameShadow(QFrame.Shadow.Plain)

        unit_label = QLabel(unit_frame)
        unit_label.setObjectName('unit_label')
        unit_label.setText("Unit Type:")
        unit_label.setStyleSheet(f'font-size: {self._font_size}px; color: {self.themes["app_color"]["text_foreground"]};')
        unit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.unit_entry = EnhancedLineEdit(parent=unit_frame)
        self.unit_entry.setFixedHeight(28)
        self.unit_entry.setMinimumWidth(110)
        self.unit_entry.setPlaceholderText("Enter unit type")
        self.unit_entry.setCursor(Qt.CursorShape.IBeamCursor)
        self.unit_entry.configure_self()

        unit_layout = QHBoxLayout(unit_frame)
        unit_layout.setContentsMargins(0, 0, 0, 0)
        unit_layout.setSpacing(7)
        unit_layout.addWidget(unit_label)
        unit_layout.addWidget(self.unit_entry)

        plot_option_frame = QFrame(outer_frame)
        plot_option_frame.setObjectName('plot_option_frame')
        plot_option_frame.setFrameShape(QFrame.Shape.NoFrame)
        plot_option_frame.setFrameShadow(QFrame.Shadow.Plain)

        plot_option_label = QLabel(plot_option_frame)
        plot_option_label.setObjectName('plot_option_label')
        plot_option_label.setText("Plot:")
        plot_option_label.setStyleSheet(f'font-size: {self._font_size}px; color: {self.themes["app_color"]["text_foreground"]};')
        plot_option_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.plot_option_toggle = PyToggle(
            width=28,
            height=16,
            ellipse_y=2,
            bg_color = self.themes["app_color"]["dark_two"],
            circle_color = self.themes["app_color"]["white"],
            active_color = self.themes["app_color"]["green_two"],
            parent=plot_option_frame
        )
        self.plot_option_toggle.setObjectName("plot_option_toggle")
        self.plot_option_toggle.setChecked(False)
        self.plot_option_toggle.setCursor(Qt.CursorShape.PointingHandCursor)

        plot_option_layout = QHBoxLayout(plot_option_frame)
        plot_option_layout.setContentsMargins(0, 0, 0, 0)
        plot_option_layout.setSpacing(7)
        plot_option_layout.addWidget(plot_option_label)
        plot_option_layout.addWidget(self.plot_option_toggle)

        if not self._plot_option:
            plot_option_frame.hide()

        outer_layout = QGridLayout(outer_frame)
        outer_layout.setContentsMargins(5, 8, 5, 8)
        outer_layout.setSpacing(6)
        outer_layout.addWidget(field_frame, 0, 0, 1, 4, alignment=Qt.AlignmentFlag.AlignCenter)
        outer_layout.addWidget(sheet_frame, 1, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        outer_layout.addWidget(unit_frame, 1, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        outer_layout.addWidget(data_type_frame, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        outer_layout.addWidget(plot_option_frame, 2, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        outer_frame.setFixedHeight(outer_layout.sizeHint().height() + 10)
        outer_frame.setFixedWidth(outer_layout.sizeHint().width() + 10)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addStretch()
        main_layout.addWidget(title_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(outer_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()
