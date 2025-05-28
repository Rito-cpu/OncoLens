from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.core.app_config import IMG_RSC_PATH
from src.gui.models.qt_line_button import QtButtonLineEdit, EnhancedLineEdit
from src.gui.models.qt_combo_widget import QtComboBox
from src.gui.models import PyToggle, QtMessage


class QtAbstractFieldWidget(QWidget):
    def __init__(
        self,
        setting_name: str,
        field_list: list,
        sheet_list: list = None,
        excel_obj = None,
        data_types: list = ["DateTime", "Float", "Integer", "String"],
        measurement_units: list = [],
        font_size: int = 12,
        is_x_var: bool = False,
        is_treatment: bool = False,
        parent=None
    ):
        super().__init__(parent)

        if parent is not None:
            self.setParent(parent)

        themes = Themes()
        self.themes = themes.items
        self._field_list = field_list
        self._setting_name = setting_name
        self._sheet_list = sheet_list
        self._excel_obj = excel_obj
        self._data_types = data_types
        self._measurement_units = measurement_units
        self._font_size = font_size
        self._is_x_var = is_x_var
        self._is_treatment = is_treatment
        self._plot_styles = ["Line", "Scatter", "Event Marker"]
        self._axis_styles = ["Primary", "Secondary"]
        self._scale_styles = ["Linear", "Log", "Log (2)", "Log (10)", "n/a"]
        self._normalization_styles = ["Min-Max", "Z-Score", "None"]

        if is_treatment:
            data_types = ["String"]

        self._state_settings = {
            "is_excel": excel_obj,
            "is_x_var": is_x_var,
            "is_treatment": is_treatment,
            "field": None,
            "sheet": None,
            "unit_type": None,
            "dtype": None,
            "plot_option": False,
            "plot_style": None,
            "axis": None,
            "normalize": False,
            "scale": None
        }

        self._setup_widget()
        if excel_obj is not None:
            self.source_sheet_combo.currentIndexChanged.connect(self.change_field_options)

    def _setup_widget(self):
        label_style = f"""
            QLabel {{
                font-size: {self._font_size}px;
                color: {self.themes["app_color"]["text_foreground_two"]};
            }}
        """
        
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

        #self.delete_bttn = QToolButton(title_frame)
        #self.delete_bttn.setObjectName('delete_bttn')
        #self.delete_bttn.setIcon(QIcon(str(IMG_RSC_PATH / "svg_icons" / "down-arrow.svg")))
        #self.delete_bttn.setIconSize(QSize(15, 15))
        #self.delete_bttn.setCursor(Qt.CursorShape.PointingHandCursor)

        title_layout = QHBoxLayout(title_frame)
        title_layout.setContentsMargins(5, 5, 5, 5)
        title_layout.setSpacing(12)
        title_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        #title_layout.addWidget(self.delete_bttn, alignment=Qt.AlignmentFlag.AlignCenter)
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
        field_label.setStyleSheet(label_style)

        self.field_combo = QtComboBox(
            bg_color=self.themes["app_color"]["dark_three"],
            text_color=self.themes["app_color"]["white"],
            green_color=self.themes["app_color"]["green_two"],
            alternate_bg=self.themes["app_color"]["bg_two"],
            parent=field_frame
        )
        self.field_combo.setObjectName('field_combo')
        self.field_combo.addItems(self._field_list)
        self.field_combo.setCurrentIndex(0)
        self.field_combo.setFixedHeight(23)
        self.field_combo.setMinimumWidth(125)
        self.field_combo.setCursor(Qt.CursorShape.PointingHandCursor)

        field_layout = QHBoxLayout(field_frame)
        field_layout.setContentsMargins(0, 0, 0, 0)
        field_layout.setSpacing(7)
        field_layout.addWidget(field_label)
        field_layout.addWidget(self.field_combo)

        sheet_frame = QFrame(outer_frame)
        sheet_frame.setObjectName('sheet_frame')
        sheet_frame.setFrameShape(QFrame.Shape.NoFrame)
        sheet_frame.setFrameShadow(QFrame.Shadow.Plain)

        sheet_label = QLabel(sheet_frame)
        sheet_label.setObjectName('sheet_label')
        sheet_label.setText("Source Sheet:")
        sheet_label.setStyleSheet(label_style)
        sheet_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.source_sheet_combo = QtComboBox(
            bg_color=self.themes["app_color"]["dark_three"],
            text_color=self.themes["app_color"]["white"],
            green_color=self.themes["app_color"]["green_two"],
            alternate_bg=self.themes["app_color"]["bg_two"],
            parent=sheet_frame
        )
        self.source_sheet_combo.setObjectName('source_sheet_combo')
        if self._sheet_list is None:
            self.source_sheet_combo.setEnabled(False)
            sheet_frame.hide()
        else:
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
        data_type_label.setStyleSheet(label_style)
        data_type_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.data_type_combo = QtComboBox(
            bg_color=self.themes["app_color"]["dark_three"],
            text_color=self.themes["app_color"]["white"],
            green_color=self.themes["app_color"]["green_two"],
            alternate_bg=self.themes["app_color"]["bg_two"],
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
        unit_label.setStyleSheet(label_style)
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
        plot_option_label.setStyleSheet(label_style)
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

        plot_style_frame = QFrame(outer_frame)
        plot_style_frame.setObjectName('plot_style_frame')
        plot_style_frame.setFrameShape(QFrame.Shape.NoFrame)
        plot_style_frame.setFrameShadow(QFrame.Shadow.Plain)

        plot_style_label = QLabel(plot_style_frame)
        plot_style_label.setObjectName('plot_style_label')
        plot_style_label.setText("Plot Style:")
        plot_style_label.setStyleSheet(label_style)
        plot_style_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.plot_style_combo = QtComboBox(
            bg_color=self.themes["app_color"]["dark_three"],
            text_color=self.themes["app_color"]["white"],
            green_color=self.themes["app_color"]["green_two"],
            alternate_bg=self.themes["app_color"]["bg_two"],
            parent=plot_style_frame
        )
        self.plot_style_combo.setObjectName('plot_style_combo')
        self.plot_style_combo.addItems(self._plot_styles)
        self.plot_style_combo.setCurrentIndex(0)
        self.plot_style_combo.setFixedHeight(23)
        self.plot_style_combo.setMinimumWidth(100)
        self.plot_style_combo.setCursor(Qt.CursorShape.PointingHandCursor)

        plot_style_layout = QHBoxLayout(plot_style_frame)
        plot_style_layout.setContentsMargins(0, 0, 0, 0)
        plot_style_layout.setSpacing(7)
        plot_style_layout.addWidget(plot_style_label)
        plot_style_layout.addWidget(self.plot_style_combo)

        normalization_frame = QFrame(outer_frame)
        normalization_frame.setObjectName('normalization_frame')
        normalization_frame.setFrameShape(QFrame.Shape.NoFrame)
        normalization_frame.setFrameShadow(QFrame.Shadow.Plain)

        normalization_label = QLabel(normalization_frame)
        normalization_label.setObjectName('normalization_label')
        normalization_label.setText("Normalize:")
        normalization_label.setStyleSheet(label_style)
        normalization_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.normalize_combo = QtComboBox(
            bg_color=self.themes["app_color"]["dark_three"],
            text_color=self.themes["app_color"]["white"],
            green_color=self.themes["app_color"]["green_two"],
            alternate_bg=self.themes["app_color"]["bg_two"],
            parent=normalization_frame
        )
        self.normalize_combo.setObjectName('normalize_combo')
        self.normalize_combo.addItems(self._normalization_styles)
        self.normalize_combo.setCurrentText("None")
        self.normalize_combo.setFixedHeight(23)
        self.normalize_combo.setMinimumWidth(100)
        self.normalize_combo.setCursor(Qt.CursorShape.PointingHandCursor)

        normalization_layout = QHBoxLayout(normalization_frame)
        normalization_layout.setContentsMargins(0, 0, 0, 0)
        normalization_layout.setSpacing(7)
        normalization_layout.addWidget(normalization_label)
        normalization_layout.addWidget(self.normalize_combo)

        axis_frame = QFrame(outer_frame)
        axis_frame.setObjectName('axis_frame')
        axis_frame.setFrameShape(QFrame.Shape.NoFrame)
        axis_frame.setFrameShadow(QFrame.Shadow.Plain)

        axis_label = QLabel(axis_frame)
        axis_label.setObjectName('axis_label')
        axis_label.setText("Axis:")
        axis_label.setStyleSheet(label_style)
        axis_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.axis_combo = QtComboBox(
            bg_color=self.themes["app_color"]["dark_three"],
            text_color=self.themes["app_color"]["white"],
            green_color=self.themes["app_color"]["green_two"],
            alternate_bg=self.themes["app_color"]["bg_two"],
            parent=axis_frame
        )
        self.axis_combo.setObjectName('axis_combo')
        self.axis_combo.addItems(self._axis_styles)
        self.axis_combo.setCurrentIndex(0)
        self.axis_combo.setFixedHeight(23)
        self.axis_combo.setMinimumWidth(100)
        self.axis_combo.setCursor(Qt.CursorShape.PointingHandCursor)

        axis_layout = QHBoxLayout(axis_frame)
        axis_layout.setContentsMargins(0, 0, 0, 0)
        axis_layout.setSpacing(7)
        axis_layout.addWidget(axis_label)
        axis_layout.addWidget(self.axis_combo)

        scale_frame = QFrame(outer_frame)
        scale_frame.setObjectName('scale_frame')
        scale_frame.setFrameShape(QFrame.Shape.NoFrame)
        scale_frame.setFrameShadow(QFrame.Shadow.Plain)

        scale_label = QLabel(scale_frame)
        scale_label.setObjectName('scale_label')
        scale_label.setText("Scale:")
        scale_label.setStyleSheet(label_style)
        scale_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.scale_combo = QtComboBox(
            bg_color=self.themes["app_color"]["dark_three"],
            text_color=self.themes["app_color"]["white"],
            green_color=self.themes["app_color"]["green_two"],
            alternate_bg=self.themes["app_color"]["bg_two"],
            parent=scale_frame
        )
        self.scale_combo.setObjectName('scale_combo')
        self.scale_combo.addItems(self._scale_styles)
        self.scale_combo.setCurrentIndex(0)
        self.scale_combo.setFixedHeight(23)
        self.scale_combo.setMinimumWidth(100)
        self.scale_combo.setCursor(Qt.CursorShape.PointingHandCursor)

        scale_layout = QHBoxLayout(scale_frame)
        scale_layout.setContentsMargins(0, 0, 0, 0)
        scale_layout.setSpacing(7)
        scale_layout.addWidget(scale_label)
        scale_layout.addWidget(self.scale_combo)

        custom_name_frame = QFrame(outer_frame)
        custom_name_frame.setObjectName('custom_name_frame')
        custom_name_frame.setFrameShape(QFrame.Shape.NoFrame)
        custom_name_frame.setFrameShadow(QFrame.Shadow.Plain)

        custom_name_label = QLabel(custom_name_frame)
        custom_name_label.setObjectName('custom_name_label')
        custom_name_label.setText("Visual Name:")
        custom_name_label.setStyleSheet(label_style)
        custom_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.custom_name_entry = EnhancedLineEdit(parent=custom_name_frame)
        self.custom_name_entry.setObjectName('custom_name_entry')
        self.custom_name_entry.setFixedHeight(28)
        self.custom_name_entry.setMinimumWidth(110)
        self.custom_name_entry.setCursor(Qt.CursorShape.IBeamCursor)
        self.custom_name_entry.setPlaceholderText("Enter a custom name")
        self.custom_name_entry.configure_self()

        custom_name_layout = QHBoxLayout(custom_name_frame)
        custom_name_layout.setContentsMargins(0, 0, 0, 0)
        custom_name_layout.setSpacing(7)
        custom_name_layout.addWidget(custom_name_label)
        custom_name_layout.addWidget(self.custom_name_entry)

        if self._is_x_var:
            # Add minimal settings
            outer_layout = QGridLayout(outer_frame)
            outer_layout.setContentsMargins(5, 8, 5, 8)
            outer_layout.setSpacing(6)
            outer_layout.addWidget(field_frame, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
            outer_layout.addWidget(data_type_frame, 1, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
            outer_layout.addWidget(unit_frame, 0, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
            outer_layout.addWidget(sheet_frame, 1, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
            #outer_layout.addWidget(plot_option_frame, 2, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
            #outer_layout.addWidget(plot_style_frame, 3, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
            #outer_layout.addWidget(normalization_frame, 3, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
            #outer_layout.addWidget(axis_frame, 4, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
            #outer_layout.addWidget(scale_frame, 4, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
            plot_option_frame.hide()
            plot_style_frame.hide()
            normalization_frame.hide()
            axis_frame.hide()
            scale_frame.hide()
            custom_name_frame.hide()
            outer_frame.setFixedHeight(outer_layout.sizeHint().height() + 10)
            outer_frame.setFixedWidth(outer_layout.sizeHint().width() + 10)
        else:
            outer_layout = QGridLayout(outer_frame)
            outer_layout.setContentsMargins(5, 8, 5, 8)
            outer_layout.setSpacing(6)
            outer_layout.addWidget(field_frame, 0, 0, 1, 4, alignment=Qt.AlignmentFlag.AlignCenter)
            outer_layout.addWidget(sheet_frame, 1, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
            if not self._is_treatment:
                outer_layout.addWidget(plot_option_frame, 2, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
                outer_layout.addWidget(data_type_frame, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
                outer_layout.addWidget(unit_frame, 1, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
                outer_layout.addWidget(plot_style_frame, 3, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
                outer_layout.addWidget(normalization_frame, 3, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
                outer_layout.addWidget(axis_frame, 4, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
                outer_layout.addWidget(scale_frame, 4, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
                custom_name_frame.hide()
            else:
                outer_layout.addWidget(plot_option_frame, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
                outer_layout.addWidget(data_type_frame, 1, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
                #outer_layout.addWidget(custom_name_frame, 2, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
                unit_frame.hide()
                plot_style_frame.hide()
                normalization_frame.hide()
                axis_frame.hide()
                scale_frame.hide()
                custom_name_frame.hide()

            outer_frame.setFixedHeight(outer_layout.sizeHint().height() + 10)
            outer_frame.setFixedWidth(outer_layout.sizeHint().width() + 10)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addStretch()
        main_layout.addWidget(title_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(outer_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()

    def change_field_options(self):
        msg_bttns = {
            "Ok": QMessageBox.ButtonRole.AcceptRole,
        }

        msg_box = QtMessage(
            buttons=msg_bttns,
            color=self.themes["app_color"]["white"],
            bg_color_one=self.themes["app_color"]["dark_one"],
            bg_color_two=self.themes["app_color"]["bg_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        msg_box.setIcon(QMessageBox.Icon.Critical)

        try:
            df = self._excel_obj.parse(self.source_sheet_combo.currentText())
            cols = df.columns.tolist()
            self.field_combo.clear()
            self.field_combo.addItems(cols)
        except Exception as e:
            msg_box.setText("Sheet Error")
            msg_box.setDetailedText("Encountered an error applying desired sheet fields to dropdown menu. Please ensure that the dataset is properly formatted.")
            msg_box.exec()
            return

    def get_x_values(self):
        if self._excel_obj:
            # if using Excel, use sheet value
            self._state_settings["field"] = self.field_combo.currentText()
            self._state_settings["unit_type"] = self.unit_entry.text()
            self._state_settings["sheet"] = self.source_sheet_combo.currentText()
            self._state_settings["dtype"] = self.data_type_combo.currentText()
        else:
            # if using csv, remove sheet value
            self._state_settings["field"] = self.field_combo.currentText()
            self._state_settings["unit_type"] = self.unit_entry.text()
            self._state_settings["dtype"] = self.data_type_combo.currentText()
        
        return self._state_settings

    def get_y_values(self):
        if self._excel_obj:
            # if using Excel data
            self._state_settings["field"] = self.field_combo.currentText()
            self._state_settings["unit_type"] = self.unit_entry.text()
            self._state_settings["sheet"] = self.source_sheet_combo.currentText()
            self._state_settings["dtype"] = self.data_type_combo.currentText()
            self._state_settings["plot_option"] = self.plot_option_toggle.isChecked()
            if not self._is_treatment:
                self._state_settings["plot_style"] = self.plot_style_combo.currentText()
                self._state_settings["normalize"] = self.normalize_combo.currentText()
                self._state_settings["axis"] = self.axis_combo.currentText()
                self._state_settings["scale"] = self.scale_combo.currentText()
        else:
            # if using csv, remove sheet value
            self._state_settings["field"] = self.field_combo.currentText()
            self._state_settings["unit_type"] = self.unit_entry.text()
            self._state_settings["dtype"] = self.data_type_combo.currentText()
            self._state_settings["plot_option"] = self.plot_option_toggle.isChecked()
            if not self._is_treatment:
                self._state_settings["plot_style"] = self.plot_style_combo.currentText()
                self._state_settings["normalize"] = self.normalize_combo.currentText()
                self._state_settings["axis"] = self.axis_combo.currentText()
                self._state_settings["scale"] = self.scale_combo.currentText()
        
        return self._state_settings

    def delete_widget(self):
        self.setParent(None)
        self.deleteLater()
