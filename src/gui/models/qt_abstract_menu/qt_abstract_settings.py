from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from .qt_abstract_field_obj import QtAbstractFieldWidget
from src.gui.models.qt_collapsible_box import QtCollapsibleWidget
from src.gui.models.py_push_button import PyPushButton
from src.gui.models.py_toggle import PyToggle
from src.gui.models.qt_basic_settings import SettingsGroupBox
from src.gui.models.qt_message import QtMessage

MAX_COLS: int = 2


class QtAbstractSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        if parent is not None:
            self.setParent(parent)

        themes = Themes()
        self.themes = themes.items
        self.title = "Abstract Visualization Settings"
        self._file_settings = None

        # Measurement related variables
        self.msrmnt_var_counter = 0
        self.msrmnt_y_list = []
        self.msrmnt_row_counter = 0
        self.msrmnt_col_counter = 0
        self.max_cols = 0

        # Treatment related variables
        self.trtmnt_var_counter = 0
        self.trtmnt_y_list = []
        self.trtmnt_row_counter = 0
        self.trtmnt_col_counter = 0

        self._setup_widget()
        self.msrmnt_add_bttn.clicked.connect(self.add_measurement_variable)
        self.msrmnt_remove_bttn.clicked.connect(self.remove_measurement_variable)
        self.trtmnt_add_bttn.clicked.connect(self.add_treatment_variable)
        self.trtmnt_remove_bttn.clicked.connect(self.remove_treatment_variable)
        self.submit_data_bttn.clicked.connect(self.submit_widgets)

    def _setup_widget(self):
        overall_frame = QFrame(self)
        overall_frame.setObjectName('overall_frame')
        overall_frame.setFrameShape(QFrame.Shape.NoFrame)
        overall_frame.setFrameShadow(QFrame.Shadow.Plain)

        settings_title = QLabel(overall_frame)
        settings_title.setObjectName('settings_title')
        settings_title.setText('Abstract Data Settings')
        settings_title.setStyleSheet('font-size: 18px; font-weight: bold;')
        settings_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        settings_title.hide()

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
        # ***********************
        # **** Plot Settings ****
        # ***********************
        plot_sttngs_gb = QGroupBox(overall_frame)
        plot_sttngs_gb.setObjectName('plot_sttngs_gb')
        plot_sttngs_gb.setTitle('Plot Settings')
        plot_sttngs_gb.setStyleSheet(f"""
            QGroupBox {{
                font-size: 16px;
                font-weight: bold;
                background: {self.themes['app_color']['green_two']};
                border: none;
                border-radius: 13px;
                margin-top: 23px;
                color: {self.themes['app_color']['dark_one']};
            }}
            QGroupBox:title {{
                subcontrol-origin: margin;
                left: 30px;
            }}
        """)

        plot_sttngs_content = QFrame(plot_sttngs_gb)
        plot_sttngs_content.setObjectName('plot_sttngs_content')
        plot_sttngs_content.setFrameShape(QFrame.Shape.NoFrame)
        plot_sttngs_content.setFrameShadow(QFrame.Shadow.Raised)
        plot_sttngs_content.setStyleSheet("QFrame#plot_sttngs_content {background: rgba(255, 255, 255, 175); border-radius: 10px;}")
        
        share_axis_option = QFrame(plot_sttngs_content)
        share_axis_option.setObjectName('share_axis_option')
        share_axis_option.setFrameShape(QFrame.Shape.NoFrame)
        share_axis_option.setFrameShadow(QFrame.Shadow.Raised)

        share_axis_label = QLabel(share_axis_option)
        share_axis_label.setObjectName('share_axis_label')
        share_axis_label.setText('Share X-Axis (Requires both plots):')
        share_axis_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        share_axis_label.setStyleSheet(f"color: {self.themes['app_color']['text_foreground_two']}; font-size: 13px;")

        self.share_axis_toggle = PyToggle(
            width=34,
            height=20,
            ellipse_y=2,
            bg_color = self.themes['app_color']['dark_two'],
            circle_color = self.themes['app_color']['white'],
            active_color = self.themes['app_color']['icon_active'],
            parent=share_axis_option
        )
        self.share_axis_toggle.setObjectName('share_axis_toggle')
        self.share_axis_toggle.setChecked(False)
        self.share_axis_toggle.setEnabled(False)

        share_axis_layout = QHBoxLayout(share_axis_option)
        share_axis_layout.setContentsMargins(0, 0, 0, 0)
        share_axis_layout.setSpacing(5)
        share_axis_layout.addWidget(share_axis_label, alignment=Qt.AlignmentFlag.AlignCenter)
        share_axis_layout.addWidget(self.share_axis_toggle, alignment=Qt.AlignmentFlag.AlignCenter)

        # TODO: Show time ranges on measurement plot

        plot_sttngs_layout = QGridLayout(plot_sttngs_content)
        plot_sttngs_layout.setContentsMargins(5, 5, 5, 5)
        plot_sttngs_layout.setSpacing(7)
        plot_sttngs_layout.addWidget(share_axis_option, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # TODO: Set a min/max for x-range

        # TODO: Add time range lines

        plot_gb_layout = QVBoxLayout(plot_sttngs_gb)
        plot_gb_layout.setContentsMargins(15, 15, 15, 15)
        plot_gb_layout.setSpacing(10)
        plot_gb_layout.addWidget(plot_sttngs_content)
        plot_sttngs_gb.setFixedHeight(plot_gb_layout.sizeHint().height() + 30)

        # ***********************************
        # **** Measurement Plot Settings ****
        # ***********************************
        self.measurement_collapsible_setting = SettingsGroupBox(
            title="  Measurement Plot",
            bg_color_two=self.themes["app_color"]["bg_one"],
            point_size=16,
            color=self.themes["app_color"]["dark_one"],
            parent=overall_frame
        )
        self.measurement_collapsible_setting.setObjectName("measurement_setting_menu")
        self.measurement_collapsible_setting.set_empty()

        msrmnt_setting_frame = QFrame(self.measurement_collapsible_setting)
        msrmnt_setting_frame.setObjectName("measurement_setting_frame")
        msrmnt_setting_frame.setFrameShape(QFrame.Shape.NoFrame)
        msrmnt_setting_frame.setFrameShadow(QFrame.Shadow.Plain)

        msrmnt_scroll_area = QScrollArea(msrmnt_setting_frame)
        msrmnt_scroll_area.setObjectName('msrmnt_scroll_area')
        msrmnt_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        msrmnt_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        msrmnt_scroll_area.setWidgetResizable(True)

        self.measurement_area = QFrame(msrmnt_scroll_area)
        self.measurement_area.setFrameShape(QFrame.Shape.NoFrame)
        self.measurement_area.setFrameShadow(QFrame.Shadow.Plain)
        self.measurement_area.setEnabled(False)

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

        self.msrmnt_area_layout = QGridLayout(self.measurement_area)
        self.msrmnt_area_layout.setContentsMargins(10, 10, 10, 10)
        self.msrmnt_area_layout.setSpacing(8)
        self.msrmnt_area_layout.setVerticalSpacing(40)
        self.msrmnt_area_layout.addWidget(self.msrmnt_var_ctrl_frame, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        msrmnt_toggle_home = QFrame(msrmnt_setting_frame)
        msrmnt_toggle_home.setObjectName("msrmnt_toggle_home")
        msrmnt_toggle_home.setFrameShape(QFrame.Shape.NoFrame)
        msrmnt_toggle_home.setFrameShadow(QFrame.Shadow.Plain)
        msrmnt_toggle_home.setStyleSheet(f'QFrame#msrmnt_toggle_home {{background: {self.themes["app_color"]["white"]}; border-top-left-radius: 8px; border-top-right-radius: 8px;}}')

        msrmnt_toggle_label = QLabel(msrmnt_toggle_home)
        msrmnt_toggle_label.setObjectName("msrmnt_toggle_label")
        msrmnt_toggle_label.setText("Use Measurement Plot:")
        msrmnt_toggle_label.setStyleSheet(f'font-size: 14px; color: {self.themes["app_color"]["context_pressed"]};')

        self.use_msrmnt_plot = PyToggle(
            width=28,
            height=16,
            ellipse_y=2,
            bg_color = self.themes["app_color"]["dark_two"],
            circle_color = self.themes["app_color"]["white"],
            active_color = self.themes["app_color"]["green_two"],
            parent=msrmnt_toggle_home
        )
        self.use_msrmnt_plot.setObjectName("use_msrmnt_plot")
        self.use_msrmnt_plot.setChecked(True)
        self.use_msrmnt_plot.setCursor(Qt.CursorShape.PointingHandCursor)

        msrmnt_toggle_layout = QHBoxLayout(msrmnt_toggle_home)
        msrmnt_toggle_layout.setContentsMargins(7, 7, 7, 7)
        msrmnt_toggle_layout.setSpacing(7)
        msrmnt_toggle_layout.addWidget(msrmnt_toggle_label)
        msrmnt_toggle_layout.addWidget(self.use_msrmnt_plot)
        msrmnt_toggle_layout.addStretch(1)

        overall_msrmnt_layout = QVBoxLayout(msrmnt_setting_frame)
        overall_msrmnt_layout.setContentsMargins(0, 0, 0, 0)
        overall_msrmnt_layout.setSpacing(15)
        overall_msrmnt_layout.addWidget(msrmnt_toggle_home)
        overall_msrmnt_layout.addWidget(msrmnt_scroll_area)

        self.measurement_collapsible_setting.set_content(msrmnt_setting_frame, additional_height=300)

        # ***********************************
        # **** Treatment Plot Settings ****
        # ***********************************
        self.treatment_collapsible_setting = SettingsGroupBox(
            title="  Treatment Plot",
            bg_color_two=self.themes["app_color"]["bg_one"],
            point_size=16,
            color=self.themes["app_color"]["dark_one"],
            parent=overall_frame
        )
        self.treatment_collapsible_setting.setObjectName("treatment_collapsible_setting")
        self.treatment_collapsible_setting.set_empty()

        trtmnt_setting_frame = QFrame(self.treatment_collapsible_setting)
        trtmnt_setting_frame.setObjectName("trtmnt_setting_frame")
        trtmnt_setting_frame.setFrameShape(QFrame.Shape.NoFrame)
        trtmnt_setting_frame.setFrameShadow(QFrame.Shadow.Plain)

        trtmnt_scroll_area = QScrollArea(trtmnt_setting_frame)
        trtmnt_scroll_area.setObjectName('trtmnt_scroll_area')
        trtmnt_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        trtmnt_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        trtmnt_scroll_area.setWidgetResizable(True)

        self.treatment_area = QFrame(trtmnt_scroll_area)
        self.treatment_area.setFrameShape(QFrame.Shape.NoFrame)
        self.treatment_area.setFrameShadow(QFrame.Shadow.Plain)
        self.treatment_area.setEnabled(False)

        trtmnt_scroll_area.setWidget(self.treatment_area)

        self.trtmnt_var_ctrl_frame = QFrame(self.measurement_area)
        self.trtmnt_var_ctrl_frame.setObjectName('trtmnt_var_ctrl_frame')
        self.trtmnt_var_ctrl_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.trtmnt_var_ctrl_frame.setFrameShadow(QFrame.Shadow.Plain)
        self.trtmnt_var_ctrl_frame.setStyleSheet(f'QFrame#trtmnt_var_ctrl_frame {{background: {self.themes["app_color"]["text_active"]}; border-radius: 8px;}}')

        self.trtmnt_add_bttn = PyPushButton(
            text="Add",
            radius=8,
            color=self.themes["app_color"]["dark_three"],
            bg_color=self.themes["app_color"]["green_two"],
            bg_color_hover=self.themes["app_color"]["green"],
            bg_color_pressed=self.themes["app_color"]["green"],
            font_size=14,
            parent=self.trtmnt_var_ctrl_frame
        )
        self.trtmnt_add_bttn.setFixedHeight(28)

        self.trtmnt_remove_bttn = PyPushButton(
            text="Remove",
            radius=8,
            color=self.themes["app_color"]["dark_three"],
            bg_color=self.themes["app_color"]["red"],
            bg_color_hover=self.themes["app_color"]["red_two"],
            bg_color_pressed=self.themes["app_color"]["red_two"],
            font_size=14,
            parent=self.trtmnt_var_ctrl_frame
        )
        self.trtmnt_remove_bttn.setFixedHeight(28)

        trtmnt_ctrl_layout = QVBoxLayout(self.trtmnt_var_ctrl_frame)
        trtmnt_ctrl_layout.setContentsMargins(5, 5, 5, 5)
        trtmnt_ctrl_layout.setSpacing(15)
        trtmnt_ctrl_layout.addWidget(self.trtmnt_add_bttn)
        trtmnt_ctrl_layout.addWidget(self.trtmnt_remove_bttn)

        self.trtmnt_area_layout = QGridLayout(self.treatment_area)
        self.trtmnt_area_layout.setContentsMargins(10, 10, 10, 10)
        self.trtmnt_area_layout.setSpacing(8)
        self.trtmnt_area_layout.setVerticalSpacing(40)
        self.trtmnt_area_layout.addWidget(self.trtmnt_var_ctrl_frame, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        trtmnt_toggle_home = QFrame(trtmnt_setting_frame)
        trtmnt_toggle_home.setObjectName("trtmnt_toggle_home")
        trtmnt_toggle_home.setFrameShape(QFrame.Shape.NoFrame)
        trtmnt_toggle_home.setFrameShadow(QFrame.Shadow.Plain)
        trtmnt_toggle_home.setStyleSheet(f'QFrame#trtmnt_toggle_home {{background: {self.themes["app_color"]["white"]}; border-top-left-radius: 8px; border-top-right-radius: 8px;}}')

        trtmnt_toggle_label = QLabel(trtmnt_toggle_home)
        trtmnt_toggle_label.setObjectName("trtmnt_toggle_label")
        trtmnt_toggle_label.setText("Use Treatment Plot:")
        trtmnt_toggle_label.setStyleSheet(f'font-size: 14px; color: {self.themes["app_color"]["context_pressed"]};')

        self.use_trtmnt_plot = PyToggle(
            width=28,
            height=16,
            ellipse_y=2,
            bg_color = self.themes["app_color"]["dark_two"],
            circle_color = self.themes["app_color"]["white"],
            active_color = self.themes["app_color"]["green_two"],
            parent=trtmnt_toggle_home
        )
        self.use_trtmnt_plot.setObjectName("use_trtmnt_plot")
        self.use_trtmnt_plot.setChecked(True)
        self.use_trtmnt_plot.setCursor(Qt.CursorShape.PointingHandCursor)

        trtmnt_toggle_layout = QHBoxLayout(trtmnt_toggle_home)
        trtmnt_toggle_layout.setContentsMargins(7, 7, 7, 7)
        trtmnt_toggle_layout.setSpacing(7)
        trtmnt_toggle_layout.addWidget(trtmnt_toggle_label)
        trtmnt_toggle_layout.addWidget(self.use_trtmnt_plot)
        trtmnt_toggle_layout.addStretch(1)
        
        overall_trtmnt_layout = QVBoxLayout(trtmnt_setting_frame)
        overall_trtmnt_layout.setContentsMargins(0, 0, 0, 0)
        overall_trtmnt_layout.setSpacing(15)
        overall_trtmnt_layout.addWidget(trtmnt_toggle_home)
        overall_trtmnt_layout.addWidget(trtmnt_scroll_area)

        self.treatment_collapsible_setting.set_content(trtmnt_setting_frame, additional_height=300)

        self.submit_data_bttn = PyPushButton(
            text="Submit",
            radius=8,
            font_size=17,
            color=self.themes["app_color"]["text_foreground_two"],
            bg_color=self.themes["app_color"]["green_two"],
            bg_color_hover=self.themes["app_color"]["green"],
            bg_color_pressed=self.themes["app_color"]["green"],
            parent=overall_frame
        )
        self.submit_data_bttn.setObjectName("submit_data_bttn")
        self.submit_data_bttn.setFixedSize(110, 41)

        overall_layout = QVBoxLayout(overall_frame)
        overall_layout.setSpacing(75)
        overall_layout.setContentsMargins(0, 0, 0, 0)
        overall_layout.addWidget(plot_sttngs_gb)
        overall_layout.addWidget(self.measurement_collapsible_setting)
        overall_layout.addWidget(self.treatment_collapsible_setting)
        overall_layout.addWidget(self.submit_data_bttn, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(overall_frame)

    def add_measurement_variable(self):
        # Disable the layout to reduce UI flickering when adding/removing widgets
        self.msrmnt_area_layout.setEnabled(False)

        if self.msrmnt_var_counter < self._file_settings["max_cols"]-1:
            new_y_var = QtAbstractFieldWidget(
                setting_name=f"Data Value {self.msrmnt_var_counter + 1}",
                field_list=self._file_settings["fields"],
                sheet_list=self._file_settings["sheets"],
                excel_obj=self._file_settings["excel_obj"],
                parent=self.measurement_area
            )
            new_y_var.setObjectName(f"y_var_{self.msrmnt_var_counter}")

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

        # TODO: Check object name for deletion, 

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

    def clear_measurement_area(self):
        if not self.msrmnt_y_list:
            return
        
        while len(self.msrmnt_y_list) > 0:
            last_var = self.msrmnt_y_list.pop()

            index = self.msrmnt_area_layout.indexOf(last_var)
            if index is not -1:
                item = self.msrmnt_area_layout.takeAt(index)
                w = item.widget()
                if w:
                    w.deleteLater()
            self.msrmnt_var_counter -= 1
        
        self.msrmnt_row_counter = 0
        self.msrmnt_col_counter = 0

        wid = self.msrmnt_area_layout.takeAt(0).widget()
        if wid.objectName() == "msrmnt_x_var":
            wid.setParent(None)
            wid.deleteLater()

        index_bttn = self.msrmnt_area_layout.indexOf(self.msrmnt_var_ctrl_frame)
        if index_bttn is not -1:
            self.msrmnt_area_layout.takeAt(index_bttn)

        self.msrmnt_area_layout.addWidget(
            self.msrmnt_var_ctrl_frame,
            self.msrmnt_row_counter,
            self.msrmnt_col_counter,
            1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )

    def add_treatment_variable(self):
        # Disable the layout to reduce UI flickering when adding/removing widgets
        self.trtmnt_area_layout.setEnabled(False)

        new_y_var = QtAbstractFieldWidget(
            setting_name=f"Data Value {self.trtmnt_var_counter + 1}",
            field_list=self._file_settings["fields"],
            sheet_list=self._file_settings["sheets"],
            excel_obj=self._file_settings["excel_obj"],
            is_treatment=True,
            parent=self.treatment_area
        )

        self.trtmnt_area_layout.addWidget(new_y_var, self.trtmnt_row_counter, self.trtmnt_col_counter, 1, 1)
        self.trtmnt_col_counter += 1
        self.trtmnt_y_list.append(new_y_var)
        self.trtmnt_var_counter += 1

        # Create new row
        if self.trtmnt_col_counter == MAX_COLS:
            self.trtmnt_row_counter += 1
            self.trtmnt_col_counter = 0

        self.trtmnt_area_layout.addWidget(
            self.trtmnt_var_ctrl_frame, 
            self.trtmnt_row_counter, 
            self.trtmnt_col_counter, 
            1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.trtmnt_area_layout.setEnabled(True)

    def remove_treatment_variable(self):
        if not self.trtmnt_y_list:
            return
        
        self.trtmnt_area_layout.setEnabled(False)

        last_var = self.trtmnt_y_list.pop()

        index = self.trtmnt_area_layout.indexOf(last_var)
        if index is not -1:
            item = self.trtmnt_area_layout.takeAt(index)
            w = item.widget()
            if w:
                w.deleteLater()

        if self.trtmnt_col_counter == 0:
            self.trtmnt_row_counter -= 1
            self.trtmnt_col_counter = 1
        else:
            self.trtmnt_col_counter = 0
        self.trtmnt_var_counter -= 1

        index_bttn = self.trtmnt_area_layout.indexOf(self.trtmnt_var_ctrl_frame)
        if index_bttn is not -1:
            self.trtmnt_area_layout.takeAt(index_bttn)

        self.trtmnt_area_layout.addWidget(
            self.trtmnt_var_ctrl_frame,
            self.trtmnt_row_counter,
            self.trtmnt_col_counter,
            1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.trtmnt_area_layout.setEnabled(True)

    def clear_treatment_area(self):
        if not self.trtmnt_y_list:
            return
        
        while len(self.trtmnt_y_list) > 0:
            last_var = self.trtmnt_y_list.pop()

            index = self.trtmnt_area_layout.indexOf(last_var)
            if index is not -1:
                item = self.trtmnt_area_layout.takeAt(index)
                w = item.widget()
                if w:
                    w.deleteLater()
            self.trtmnt_var_counter -= 1
        
        self.trtmnt_row_counter = 0
        self.trtmnt_col_counter = 0

        wid = self.trtmnt_area_layout.takeAt(1).widget()
        if wid.objectName() == "trtmnt_x_var_end":
            wid.setParent(None)
            wid.deleteLater()
        wid = self.trtmnt_area_layout.takeAt(0).widget()
        if wid.objectName() == "trtmnt_x_var_start":
            wid.setParent(None)
            wid.deleteLater()

        index_bttn = self.trtmnt_area_layout.indexOf(self.trtmnt_var_ctrl_frame)
        if index_bttn is not -1:
            self.trtmnt_area_layout.takeAt(index_bttn)

        self.trtmnt_area_layout.addWidget(
            self.trtmnt_var_ctrl_frame,
            self.trtmnt_row_counter,
            self.trtmnt_col_counter,
            1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )

    def check_toggles(self):
        pass

    def import_info(self, file_settings: dict):
        self._file_settings = file_settings
        self.measurement_area.setEnabled(True)
        self.treatment_area.setEnabled(True)

        # Reset areas to add dynamic settings
        self.clear_measurement_area()
        self.clear_treatment_area()

        # Instantiate measurement options with X-Variable
        msrmnt_x_var = QtAbstractFieldWidget(
            setting_name="X-Variable",
            field_list=self._file_settings["fields"],
            sheet_list=self._file_settings["sheets"],
            excel_obj=self._file_settings["excel_obj"],
            is_x_var=True,
            parent=self.measurement_area
        )
        msrmnt_x_var.setObjectName('msrmnt_x_var')
        self.msrmnt_area_layout.addWidget(msrmnt_x_var, 0, 0, 1, 1)
        self.msrmnt_area_layout.addWidget(
            self.msrmnt_var_ctrl_frame, 
            0, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.msrmnt_row_counter, self.msrmnt_col_counter = 0, 1

        # Instantiate treatments options with X-variable
        trtmnt_x_var_start = QtAbstractFieldWidget(
            setting_name="X-Var Start",
            field_list=self._file_settings["fields"],
            sheet_list=self._file_settings["sheets"],
            excel_obj=self._file_settings["excel_obj"],
            is_x_var=True,
            parent=self.treatment_area
        )
        trtmnt_x_var_start.setObjectName('trtmnt_x_var_start')
        trtmnt_x_var_end = QtAbstractFieldWidget(
            setting_name="X-Var End",
            field_list=self._file_settings["fields"],
            sheet_list=self._file_settings["sheets"],
            excel_obj=self._file_settings["excel_obj"],
            is_x_var=True,
            parent=self.treatment_area
        )
        trtmnt_x_var_end.setObjectName('trtmnt_x_var_end')

        self.trtmnt_area_layout.addWidget(trtmnt_x_var_start, 0, 0, 1, 1)
        self.trtmnt_area_layout.addWidget(trtmnt_x_var_end, 0, 1, 1, 1)
        self.trtmnt_row_counter, self.trtmnt_col_counter = 1, 0
        self.trtmnt_area_layout.addWidget(
            self.trtmnt_var_ctrl_frame, 
            self.trtmnt_row_counter, 
            self.trtmnt_col_counter, 
            1, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )

    def submit_widgets(self):
        msg_bttns = {
            "Ok": QMessageBox.ButtonRole.AcceptRole,
        }

        error_box = QtMessage(
            buttons=msg_bttns,
            color=self.themes["app_color"]["white"],
            bg_color_one=self.themes["app_color"]["dark_one"],
            bg_color_two=self.themes["app_color"]["bg_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        error_box.setIcon(QMessageBox.Icon.Warning)

        all_widgets = {
            "measurement_vars": {},
            "treatment_vars": {}
        }

        if self.use_msrmnt_plot.isChecked():
            if self.msrmnt_var_counter == 0:
                # Using measurement plot but no variables were defined/added
                error_box.setText('No Measurement Variables Added.')
                error_box.setDetailedText('No measurement data values were detected. There must be at least 1 data value added, other than the X-Variable, in order to plot.')
                error_box.exec()
                return
            else:
                # Gather measurement widget states
                # Ensure that at least one y-variable is enabled for plotting
                # Go through measurement widgets
                throw_error = True
                for index in range(self.msrmnt_area_layout.count()):
                    curr_widget = self.msrmnt_area_layout.itemAt(index).widget()
                    widget_name = curr_widget.objectName()
                    if widget_name != "msrmnt_var_ctrl_frame":
                        if widget_name == "msrmnt_x_var":
                            widget_state = curr_widget.get_x_values()
                        else:
                            # Expected y variable
                            widget_state = curr_widget.get_y_values()
                            if widget_state["plot_option"] and throw_error is True:
                                throw_error = False
                        all_widgets["measurement_vars"][widget_name] = widget_state
                if throw_error:
                    error_box.setText('No Measurement Variables Plotted.')
                    error_box.setDetailedText('No measurement variables are being plotted. At least one added variable must be toggled to plot.')
                    error_box.exec()
                    return

        if self.use_trtmnt_plot.isChecked():
            if self.trtmnt_var_counter == 0:
                # Using treatment plot but no variables were defined/added
                error_box.setText('No Treatment Variables Added.')
                error_box.setDetailedText('No treatment data values were detected. There must be at least 1 data value added, other than the X-Variable(s), in order to plot.')
                error_box.exec()
                return
            else:
                # Gather treatment widget states
                # Ensure that at least one x-variable is enabled for plotting
                throw_error = True
                for index in range(self.trtmnt_area_layout.count()):
                    curr_widget = self.trtmnt_area_layout.itemAt(index).widget()
                    widget_name = curr_widget.objectName()
                    if widget_name != "trtmnt_var_ctrl_frame":
                        if widget_name == "trtmnt_x_var_start" or widget_name == "trtmnt_x_var_end":
                            widget_state = curr_widget.get_x_values()
                        else:
                            widget_state = curr_widget.get_y_values()
                            if widget_state["plot_option"] and throw_error is True:
                                throw_error = False
                        all_widgets["treatment_vars"][widget_name] = widget_state
                if throw_error:
                    error_box.setText('No Treatment Variables Plotted.')
                    error_box.setDetailedText('No treatment variables are being plotted. At least one added variable must be toggled to plot')
                    error_box.exec()
                    return

        print(f'Gathered all states!')
        print(all_widgets)
        for key, value in all_widgets.items():
            print(f'\n{key}: \n\t{value}')