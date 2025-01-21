from functools import partial
from src.core.pyqt_core import *
from src.core.json.json_settings import Settings
from src.core.json.json_themes import Themes
from src.core.image_functions import Functions
from src.gui.models import *
from src.gui.views.windows.ui_main_window import UI_MainWindow
from src.gui.views.windows.functions_main_window import *

from datetime import datetime


class SetupMainWindow:
    def __init__(self) -> None:
        super().__init__()
        # SETUP MAIN WINDOW
        # Load widgets from "gui\uis\main_window\ui_main.py"
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

    # Setup Main Window with custom parameters
    def setup_gui(self):
        # App title
        self.setWindowTitle(self.settings["app_name"])

        # Remove title bar
        if self.settings["custom_title_bar"]:
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # ADD GRIPS
        if self.settings["custom_title_bar"]:
            self.left_grip = PyGrips(self, "left", self.hide_grips)
            self.right_grip = PyGrips(self, "right", self.hide_grips)
            self.top_grip = PyGrips(self, "top", self.hide_grips)
            self.bottom_grip = PyGrips(self, "bottom", self.hide_grips)
            self.top_left_grip = PyGrips(self, "top_left", self.hide_grips)
            self.top_right_grip = PyGrips(self, "top_right", self.hide_grips)
            self.bottom_left_grip = PyGrips(self, "bottom_left", self.hide_grips)
            self.bottom_right_grip = PyGrips(self, "bottom_right", self.hide_grips)

        # LEFT MENUS / GET SIGNALS WHEN LEFT MENU BTN IS CLICKED / RELEASED
        # ADD LEFT MENUS
        left_menu_bttns = [
        {
            "bttn_icon" : "icon_home.svg",
            "bttn_id" : "bttn_home",
            "bttn_text" : "Home",
            "bttn_tooltip" : "Home page",
            "show_top" : True,
            "is_active" : True
        },
        {
            "bttn_icon" : "etb_icon.svg",
            "bttn_id" : "etb_model_bttn",
            "bttn_text" : "Tumor Modeling",
            "bttn_tooltip" : "Modeling with GDRS tumor model",
            "show_top" : True,
            "is_active" : False
        },
        {
            "bttn_icon": "algorithm_icon.svg",
            "bttn_id": "enhanced_modeling_bttn",
            "bttn_text": "Enhanced Modeling",
            "bttn_tooltip": "New Multi-Model Page",
            "show_top": True,
            "is_active": False
        },
        {
            "bttn_icon" : "icon_add_user.svg",
            "bttn_id" : "rosetta_bttn",
            "bttn_text" : "Rosetta",
            "bttn_tooltip" : "Multi-Model framework",
            "show_top" : True,
            "is_active" : False
        },
        {
            "bttn_icon" : "icon_info.svg",
            "bttn_id" : "bttn_info",
            "bttn_text" : "Information",
            "bttn_tooltip" : "Open informations",
            "show_top" : False,
            "is_active" : False
        }
        ]

        # ADD MENUS
        self.ui.left_menu.add_menus(left_menu_bttns)

        # SET SIGNALS
        self.ui.left_menu.clicked.connect(self.menu_clicked)
        self.ui.left_menu.released.connect(self.menu_released)

        # TITLE BAR / ADD EXTRA BUTTONS
        # ADD TITLE BAR MENUS
        title_bar_bttns = [
            {
                "bttn_icon" : "icon_menu.svg",
                "bttn_id" : "bttn_sub_menu",
                "bttn_tooltip" : "Sub-Menu Options",
                "is_active" : False
            }
        ]

        # ADD MENUS
        self.ui.title_bar.add_menus(title_bar_bttns)

        # SET SIGNALS
        self.ui.title_bar.clicked.connect(self.menu_clicked)
        self.ui.title_bar.released.connect(self.menu_released)

        # ADD Title
        if self.settings["custom_title_bar"]:
            self.ui.title_bar.set_title(self.settings["app_name"])
        else:
            self.ui.title_bar.set_title("Testing hehe")   # ("Welcome to PyOneDark")

        # LEFT COLUMN SET SIGNALS
        self.ui.left_column.clicked.connect(self.menu_clicked)
        self.ui.left_column.released.connect(self.menu_released)

        # Right Column
#         self.ui.right_column.bt_1.clicked.connect(partial(self.page_picker, self.ui.load_pages.file_menu_container))
#         self.ui.right_column.bt_2.clicked.connect(partial(self.page_picker, self.ui.load_pages.parameter_menu_container))

        # SET INITIAL PAGE / SET LEFT AND RIGHT COLUMN MENUS
        MainFunctions.set_page(self, self.ui.load_pages.home_menu_container)
        MainFunctions.set_left_column_menu(
            self,
            menu = self.ui.left_column.menus.settings_menu,
            title = "Settings Left Column",
            icon_path = Functions.set_svg_icon("icon_settings.svg")
        )
        MainFunctions.set_right_column_menu(self, self.ui.right_column.menu_1)

        # OBJECTS FOR LOAD PAGES, LEFT AND RIGHT COLUMNS
        # You can access objects inside Qt Designer projects using
        # the objects below:
        #
        # <OBJECTS>
        # LEFT COLUMN: self.ui.left_column.menus
        # RIGHT COLUMN: self.ui.right_column
        # LOAD PAGES: self.ui.load_pages
        # </OBJECTS>

        # Load settings
        settings = Settings()
        self.settings = settings.items

        # Load Theme
        themes = Themes()
        self.themes = themes.items

        # Left Column
        # Widget goes here
        # Button 1 Test
        # self.left_btn_1 = PyPushButton(
        #     text="Btn 1",
        #     radius=8,
        #     color=self.themes["app_color"]["text_foreground"],
        #     bg_color=self.themes["app_color"]["dark_one"],
        #     bg_color_hover=self.themes["app_color"]["dark_three"],
        #     bg_color_pressed=self.themes["app_color"]["dark_four"]
        # )
        # self.left_btn_1.setMaximumHeight(40)
        # self.ui.left_column.menus.btn_1_layout.addWidget(self.left_btn_1)
        self.left_btn_1 = QPushButton(text="Push Me")
        self.left_btn_1.setMaximumHeight(40)
        self.ui.left_column.menus.btn_1_layout.addWidget(self.left_btn_1)

        #################################
        # * Right Column Menu Buttons * #
        #################################
        # * Basic Data Modeling Page Selection Button Creation * #
        self.input_file_menu_bttn = PyPushButton(
            text="Import Page",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            highlight=self.themes["app_color"]["green"],
            parent=self.ui.right_column.etb_bttn_frame
        )
        self.input_file_menu_bttn.setFixedHeight(38)
        self.input_file_menu_bttn.setObjectName("input_file_menu_bttn")
        self.input_file_menu_bttn.set_highlight()

        self.parameter_menu_bttn = PyPushButton(
            text="Parameter Page",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            highlight=self.themes["app_color"]["green"],
            parent=self.ui.right_column.etb_bttn_frame
        )
        self.parameter_menu_bttn.setFixedHeight(38)
        self.parameter_menu_bttn.setObjectName("parameter_menu_bttn")

        self.plot_menu_bttn = PyPushButton(
            text="Plot Page",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            highlight=self.themes["app_color"]["green"],
            parent=self.ui.right_column.etb_bttn_frame
        )
        self.plot_menu_bttn.setFixedHeight(38)
        self.plot_menu_bttn.setObjectName("plot_menu_bttn")

        self.ui.right_column.etb_bttn_layout.addWidget(self.input_file_menu_bttn)
        self.ui.right_column.etb_bttn_layout.addWidget(self.parameter_menu_bttn)
        self.ui.right_column.etb_bttn_layout.addWidget(self.plot_menu_bttn)

        self.input_file_menu_bttn.clicked.connect(partial(self.data_modeling_bookmark_event, self.ui.load_pages.etb_file_subpage))
        self.parameter_menu_bttn.clicked.connect(partial(self.data_modeling_bookmark_event, self.ui.load_pages.etb_settings_subpage))
        self.plot_menu_bttn.clicked.connect(partial(self.data_modeling_bookmark_event, self.ui.load_pages.etb_plot_subpage))
        
        # * Adaptive Modeling Page Selection Button Creation * #
        self.upload_menu_bttn = PyPushButton(
            text="Upload & Model Menu",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            highlight=self.themes["app_color"]["green"],
            parent=self.ui.right_column.enhanced_modeling_bttn_frame
        )
        self.upload_menu_bttn.setFixedHeight(38)
        self.upload_menu_bttn.setObjectName("upload_menu_bttn")
        self.upload_menu_bttn.set_highlight()

        self.model_settings_menu_bttn = PyPushButton(
            text="Settings Menu",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            highlight=self.themes["app_color"]["green"],
            parent=self.ui.right_column.enhanced_modeling_bttn_frame
        )
        self.model_settings_menu_bttn.setFixedHeight(38)
        self.model_settings_menu_bttn.setObjectName("model_settings_menu_bttn")

        self.results_menu_bttn = PyPushButton(
            text="Results Menu",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            highlight=self.themes["app_color"]["green"],
            parent=self.ui.right_column.enhanced_modeling_bttn_frame
        )
        self.results_menu_bttn.setFixedHeight(38)
        self.results_menu_bttn.setObjectName("results_menu_bttn")

        self.ui.right_column.enhanced_modeling_bttn_layout.addWidget(self.upload_menu_bttn)
        self.ui.right_column.enhanced_modeling_bttn_layout.addWidget(self.model_settings_menu_bttn)
        self.ui.right_column.enhanced_modeling_bttn_layout.addWidget(self.results_menu_bttn)

        self.upload_menu_bttn.clicked.connect(lambda: self.adaptive_modeling_bookmark_event(self.ui.load_pages.data_model_selection_page))
        self.model_settings_menu_bttn.clicked.connect(lambda: self.adaptive_modeling_bookmark_event(self.ui.load_pages.modeling_settings_page))
        self.results_menu_bttn.clicked.connect(lambda: self.adaptive_modeling_bookmark_event(self.ui.load_pages.enhanced_results_page))

        #########################################
        # Application Pages/Menu Initialization #
        #########################################
        # * Home Page Setup * #
        self.project_dir_entry = QtButtonLineEdit(
            title="Directory",
            title_color=self.themes["app_color"]["text_foreground"],
            top_margin=19,
            excel_mode=False,
            parent=self.ui.load_pages.directory_frame
        )
        self.project_dir_entry.setObjectName(u'proj_dir_entry')
        self.project_dir_entry.setMinimumWidth(350)

        self.submit_dir_bttn = PyPushButton(
            text="Submit",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            parent=self.ui.load_pages.directory_frame
        )
        self.submit_dir_bttn.setObjectName(u"dir_submit_bttn")
        self.submit_dir_bttn.setMinimumSize(85, 31)

        self.project_dir_label = QtMarqueeLabel(
            color=self.themes["app_color"]["text_foreground_two"],
            parent=self.ui.load_pages.project_dir_frame)
        self.project_dir_label.setMinimumWidth(275)
        self.project_dir_label.setText('None')

        self.submit_dir_bttn.clicked.connect(lambda: MainFunctions.test_run(
            self
        ))

        self.ui.load_pages.dir_entry_interaction.addWidget(self.project_dir_entry)
        self.ui.load_pages.bttn_holder.addWidget(self.submit_dir_bttn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.ui.load_pages.dir_entry_interaction.addLayout(self.ui.load_pages.bttn_holder)
        self.ui.load_pages.project_dir_layout.addWidget(self.project_dir_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.ui.load_pages.project_dir_layout.addStretch(1)
        self.ui.load_pages.project_dir_frame.setMaximumWidth(self.ui.load_pages.dir_entry_interaction.sizeHint().width())

        # * ETB File Page Setup * #
        etb_upload_widget = QtUploadMainWidget(parent=self.ui.load_pages.file_scroll_contents)

        self.nonsystemic_table = PyTableWidget(
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["context_color"],
            bg_color = self.themes["app_color"]["dark_one"],
            header_horizontal_color = self.themes["app_color"]["dark_two"],
            header_vertical_color = self.themes["app_color"]["bg_three"],
            bottom_line_color = self.themes["app_color"]["bg_three"],
            grid_line_color = self.themes["app_color"]["bg_one"],
            scroll_bar_bg_color = self.themes["app_color"]["bg_one"],
            scroll_bar_btn_color = self.themes["app_color"]["dark_four"],
            context_color = self.themes["app_color"]["context_color"]
        )
        self.nonsystemic_table.hide()

        #self.submit_file_bttn.clicked.connect(lambda: MainFunctions.inititate_file_check(self, self.etb_file_entry.text()))
        etb_upload_widget.submit_data_bttn.clicked.connect(lambda: MainFunctions.inititate_file_check(self, etb_upload_widget))

        self.ui.load_pages.file_content_layout.addWidget(etb_upload_widget)

        # * ETB Parameters Page Setup * #
        self.general_groupbox = GeneralSettings(
            header_color=self.themes["app_color"]["dark_four"],
            toggle_bg_color=self.themes["app_color"]["dark_two"],
            circle_color=self.themes["app_color"]["white"],    # icon_color
            active_color=self.themes["app_color"]["context_color"],
            parent=self.ui.load_pages.parameter_scroll_contents
        )
        self.general_groupbox.setObjectName(u"general_groupbox")
        self.general_groupbox.apply.connect(lambda: MainFunctions.load_etb_settings(self))

        self.lesion_groupbox = SettingsGroupBox(
            title="  Lesion Settings",
            color=self.themes["app_color"]["dark_one"],
            parent=self.ui.load_pages.parameter_scroll_contents
        )
        self.lesion_groupbox.setObjectName(u"lesion_groupbox")
        self.lesion_groupbox.set_empty()

        self.historical_groupbox = SettingsGroupBox(
            title="  Historical Treatments",
            color=self.themes["app_color"]["dark_one"],
            parent=self.ui.load_pages.parameter_scroll_contents
        )
        self.historical_groupbox.setObjectName(u"historical_groupbox")
        self.historical_groupbox.set_empty()

        self.available_tx_groupbox = SettingsGroupBox(
            title="  Available Treatments",
            color=self.themes["app_color"]["dark_one"],
            parent=self.ui.load_pages.parameter_scroll_contents
        )
        self.available_tx_groupbox.setObjectName(u"available_groupbox")
        self.available_tx_groupbox.set_empty()

        self.submit_parameters_bttn = PyPushButton(
            text="Submit",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            font_size=14,
            parent=self.ui.right_column.etb_bttn_frame
        )
        self.submit_parameters_bttn.setObjectName(u"submit_parameters_bttn")
        # self.submit_parameters_bttn.setMinimumHeight(40)
        # self.submit_parameters_bttn.setFixedWidth(185)
        self.submit_parameters_bttn.setMinimumSize(120, 40)
        self.submit_parameters_bttn.clicked.connect(self.start_table_window)

        submit_param_bttn_layout = QHBoxLayout()
        submit_param_bttn_layout.addStretch(1)
        submit_param_bttn_layout.addWidget(self.submit_parameters_bttn)
        submit_param_bttn_layout.addStretch(1)

        self.ui.load_pages.parameter_scroll_layout.addWidget(self.general_groupbox)
        self.ui.load_pages.parameter_scroll_layout.addWidget(self.lesion_groupbox)
        self.ui.load_pages.parameter_scroll_layout.addWidget(self.historical_groupbox)
        self.ui.load_pages.parameter_scroll_layout.addWidget(self.available_tx_groupbox)
        self.ui.load_pages.parameter_scroll_layout.addLayout(submit_param_bttn_layout)

        # * ETB Plot Page Setup * #
        log_frame = QFrame(self.ui.load_pages.etb_plot_subpage)
        log_frame.setObjectName('log_frame')
        log_frame.setFrameShape(QFrame.Shape.NoFrame)
        log_frame.setFrameShadow(QFrame.Shadow.Raised)
        log_frame.setStyleSheet('QFrame#log_frame{{background: {bg}; border-radius: 12px; border: none;}}'.format(bg=self.themes['app_color']['bg_two']))

        apply_log_label = QLabel(log_frame)
        apply_log_label.setObjectName('apply_log_label')
        apply_log_label.setText("Apply log10:")
        apply_log_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        apply_log_label.setStyleSheet("font-size: 12px;")

        self.scale_toggle = PyToggle(
            width=50,
            height=28,
            ellipse_y=3,
            bg_color = self.themes["app_color"]["dark_two"],
            circle_color = self.themes["app_color"]["white"],
            active_color = self.themes["app_color"]["green_two"],
            parent=log_frame
        )
        self.scale_toggle.setObjectName(u"scale_toggle")
        self.scale_toggle.setEnabled(False)
        self.scale_toggle.setChecked(False)

        log_layout = QHBoxLayout(log_frame)
        log_layout.setObjectName('log_layout')
        log_layout.setContentsMargins(7, 11, 15, 11)
        log_layout.setSpacing(5)
        log_layout.addWidget(apply_log_label)
        log_layout.addWidget(self.scale_toggle)
        log_frame.setMinimumWidth(log_layout.sizeHint().width())
        log_frame.setMaximumWidth(int(log_layout.sizeHint().width() * 1.4))

        toggle_stack_container = QFrame(self.ui.load_pages.etb_plot_subpage)
        toggle_stack_container.setObjectName('toggle_stack_container')
        toggle_stack_container.setFrameShape(QFrame.Shape.NoFrame)
        toggle_stack_container.setFrameShadow(QFrame.Shadow.Raised)

        extend_log_frame = QFrame(toggle_stack_container)
        extend_log_frame.setObjectName('extend_log_frame')
        extend_log_frame.setFrameShape(QFrame.Shape.NoFrame)
        extend_log_frame.setFrameShadow(QFrame.Shadow.Raised)
        extend_log_frame.setStyleSheet('QFrame#extend_log_frame{{background: {bg}; border-radius: 12px; border: none;}}'.format(bg=self.themes['app_color']['bg_two']))

        extend_log_label = QLabel(extend_log_frame)
        extend_log_label.setObjectName('extend_log_label')
        extend_log_label.setText('Extend Tx Bar:')
        extend_log_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        extend_log_label.setStyleSheet('font-size: 12px;')

        self.extend_log_toggle = PyToggle(
            width=50,
            height=28,
            ellipse_y=3,
            bg_color = self.themes["app_color"]["dark_two"],
            circle_color = self.themes["app_color"]["white"],
            active_color = self.themes["app_color"]["green_two"],
            parent=extend_log_frame
        )
        self.extend_log_toggle.setObjectName('extend_log_toggle')
        self.extend_log_toggle.setEnabled(False)
        self.extend_log_toggle.setChecked(False)

        extend_log_layout = QHBoxLayout(extend_log_frame)
        extend_log_layout.setObjectName('extend_log_layout')
        extend_log_layout.setContentsMargins(7, 11, 15, 11)
        extend_log_layout.setSpacing(5)
        extend_log_layout.addWidget(extend_log_label)
        extend_log_layout.addWidget(self.extend_log_toggle)
        extend_log_frame.setMinimumSize(extend_log_layout.sizeHint().width(), 50)
        extend_log_frame.setMaximumSize(int(extend_log_layout.sizeHint().width() * 1.4), 50)

        extend_norm_frame = QFrame(toggle_stack_container)
        extend_norm_frame.setObjectName('extend_norm_frame')
        extend_norm_frame.setFrameShape(QFrame.Shape.NoFrame)
        extend_norm_frame.setFrameShadow(QFrame.Shadow.Raised)
        extend_norm_frame.setStyleSheet('QFrame#extend_norm_frame{{background: {bg}; border-radius: 12px; border: none;}}'.format(bg=self.themes['app_color']['bg_two']))

        extend_norm_label = QLabel(extend_norm_frame)
        extend_norm_label.setObjectName('extend_norm_label')
        extend_norm_label.setText('Extend Tx Bar:')
        extend_norm_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        extend_norm_label.setStyleSheet('font-size: 12px;')

        self.extend_norm_toggle = PyToggle(
            width=50,
            height=28,
            ellipse_y=3,
            bg_color = self.themes["app_color"]["dark_two"],
            circle_color = self.themes["app_color"]["white"],
            active_color = self.themes["app_color"]["green_two"],
            parent=extend_norm_frame
        )
        self.extend_norm_toggle.setObjectName('extend_norm_toggle')
        self.extend_norm_toggle.setEnabled(False)
        self.extend_norm_toggle.setChecked(False)

        extend_norm_layout = QHBoxLayout(extend_norm_frame)
        extend_norm_layout.setObjectName('extend_norm_layout')
        extend_norm_layout.setContentsMargins(7, 11, 15, 11)
        extend_norm_layout.setSpacing(5)
        extend_norm_layout.addWidget(extend_norm_label)
        extend_norm_layout.addWidget(self.extend_norm_toggle)
        extend_norm_frame.setMinimumSize(extend_norm_layout.sizeHint().width(), 50)
        extend_norm_frame.setMaximumSize(int(extend_norm_layout.sizeHint().width() * 1.4), 50)

        self.extend_toggle_stack = QStackedLayout(toggle_stack_container)
        self.extend_toggle_stack.setObjectName('extend_toggle_stack')
        self.extend_toggle_stack.setContentsMargins(0, 0, 0, 0)
        self.extend_toggle_stack.addWidget(extend_norm_frame)
        self.extend_toggle_stack.addWidget(extend_log_frame)
        self.extend_toggle_stack.setCurrentWidget(extend_log_frame)
        toggle_stack_container.setMinimumSize(extend_log_frame.minimumSize())
        toggle_stack_container.setMaximumSize(extend_log_frame.maximumSize())

        self.save_settings_bttn = PyPushButton(
            text="Save Settings",
            radius=8,
            color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            font_size=13,
            parent=self.ui.load_pages.etb_plot_subpage
        )
        self.save_settings_bttn.setObjectName(u"save_settings_bttn")
        self.save_settings_bttn.setFixedSize(150, 50)

        self.scale_toggle.stateChanged.connect(lambda state: MainFunctions.toggle_plots(self, state, self.extend_toggle_stack))
        self.save_settings_bttn.clicked.connect(lambda: MainFunctions.save_etb_settings(self))

        scale_layout = QGridLayout()
        scale_layout.setContentsMargins(0, 0, 0, 0)
        # scale_layout.setSpacing(25)
        scale_layout.addWidget(log_frame, 0, 0, 1, 1)
        scale_layout.addWidget(toggle_stack_container, 0, 1, 1, 1)
        scale_layout.addWidget(self.save_settings_bttn, 0, 3, 1, 1)

        self.ui.load_pages.plot_menu_center_layout.addLayout(scale_layout)

        # * Enhanced Modeling Upload Page * #
        self.enhanced_upload = QtEnhancedModelingMenu()
        self.ui.load_pages.data_model_scroll_layout.addWidget(self.enhanced_upload)

        # * Enhanced Modeling Settings Page * #
        settings_label = QLabel(parent=self.ui.load_pages.modeling_content_frame)
        settings_label.setText("Enhanced Settings Go Here.")
        settings_label.setStyleSheet("color: black; font-size:13px;")
        self.ui.load_pages.modeling_frame_layout.addWidget(settings_label)

        # * Enhanced Modeling Results Page * #
        results_label = QLabel(parent=self.ui.load_pages.results_content_frame)
        results_label.setText("Enhanced Results Go Here.")
        results_label.setStyleSheet("color: black; font-size:13px;")
        self.ui.load_pages.results_content_layout.addWidget(results_label)

        # PAGE 2
        # CIRCULAR PROGRESS 1
        # self.circular_progress_1 = PyCircularProgress(
        #     value = 80,
        #     progress_color = self.themes["app_color"]["context_color"],
        #     text_color = self.themes["app_color"]["text_title"],
        #     font_size = 14,
        #     bg_color = self.themes["app_color"]["dark_four"]
        # )
        # self.circular_progress_1.setFixedSize(200,200)

    # RESIZE GRIPS AND CHANGE POSITION
    # Resize or change position when window is resized
    def resize_grips(self):
        if self.settings["custom_title_bar"]:
            self.left_grip.setGeometry(5, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 15, 10, 10, self.height())
            self.top_grip.setGeometry(5, 5, self.width() - 10, 10)
            self.bottom_grip.setGeometry(5, self.height() - 15, self.width() - 10, 10)
            self.top_right_grip.setGeometry(self.width() - 20, 5, 15, 15)
            self.bottom_left_grip.setGeometry(5, self.height() - 20, 15, 15)
            self.bottom_right_grip.setGeometry(self.width() - 20, self.height() - 20, 15, 15)
