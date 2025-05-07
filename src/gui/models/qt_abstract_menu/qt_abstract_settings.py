from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from .qt_abstract_field_obj import QtAbstractFieldWidget
from src.gui.models.qt_collapsible_box import QtCollapsibleWidget
from src.gui.models.py_push_button import PyPushButton

MAX_COLS: int = 2


class QtAbstractSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        if parent is not None:
            self.setParent(parent)

        themes = Themes()
        self.themes = themes.items

        # Measurement related variables
        self.msrmnt_var_counter = 0
        self.msrmnt_y_list = []
        self.msrmnt_row_counter = 0
        self.msrmnt_col_counter = 1

        # Treatment related variables
        self.trtmnt_var_counter = 0
        self.trtmnt_y_list = []
        self.trtmnt_row_counter = 0
        self.trtmnt_col_counter = 1

        self._setup_widget()
        self.msrmnt_add_bttn.clicked.connect(self.add_measurement_variable)
        self.msrmnt_remove_bttn.clicked.connect(self.remove_measurement_variable)

    def _setup_widget(self):
        overall_frame = QFrame(self)
        overall_frame.setObjectName('overall_frame')
        overall_frame.setFrameShape(QFrame.Shape.NoFrame)
        overall_frame.setFrameShadow(QFrame.Shadow.Plain)

        # TODO: Think of - create scroll area here to separate title from menu contents?
        settings_title = QLabel(overall_frame)
        settings_title.setObjectName('settings_title')
        settings_title.setText('Abstract Data Settings')
        settings_title.setStyleSheet('font-size: 18px; font-weight: bold;')
        settings_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        settings_title.hide()

        # TODO: Settings - Column Definitions, Plot Options
        """
        Column Definitions:
            1. Expected Field Name(s)
            2. Expected Field Data Type (DateTime, Float, Int, String)
            3. Expected Field Unit (e.g., seconds, meters, etc.)
                3.5. Create into one dynamic widget

        Plot Options:
            1. What to plot (1, 2, or both)
            2. Add time range lines across plots
            3. Set min/max day?

        Measurement Plot (with toggle):
            select measurement(s) to be plotted
            Needs a minimum of: dates, measurements, names (column with names at values, or columns with names and measurements as values)
        Treatment Plot (with toggle):
        Plot Options:
        """

        # ***********************************
        # **** Measurement Plot Settings ****
        # ***********************************
        measurement_collapsible_setting = QtCollapsibleWidget(
            title='Measurement Plot',
            help_msg="This is a message",
            parent=overall_frame
        )

        msrmnt_scroll_area = QScrollArea(measurement_collapsible_setting)
        msrmnt_scroll_area.setObjectName('msrmnt_scroll_area')
        msrmnt_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        msrmnt_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        msrmnt_scroll_area.setWidgetResizable(True)

        self.measurement_area = QFrame(msrmnt_scroll_area)
        self.measurement_area.setFrameShape(QFrame.Shape.NoFrame)
        self.measurement_area.setFrameShadow(QFrame.Shadow.Plain)

        msrmnt_scroll_area.setWidget(self.measurement_area)

        self.msrmnt_var_ctrl_frame = QFrame(self.measurement_area)
        self.msrmnt_var_ctrl_frame.setObjectName('msrmnt_var_ctrl_frame')
        self.msrmnt_var_ctrl_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.msrmnt_var_ctrl_frame.setFrameShadow(QFrame.Shadow.Plain)
        self.msrmnt_var_ctrl_frame.setStyleSheet(f'QFrame#msrmnt_var_ctrl_frame {{background: {self.themes["app_color"]["text_active"]}; border-radius: 8px;}}')

        self.msrmnt_add_bttn = PyPushButton(
            text="Add",
            radius=8,
            color=self.themes["app_color"]["dark_three"],
            bg_color=self.themes["app_color"]["green_two"],
            bg_color_hover=self.themes["app_color"]["green"],
            bg_color_pressed=self.themes["app_color"]["green"],
            font_size=14,
            parent=self.msrmnt_var_ctrl_frame
        )
        self.msrmnt_add_bttn.setFixedHeight(28)

        self.msrmnt_remove_bttn = PyPushButton(
            text="Remove",
            radius=8,
            color=self.themes["app_color"]["dark_three"],
            bg_color=self.themes["app_color"]["red"],
            bg_color_hover=self.themes["app_color"]["red_two"],
            bg_color_pressed=self.themes["app_color"]["red_two"],
            font_size=14,
            parent=self.msrmnt_var_ctrl_frame
        )
        self.msrmnt_remove_bttn.setFixedHeight(28)

        msrmnt_ctrl_layout = QVBoxLayout(self.msrmnt_var_ctrl_frame)
        msrmnt_ctrl_layout.setContentsMargins(5, 5, 5, 5)
        msrmnt_ctrl_layout.setSpacing(15)
        msrmnt_ctrl_layout.addWidget(self.msrmnt_add_bttn)
        msrmnt_ctrl_layout.addWidget(self.msrmnt_remove_bttn)

        msrmnt_x_var = QtAbstractFieldWidget(
            setting_name="X-Variable",
            sheet_list=["s1", "s2", "s3", "s4"],
            plot_option=False,
            parent=self.measurement_area
        )

        self.msrmnt_area_layout = QGridLayout(self.measurement_area)
        self.msrmnt_area_layout.setContentsMargins(10, 10, 10, 10)
        self.msrmnt_area_layout.setSpacing(8)
        self.msrmnt_area_layout.setVerticalSpacing(25)
        self.msrmnt_area_layout.addWidget(msrmnt_x_var, 0, 0, 1, 1)
        self.msrmnt_area_layout.addWidget(self.msrmnt_var_ctrl_frame, 0, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        measurement_collapsible_setting.set_content(msrmnt_scroll_area)

        # ***********************************
        # **** Treatment Plot Settings ****
        # ***********************************
        treatment_collapsible_setting = QtCollapsibleWidget(
            title='Treatment Plot',
            help_msg="This is a message",
            parent=overall_frame
        )

        trtmnt_scroll_area = QScrollArea(treatment_collapsible_setting)
        trtmnt_scroll_area.setObjectName('trtmnt_scroll_area')
        trtmnt_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        trtmnt_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        trtmnt_scroll_area.setWidgetResizable(True)

        treatment_area = QFrame(trtmnt_scroll_area)
        treatment_area.setFrameShape(QFrame.Shape.NoFrame)
        treatment_area.setFrameShadow(QFrame.Shadow.Plain)

        trtmnt_scroll_area.setWidget(treatment_area)

        trtmnt_x_var = QtAbstractFieldWidget(
            setting_name="X-Variable",
            sheet_list=["s1", "s2", "s3", "s4"],
            plot_option=False,
            parent=treatment_area
        )

        trtmnt_y_var = QtAbstractFieldWidget(
            setting_name="Y-Variable",
            sheet_list=["s1", "s2", "s3", "s4"],
            plot_option=True,
            parent=treatment_area
        )

        trtmnt_area_layout = QHBoxLayout(treatment_area)
        trtmnt_area_layout.setContentsMargins(5, 5, 5, 5)
        trtmnt_area_layout.setSpacing(8)
        trtmnt_area_layout.addWidget(trtmnt_x_var)
        trtmnt_area_layout.addWidget(trtmnt_y_var)

        treatment_collapsible_setting.set_content(trtmnt_scroll_area)

        overall_layout = QVBoxLayout(overall_frame)
        overall_layout.setSpacing(15)
        overall_layout.setContentsMargins(0, 0, 0, 0)
        overall_layout.addWidget(measurement_collapsible_setting)
        overall_layout.addWidget(treatment_collapsible_setting)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(overall_frame)

    def add_measurement_variable(self):
        # Disable the layout to reduce UI flickering when adding/removing widgets
        self.msrmnt_area_layout.setEnabled(False)

        new_y_var = QtAbstractFieldWidget(
            setting_name=f"Y-Var {self.msrmnt_var_counter + 1}",
            sheet_list=["s1", "s2", "s3", "s4"],
            plot_option=True,
            parent=self.measurement_area
        )

        self.msrmnt_area_layout.addWidget(new_y_var, self.msrmnt_row_counter, self.msrmnt_col_counter, 1, 1)
        self.msrmnt_col_counter += 1
        self.msrmnt_y_list.append(new_y_var)
        self.msrmnt_var_counter += 1

        # Create new row
        if self.msrmnt_col_counter == MAX_COLS:
            self.msrmnt_row_counter += 1
            self.msrmnt_col_counter = 0

        self.msrmnt_area_layout.addWidget(
            self.msrmnt_var_ctrl_frame, 
            self.msrmnt_row_counter, 
            self.msrmnt_col_counter, 
            1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.msrmnt_area_layout.setEnabled(True)

    def remove_measurement_variable(self):
        if not self.msrmnt_y_list:
            return
        
        self.msrmnt_area_layout.setEnabled(False)

        last_var = self.msrmnt_y_list.pop()

        index = self.msrmnt_area_layout.indexOf(last_var)
        if index is not -1:
            item = self.msrmnt_area_layout.takeAt(index)
            w = item.widget()
            if w:
                w.deleteLater()

        if self.msrmnt_col_counter == 0:
            self.msrmnt_row_counter -= 1
            self.msrmnt_col_counter = 1
        else:
            self.msrmnt_col_counter = 0
        self.msrmnt_var_counter -= 1

        index_bttn = self.msrmnt_area_layout.indexOf(self.msrmnt_var_ctrl_frame)
        if index_bttn is not -1:
            self.msrmnt_area_layout.takeAt(index_bttn)

        self.msrmnt_area_layout.addWidget(
            self.msrmnt_var_ctrl_frame,
            self.msrmnt_row_counter,
            self.msrmnt_col_counter,
            1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.msrmnt_area_layout.setEnabled(True)

    def add_treatment_variable(self):
        pass
