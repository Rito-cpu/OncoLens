from src.core.pyqt_core import *
from src.core.json.json_settings import Settings
from src.core.json.json_themes import Themes
from src.gui.views.windows.ui_main_window import *
from src.gui.views.windows.setup_main_window import *
from src.gui.models import *


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        settings = Settings()
        self.settings = settings.items

        self.hide_grips = True
        SetupMainWindow.setup_gui(self)

        self.reuse_bool = False
        self.reuse_matrix = {
            True: None,
            False: None
        }
        self.table_window = None
        self._connection_log = None
        self._connection_norm = None

        self.data_modeling_page_bookmark = None
        self.adaptive_modeling_page_bookmark = None

        themes = Themes()
        self.themes = themes.items

        self.show()

    # LEFT MENU BTN IS CLICKED
    # Check funtion by object name / btn_id
    def menu_clicked(self, menu_bttn):
        # GET BTTN CLICKED

        # Remove Selection If Clicked By "btn_close_left_column"
        if menu_bttn.objectName() != "bttn_settings":
            self.ui.left_menu.deselect_all_tab()

        # Get Title Bar Btn And Reset Active
        top_settings = MainFunctions.get_title_bar_btn(self, "bttn_sub_menu")
        top_settings.set_active(False)

        # LEFT MENU
        # HOME BTN
        if menu_bttn.objectName() == "bttn_home":
            # Close right panel and disable it, nothing to show
            if MainFunctions.right_column_is_visible(self):
                menu_bttn.set_active(False)
                MainFunctions.toggle_right_column(self)
            top_settings.setDisabled(True)
            # Select Menu
            self.ui.left_menu.select_only_one(menu_bttn.objectName())

            # Load Page 1
            MainFunctions.set_page(self, self.ui.load_pages.home_menu_container)
            # MainFunctions.set_right_column_menu(self, self.ui.right_column.menu_1)

        # Original Modeling Main Bttn
        if menu_bttn.objectName() == "etb_model_bttn":
            # Select Menu
            self.ui.left_menu.select_only_one(menu_bttn.objectName())
            top_settings.setEnabled(True)

            # Load Page 2
            if self.data_modeling_page_bookmark == None:
                MainFunctions.set_page(self, self.ui.load_pages.etb_file_subpage)
            else:
                MainFunctions.set_page(self, self.data_modeling_page_bookmark)
            MainFunctions.set_right_column_menu(self, self.ui.right_column.etb_menu_page)

        # Enhanced Modeling Main Bttn
        if menu_bttn.objectName() == "enhanced_modeling_bttn":
            # Select Menu
            self.ui.left_menu.select_only_one(menu_bttn.objectName())
            top_settings.setEnabled(True)

            # Load Enhanced Modeling Scene
            if self.adaptive_modeling_page_bookmark == None:
                MainFunctions.set_page(self, self.ui.load_pages.data_model_selection_page)
            else:
                MainFunctions.set_page(self, self.adaptive_modeling_page_bookmark)
            MainFunctions.set_right_column_menu(self, self.ui.right_column.enhanced_modeling_submenu)

        # Rosetta Main Bttn
        if menu_bttn.objectName() == "rosetta_bttn":
            # Select Menu
            self.ui.left_menu.select_only_one(menu_bttn.objectName())
            top_settings.setEnabled(True)

            # Load Page 3
            MainFunctions.set_page(self, self.ui.load_pages.rosetta_model_page)
            MainFunctions.set_right_column_menu(self, self.ui.right_column.menu_2)

        # BOTTOM INFORMATION
        if menu_bttn.objectName() == "bttn_info":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                self.ui.left_menu.select_only_one_tab(menu_bttn.objectName())

                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(menu_bttn.objectName())
            else:
                if menu_bttn.objectName() == "bttn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)

                self.ui.left_menu.select_only_one_tab(menu_bttn.objectName())

            # Change Left Column Menu
            if menu_bttn.objectName() != "bttn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self,
                    menu = self.ui.left_column.menus.info_menu,
                    title = "Info tab",
                    icon_path = Functions.set_svg_icon("icon_info.svg")
                )

        # SETTINGS LEFT
        if menu_bttn.objectName() == "bttn_settings" or menu_bttn.objectName() == "bttn_close_left_column":
            # CHECK IF LEFT COLUMN IS VISIBLE
            if not MainFunctions.left_column_is_visible(self):
                # Show / Hide
                MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(menu_bttn.objectName())
            else:
                if menu_bttn.objectName() == "bttn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    # Show / Hide
                    MainFunctions.toggle_left_column(self)
                self.ui.left_menu.select_only_one_tab(menu_bttn.objectName())

            # Change Left Column Menu
            if menu_bttn.objectName() != "bttn_close_left_column":
                MainFunctions.set_left_column_menu(
                    self,
                    menu = self.ui.left_column.menus.settings_menu,
                    title = "Settings Left Column",
                    icon_path = Functions.set_svg_icon("icon_settings.svg")
                )

        # TITLE BAR MENU
        # SETTINGS TITLE BAR
        if menu_bttn.objectName() == "bttn_sub_menu":
            # Toogle Active
            if not MainFunctions.right_column_is_visible(self):
                menu_bttn.set_active(True)

                # Show / Hide
                MainFunctions.toggle_right_column(self)
            else:
                menu_bttn.set_active(False)

                # Show / Hide
                MainFunctions.toggle_right_column(self)

            # Get Left Menu Btn
            # top_settings = MainFunctions.get_left_menu_btn(self, "bttn_settings")
            # top_settings.set_active_tab(False)

    # LEFT MENU BTN IS RELEASED
    # Run function when menu_bttn is released
    # Check funtion by object name / btn_id
    def menu_released(self, menu_bttn):
        pass
        # GET BT CLICKED
        # menu_bttn = SetupMainWindow.setup_btns(self)

        # DEBUG
        # print(f"Button {menu_bttn.objectName()}, released!")

    def data_modeling_bookmark_event(self, page):
        MainFunctions.set_page(self, page)

        upload_bttn = self.ui.right_column.etb_bttn_frame.findChild(PyPushButton, "input_file_menu_bttn")
        settings_bttn = self.ui.right_column.etb_bttn_frame.findChild(PyPushButton, "parameter_menu_bttn")
        plot_page = self.ui.right_column.etb_bttn_frame.findChild(PyPushButton, "plot_menu_bttn")

        if page == self.ui.load_pages.etb_file_subpage:
            upload_bttn.set_highlight()
            settings_bttn.remove_highlight()
            plot_page.remove_highlight()
        elif page == self.ui.load_pages.etb_settings_subpage:
            upload_bttn.remove_highlight()
            settings_bttn.set_highlight()
            plot_page.remove_highlight()
        else:
            upload_bttn.remove_highlight()
            settings_bttn.remove_highlight()
            plot_page.set_highlight()

        self.data_modeling_page_bookmark = page

    def adaptive_modeling_bookmark_event(self, page):
        MainFunctions.set_page(self, page)

        upload_bttn = self.ui.right_column.enhanced_modeling_bttn_frame.findChild(PyPushButton, 'upload_menu_bttn')
        settings_bttn = self.ui.right_column.enhanced_modeling_bttn_frame.findChild(PyPushButton, 'model_settings_menu_bttn')
        results_bttn = self.ui.right_column.enhanced_modeling_bttn_frame.findChild(PyPushButton, 'results_menu_bttn')
        if page == self.ui.load_pages.data_model_selection_page:
            upload_bttn.set_highlight()
            settings_bttn.remove_highlight()
            results_bttn.remove_highlight()
        elif page == self.ui.load_pages.modeling_settings_page:
            upload_bttn.remove_highlight()
            settings_bttn.set_highlight()
            results_bttn.remove_highlight()
        else:
            upload_bttn.remove_highlight()
            settings_bttn.remove_highlight()
            results_bttn.set_highlight()

        self.adaptive_modeling_page_bookmark = page

    # RESIZE EVENT
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # MOUSE CLICK EVENTS
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPosition().toPoint()

    def start_table_window(self):
        general_groupbox = self.ui.load_pages.parameter_scroll_contents.findChild(QWidget, "general_groupbox")

        error_message = QtMessage(
            buttons={"Ok": QMessageBox.ButtonRole.AcceptRole},
            color=self.themes["app_color"]["white"],
            bg_color_one=self.themes["app_color"]["dark_one"],
            bg_color_two=self.themes["app_color"]["bg_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"]
        )
        error_message.setIcon(QMessageBox.Icon.Warning)

        if general_groupbox.get_patient_file() != None:
            settings_data = MainFunctions.package_parameters(self)
            if settings_data == None:
                return
            lesion_data = settings_data[1]
            historical_treatments = settings_data[2]

            nonsystemic_table = PyTableWidget(
                radius = 8,
                color = self.themes["app_color"]["dark_one"],
                selection_color = self.themes["app_color"]["context_color"],
                bg_color = self.themes["app_color"]["dark_one"],
                header_horizontal_color = self.themes["app_color"]["bg_two"],
                header_vertical_color = self.themes["app_color"]["bg_two"],
                bottom_line_color = self.themes["app_color"]["bg_three"],
                grid_line_color = self.themes["app_color"]["bg_one"],
                scroll_bar_bg_color = self.themes["app_color"]["bg_one"],
                scroll_bar_btn_color = self.themes["app_color"]["dark_four"],
                context_color = self.themes["app_color"]["context_color"]
            )

            table_menu = NonSystemicSettings(
                lesion_data["abbr"],
                historical_treatments["abbr"],
                historical_treatments["date_on"],
                nonsystemic_table,
                reuseable_data=self.reuse_matrix[self.reuse_bool]
            )

            self.table_window = FramelessWindow(
                radius=8,
                color=self.themes["app_color"]["white"],
                bg_color=self.themes["app_color"]["dark_one"],
                bg_color_two=self.themes["app_color"]["bg_one"],
                bg_color_hover=self.themes["app_color"]["dark_three"],
                bg_color_pressed=self.themes["app_color"]["dark_four"],
                circle_color=self.themes["app_color"]["white"],
                active_color=self.themes["app_color"]["green_two"],
                main_bg_color=self.themes["app_color"]["bg_two"],
                widget=table_menu,
                data=settings_data,
                parent=self
            )
            self.table_window.reuse.connect(self.update_table_settings)
            self.table_window.finished.connect(self.setup_plots)
        else:
            error_message.setText("No patient file selected.")
            error_message.exec()

    def update_table_settings(self, data):
        matrix, self.reuse_bool = data
        self.reuse_matrix[True] = matrix

    def setup_plots(self, modeling_dict):
        self.table_window = None

        # *** If bar extensions are enabled, clear then and reset toggle ***
        extend_log_toggle: PyToggle
        extend_norm_toggle: PyToggle
        extend_log_toggle = self.ui.load_pages.etb_plot_subpage.findChild(QWidget, 'extend_log_toggle')
        extend_norm_toggle = self.ui.load_pages.etb_plot_subpage.findChild(QWidget, 'extend_norm_toggle')
        if not extend_log_toggle.isEnabled() and not extend_norm_toggle.isEnabled():
            extend_log_toggle.setEnabled(True)
            extend_norm_toggle.setEnabled(True)
        # ** Reset connections so we can reset widget to new default state ***
        if self._connection_log:
            extend_log_toggle.stateChanged.disconnect(self._connection_log)
            self._connection_log = None
            # *** If toggle widget was left on, turn off and remove bars ***
            if extend_log_toggle.isChecked():
                extend_log_toggle.setChecked(False)
                MainFunctions.remove_treatment_bars(self, self.ui.load_pages.plot_stack_menu.widget(1))
        if self._connection_norm:
            extend_norm_toggle.stateChanged.disconnect(self._connection_norm)
            self._connection_norm = None
            if extend_norm_toggle.isChecked():
                extend_norm_toggle.setChecked(False)
                MainFunctions.remove_treatment_bars(self, self.ui.load_pages.plot_stack_menu.widget(0))

        # *** Clear plot stack ***
        if self.ui.load_pages.plot_stack_menu.count() != 0:
            while self.ui.load_pages.plot_stack_menu.count() > 0:
                widget = self.ui.load_pages.plot_stack_menu.widget(0)
                self.ui.load_pages.plot_stack_menu.removeWidget(widget)
                widget.deleteLater()

        normal_fig, normal_ax = modeling_dict['normal_plot']
        log_fig, log_ax = modeling_dict['log_plot']
        merged_treatments = modeling_dict['bar_data']

        normal_canvas = QtPlotMenu(fig=normal_fig, ax=normal_ax, parent=self.ui.load_pages.plot_stack_menu)
        normal_canvas.setObjectName('normal_canvas')
        log_canvas = QtPlotMenu(fig=log_fig, ax=log_ax, parent=self.ui.load_pages.plot_stack_menu)
        log_canvas.setObjectName('log_canvas')

        scale_toggle: PyToggle
        scale_toggle = self.ui.load_pages.etb_plot_subpage.findChild(QWidget, "scale_toggle")
        if not scale_toggle.isEnabled():
            scale_toggle.setEnabled(True)
        scale_toggle.setChecked(True)

        if self._connection_log is None:
            self._connection_log = extend_log_toggle.stateChanged.connect(lambda state: MainFunctions.toggle_treatment_bar(self, state, merged_treatments))
        if self._connection_norm is None:
            self._connection_norm = extend_norm_toggle.stateChanged.connect(lambda state: MainFunctions.toggle_treatment_bar(self, state, merged_treatments))

        self.ui.load_pages.plot_stack_menu.addWidget(normal_canvas)
        self.ui.load_pages.plot_stack_menu.addWidget(log_canvas)
        self.ui.load_pages.plot_stack_menu.setCurrentWidget(log_canvas)

        self.data_modeling_bookmark_event(self.ui.load_pages.etb_plot_subpage)

    def closeEvent(self, event) -> None:
        exit_buttons = {
            "Yes": QMessageBox.ButtonRole.YesRole,
            "No": QMessageBox.ButtonRole.NoRole
        }

        exit_message = QtMessage(buttons=exit_buttons,
                        color=self.themes["app_color"]["white"],
                        bg_color_one=self.themes["app_color"]["dark_one"],
                        bg_color_two=self.themes["app_color"]["bg_one"],
                        bg_color_hover=self.themes["app_color"]["dark_three"],
                        bg_color_pressed=self.themes["app_color"]["dark_four"])
        exit_message.setIcon(QMessageBox.Icon.Warning)
        exit_message.setText("Are you sure you want to exit?")
        exit_message.setInformativeText("Any unsaved work will be lost.")
        exit_message.exec()

        if exit_message.clickedButton() == exit_message.buttons["Yes"]:
            if self.table_window: self.table_window.deleteLater()
            QApplication.instance().closeAllWindows()
            event.accept()
        else:
            event.ignore()
