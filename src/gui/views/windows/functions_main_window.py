import os
import json
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from datetime import datetime
from src.core.pyqt_core import *
from src.core.keyword_store import COMPARISON_CONE
from src.core.app_config import working_directory
from src.core.json.json_themes import Themes
from src.core.json.json_encoder import NumpyArrayEncoder
from src.core.validation.validate_file import is_json_file, is_excel_file
from src.core.validation.excel_utils import initiate_excel_check
from src.core.validation.data_validation import preprocess_data
from src.gui.views.windows.ui_main_window import UI_MainWindow
from src.gui.models import *
from src.core.processing.mysql_connector import MySQLConnector


class MainFunctions():
    def __init__(self) -> None:
        super().__init__()
        # Setup Main Window
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        themes = Themes
        self.themes = themes.items

    # SET MAIN WINDOW PAGES
    def set_page(self, page):
        self.ui.load_pages.pages.setCurrentWidget(page)

    # SET LEFT COLUMN PAGES
    def set_left_column_menu(
        self,
        menu,
        title,
        icon_path
    ):
        self.ui.left_column.menus.menus.setCurrentWidget(menu)
        self.ui.left_column.title_label.setText(title)
        self.ui.left_column.icon.set_icon(icon_path)

    # RETURN IF LEFT COLUMN IS VISIBLE
    def left_column_is_visible(self):
        width = self.ui.left_column_frame.width()
        if width == 0:
            return False
        else:
            return True

    # RETURN IF RIGHT COLUMN IS VISIBLE
    def right_column_is_visible(self):
        width = self.ui.right_column_frame.width()
        if width == 0:
            return False
        else:
            return True

    # SET RIGHT COLUMN PAGES
    def set_right_column_menu(self, menu):
        self.ui.right_column.menus.setCurrentWidget(menu)

    # GET TITLE BUTTON BY OBJECT NAME
    def get_title_bar_btn(self, object_name):
        return self.ui.title_bar_frame.findChild(QPushButton, object_name)

    # GET TITLE BUTTON BY OBJECT NAME
    def get_left_menu_btn(self, object_name):
        return self.ui.left_menu.findChild(QPushButton, object_name)

    # LEFT AND RIGHT COLUMNS / SHOW / HIDE
    def toggle_left_column(self):
        # GET ACTUAL CLUMNS SIZE
        width = self.ui.left_column_frame.width()
        right_column_width = self.ui.right_column_frame.width()

        MainFunctions.start_box_animation(self, width, right_column_width, "left")

    def toggle_right_column(self):
        # GET ACTUAL CLUMNS SIZE
        left_column_width = self.ui.left_column_frame.width()
        width = self.ui.right_column_frame.width()

        MainFunctions.start_box_animation(self, left_column_width, width, "right")

    def toggle_plots(self, state, toggle_stack: QStackedLayout):
        if state == 2: # Checked
            self.ui.load_pages.plot_stack_menu.setCurrentIndex(1)
            toggle_stack.setCurrentIndex(1)
        else:
            self.ui.load_pages.plot_stack_menu.setCurrentIndex(0)
            toggle_stack.setCurrentIndex(0)

    def toggle_treatment_bar(self, state, treatments):
        # Get the current active canvas from the plot stack menu
        current_canvas = self.ui.load_pages.plot_stack_menu.currentWidget()

        if state == 2:
            # Add treatment bars to the current canvas
            MainFunctions.add_treatment_bars(self, current_canvas, treatments)
        else:
            # Remove treatment bars from the current canvas
            if current_canvas:
                MainFunctions.remove_treatment_bars(self, current_canvas)

    def add_treatment_bars(self, canvas, treatments):
        # Iterate over treatments and add vertical bars to the canvas
        ax = canvas.get_axes()

        canvas.treatment_bars = []
        for start, end in treatments:
            bar = ax[0].axvspan(start, end, alpha=0.3, color='lightgray', hatch='///')
            canvas.treatment_bars.append(bar)

        canvas.draw()

    def remove_treatment_bars(self, canvas):
        # Remove all vertical bars from the canvas
        treatment_bars = getattr(canvas, 'treatment_bars', [])

        if len(treatment_bars) != 0:
            for bar in treatment_bars:
                bar.remove()

            canvas.draw()

    def start_box_animation(self, left_box_width, right_box_width, direction):
        right_width = 0
        left_width = 0
        time_animation = self.ui.settings["time_animation"]
        minimum_left = self.ui.settings["left_column_size"]["minimum"]
        maximum_left = self.ui.settings["left_column_size"]["maximum"]
        minimum_right = self.ui.settings["right_column_size"]["minimum"]
        maximum_right = self.ui.settings["right_column_size"]["maximum"]

        # Check Left Values
        if left_box_width == minimum_left and direction == "left":
            left_width = maximum_left
        else:
            left_width = minimum_left

        # Check Right values
        if right_box_width == minimum_right and direction == "right":
            right_width = maximum_right
        else:
            right_width = minimum_right

        # ANIMATION LEFT BOX
        self.left_box = QPropertyAnimation(self.ui.left_column_frame, b"minimumWidth")
        self.left_box.setDuration(time_animation)
        self.left_box.setStartValue(left_box_width)
        self.left_box.setEndValue(left_width)
        self.left_box.setEasingCurve(QEasingCurve.Type.InOutQuart)

        # ANIMATION RIGHT BOX
        self.right_box = QPropertyAnimation(self.ui.right_column_frame, b"minimumWidth")
        self.right_box.setDuration(time_animation)
        self.right_box.setStartValue(right_box_width)
        self.right_box.setEndValue(right_width)
        self.right_box.setEasingCurve(QEasingCurve.Type.InOutQuart)

        # GROUP ANIMATION
        self.group = QParallelAnimationGroup()
        self.group.stop()
        self.group.addAnimation(self.left_box)
        self.group.addAnimation(self.right_box)
        self.group.start()

    def check_project_directory(self, directory: str, label: QtMarqueeLabel):
        if os.path.isdir(directory):
            global working_directory
            working_directory = directory

            label.setText(directory)

    def inititate_file_check(self, upload_widget):
        data_path = upload_widget.submit_menu_data()
        if data_path:
            try:
                # TODO: Check for excel file using utility file in core
                file_data = preprocess_data(data_path)

                # Collapse boxes here to prevent any resizing issues when applying new content
                lesion_groupbox: SettingsGroupBox
                lesion_groupbox = self.ui.load_pages.parameter_scroll_contents.findChild(QWidget, "lesion_groupbox")
                historical_groupbox: SettingsGroupBox
                historical_groupbox = self.ui.load_pages.parameter_scroll_contents.findChild(QWidget, "historical_groupbox")
                available_groupbox: SettingsGroupBox
                available_groupbox = self.ui.load_pages.parameter_scroll_contents.findChild(QWidget, "available_groupbox")

                if lesion_groupbox.is_expanded():
                    lesion_groupbox.collapse_widget()
                if historical_groupbox.is_expanded():
                    historical_groupbox.collapse_widget()
                if available_groupbox.is_expanded():
                    available_groupbox.collapse_widget()

                MainFunctions.setup_etb_settings(self, file_data)

                # Keep
                MainFunctions.set_page(self, self.ui.load_pages.etb_settings_subpage)
                upload_bttn = self.ui.right_column.etb_bttn_frame.findChild(PyPushButton, "input_file_menu_bttn")
                settings_bttn = self.ui.right_column.etb_bttn_frame.findChild(PyPushButton, "parameter_menu_bttn")
                upload_bttn.remove_highlight()
                settings_bttn.set_highlight()
            except ValueError as ve:
                exit_buttons = {
                    "Ok": QMessageBox.ButtonRole.AcceptRole,
                }

                exit_message_box = QtMessage(
                    buttons=exit_buttons,
                    color=self.themes["app_color"]["white"],
                    bg_color_one=self.themes["app_color"]["dark_one"],
                    bg_color_two=self.themes["app_color"]["bg_one"],
                    bg_color_hover=self.themes["app_color"]["dark_three"],
                    bg_color_pressed=self.themes["app_color"]["dark_four"]
                )
                exit_message_box.setIcon(QMessageBox.Icon.Critical)
                exit_message_box.setText("Invalid Sheets")
                exit_message_box.setDetailedText(str(ve))
                exit_message_box.exec()
            return
        else:
            return

        #if result_object:
        #    MainFunctions.setup_etb_settings(self, result_object)

    def setup_etb_settings(self, file_data: dict):
        settings = file_data

        general_groupbox: GeneralSettings
        general_groupbox = self.ui.load_pages.parameter_scroll_contents.findChild(QWidget, "general_groupbox")
        lesion_groupbox: SettingsGroupBox
        lesion_groupbox = self.ui.load_pages.parameter_scroll_contents.findChild(QWidget, "lesion_groupbox")
        historical_groupbox: SettingsGroupBox
        historical_groupbox = self.ui.load_pages.parameter_scroll_contents.findChild(QWidget, "historical_groupbox")
        available_groupbox: SettingsGroupBox
        available_groupbox = self.ui.load_pages.parameter_scroll_contents.findChild(QWidget, "available_groupbox")

        lesion_data = LesionSettings(
            data_dict=settings["scan_data"],
            header_color=self.themes["app_color"]["dark_four"],
            bg_color=self.themes["app_color"]["dark_two"],
            circle_color=self.themes["app_color"]["white"], # icon_color
            active_color=self.themes["app_color"]["context_color"],
            parent=lesion_groupbox
        )
        lesion_data.setObjectName(u"lesion_settings")

        historical_data = TxSettings(
            data_dict=settings["historical_treatments"],
            header_color=self.themes["app_color"]["dark_four"],
            treatment_bg=self.themes["app_color"]["blue_one"],
            parent=historical_groupbox
        )
        historical_data.setObjectName(u"historical_treatment_settings")

        lesions = settings["scan_data"]["abbr"]
        available_tx_data = AvailableTxSettings(
            lesion_names=lesions,
            data_dict=settings["available_treatments"],
            header_color=self.themes["app_color"]["dark_four"],
            treatment_bg=self.themes["app_color"]["blue_one"],
            bg_color=self.themes["app_color"]["dark_two"],
            circle_color=self.themes["app_color"]["white"], # icon_color
            active_color=self.themes["app_color"]["context_color"],
            parent=available_groupbox
        )
        available_tx_data.setObjectName(u"available_treatment_settings")

        general_groupbox.set_patient_file(settings["data_path"])
        lesion_groupbox.set_content(lesion_data)
        historical_groupbox.set_content(historical_data)
        available_groupbox.set_content(available_tx_data)

    def package_parameters(self):
        # **** Gather data by searching for target child widget ****
        general_groupbox = self.ui.load_pages.parameter_scroll_contents.findChild(QWidget, "general_groupbox")
        general_data = general_groupbox.get_data_dictionary()
        lesion_groupbox = self.ui.load_pages.parameter_scroll_contents.findChild(QWidget, "lesion_groupbox")
        lesion_data = lesion_groupbox.get_content_widget().get_data_dictionary()
        historical_tx_groupbox = self.ui.load_pages.parameter_scroll_contents.findChild(QWidget, "historical_groupbox")
        historical_tx_data = historical_tx_groupbox.get_content_widget().get_data_dictionary()
        available_tx_groupbox = self.ui.load_pages.parameter_scroll_contents.findChild(QWidget, "available_groupbox")
        available_treatments_widget = available_tx_groupbox.get_content_widget()
        available_tx_data = available_treatments_widget.get_data_dictionary()

        cone_settings = available_treatments_widget.get_cone_settings()
        cone_settings["toggled_treatments"] = available_tx_data
        if cone_settings['method'] == COMPARISON_CONE:
            simulate_index = lesion_data['abbr'].index(cone_settings['data']['target_lesion'])

            error_message = QtMessage(
                buttons={"Ok": QMessageBox.ButtonRole.AcceptRole},
                color=self.themes["app_color"]["white"],
                bg_color_one=self.themes["app_color"]["dark_one"],
                bg_color_two=self.themes["app_color"]["bg_one"],
                bg_color_hover=self.themes["app_color"]["dark_three"],
                bg_color_pressed=self.themes["app_color"]["dark_four"]
            )
            error_message.setIcon(QMessageBox.Icon.Warning)

            cone_drugs = list(cone_settings['data']['drugs'].keys())
            toggled_drugs = cone_settings['toggled_treatments']['abbr']

            length_check = len(cone_drugs) != len(toggled_drugs)
            content_check = sorted(cone_drugs) != sorted(toggled_drugs)
            simulate_check = not lesion_data['simulate'][simulate_index]

            if length_check:
                error_message.setText("Uneven cone treatments!")
                error_message.setDetailedText(
                    f"The amount of available treatments that are toggled do not match the amount of treatments registered into the cone settings." +
                    f"\nLength of Cone Treatments: {len(cone_drugs)}\nLength of Available Treatments: {len(toggled_drugs)}"
                )
                error_message.exec()
                return None
            elif content_check:
                error_message.setText("Mismatched treatment content!")
                error_message.setDetailedText(
                    f"The treatments registered in the cone settings do not match those that are toggled for available treatments." +
                    f"\nCone Drugs: {cone_drugs}\nToggled Available Drugs: {toggled_drugs}"
                )
                error_message.exec()
                return None
            elif simulate_check:
                error_message.setText("Target lesion not simulated!")
                error_message.setDetailedText(
                    f"The lesion selected in the comparison cone settings menu is not selected for simulation in the lesion settings." +
                    f"\nTo fix this:\n1. Go to the lesion settings box.\n2. Find the lesion you want to target for cone settings.\n3. Toggle the simulation button to \'on\'."
                )
                error_message.exec()
                return None

        return [general_data, lesion_data, historical_tx_data, available_tx_data, cone_settings]

    def save_etb_settings(self):
        # **** Gather all data from each area in the settings page of etb ****
        general_groupbox = self.ui.load_pages.parameter_scroll_contents.findChild(QWidget, "general_groupbox")
        general_data = general_groupbox.get_data_dictionary()
        lesion_data = self.ui.load_pages.parameter_scroll_contents.findChild(QWidget, "lesion_groupbox").get_content_widget()
        lesion_data = lesion_data.get_data_dictionary()
        historical_treatment_data = self.ui.load_pages.parameter_scroll_contents.findChild(QWidget, "historical_groupbox").get_content_widget()
        historical_treatment_data = historical_treatment_data.get_data_dictionary()
        available_treatment_data = self.ui.load_pages.parameter_scroll_contents.findChild(QWidget, "available_groupbox").get_content_widget()
        available_treatment_data = available_treatment_data.read_all()
        # available_treatment_data = available_treatment_data.get_data_dictionary()

        loaded_file = os.path.basename(general_data["file"])
        loaded_file = str(loaded_file).replace(".xlsx", "")

        encoded_numpy_matrix = json.dumps(self.reuse_matrix[True], cls=NumpyArrayEncoder)

        # **** Create a dictionary of dictionaries to store settings state ****
        settings_data = {
            "file_id": loaded_file,
            "general": general_data,
            "lesion": lesion_data,
            "historical_treatments": historical_treatment_data,
            "available_treatments": available_treatment_data,
            "nonsystemic_matrix": encoded_numpy_matrix
        }

        # Convert date objects to strings
        for date_list in ["date_on", "date_off"]:
            settings_data["historical_treatments"][date_list] = [date.isoformat() for date in settings_data["historical_treatments"][date_list]]
            settings_data["available_treatments"][date_list] = [date.isoformat() if date else None for date in settings_data["available_treatments"][date_list]]

        # TODO: Please note that you’ll need to reverse this conversion when loading the data from the JSON file.
        # You can use the datetime.datetime.fromisoformat() function to convert the date strings back into date objects.

        # **** Create a file dialog to allow user to create saved settings file ****
        print(f'Working directory when saving:\n{working_directory}')
        if working_directory is not None:
            initial_directory = working_directory
        else:
            initial_directory = QDir.homePath()

        print(f'Initial Directory: \n{initial_directory}')

        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setDefaultSuffix('json')
        file_dialog.setDirectory(initial_directory)

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            filename = file_dialog.selectedFiles()[0]

            # **** Write to json file ****
            if filename:
                with open(filename, "w") as file:
                    json.dump(settings_data, file)
            else:
                return

    def load_etb_settings(self):
        general_groupbox = self.ui.load_pages.parameter_scroll_contents.findChild(QWidget, "general_groupbox")
        patient_file = general_groupbox.get_patient_file()

        error_message = QtMessage(buttons={"Ok": QMessageBox.ButtonRole.AcceptRole},
                        color=self.themes["app_color"]["white"],
                        bg_color_one=self.themes["app_color"]["dark_one"],
                        bg_color_two=self.themes["app_color"]["bg_one"],
                        bg_color_hover=self.themes["app_color"]["dark_three"],
                        bg_color_pressed=self.themes["app_color"]["dark_four"])
        error_message.setIcon(QMessageBox.Icon.Warning)

        if patient_file is not None:
            settings_file = general_groupbox.get_settings_file()

            if os.path.exists(settings_file) and is_json_file(settings_file):
                # load_parameters_from_json
                with open(settings_file, "r") as file:
                    parameters = json.load(file)

                # apply parameters to child widgets
                if parameters["file_id"] in patient_file:
                    try:
                        for date_list in ["date_on", "date_off"]:
                            parameters["historical_treatments"][date_list] = [datetime.fromisoformat(date).strftime("%m/%d/%Y") for date in parameters["historical_treatments"][date_list]]
                            parameters["available_treatments"][date_list] = [datetime.fromisoformat(date).strftime("%m/%d/%Y") if date else None for date in parameters["available_treatments"][date_list]]

                        general_groupbox.set_clean_lesions()
                        lesion_settings = self.ui.load_pages.parameter_scroll_contents.findChild(QWidget, "lesion_groupbox").findChild(QWidget, "lesion_settings")
                        lesion_settings.import_settings(parameters["lesion"])
                        historical_settings = self.ui.load_pages.parameter_scroll_contents.findChild(QWidget, "historical_groupbox").findChild(QWidget, "historical_treatment_settings")
                        historical_settings.import_settings(parameters["historical_treatments"])
                        available_settings = self.ui.load_pages.parameter_scroll_contents.findChild(QWidget, "available_groupbox").findChild(QWidget, "available_treatment_settings")
                        available_settings.import_settings(parameters["available_treatments"])

                        matrix = json.loads(parameters["nonsystemic_matrix"])
                        matrix = np.array(matrix)

                        self.reuse_bool = True
                        self.reuse_matrix[self.reuse_bool] = matrix
                    except Exception as e:
                        error_message.setIcon(QMessageBox.Icon.Critical)
                        error_message.setText("Error Encountered Applying Settings.")
                        error_message.setInformativeText(str(e))
                        error_message.exec()
                else:
                    error_message.setText("Mismatched Files")
                    error_message.setInformativeText("Settings file contains a different ID than the loaded patient data file. ID follows naming convention of patient file.")
                    error_message.exec()
            else:
                error_message.setText("Wrong File Submitted.")
                error_message.setInformativeText("Empty submission or file type not applicable to this menu. Create/Select the appropriate file.")
                error_message.exec()
        else:
            error_message.setText("No Data To Apply Settings.")
            error_message.setInformativeText("No patient data file has been submitted to apply settings to.")
            error_message.exec()

    def on_apply_clicked(self):
        pass
        # parameters = load_parameters_from_csv(filename)
        # self.update_widgets_with_parameters(parameters)

    def convert_date_format(self, date: str):
        date_obj = datetime.strptime(date, "%Y-%m-%d")

        formatted_date = datetime.strftime("%m/%d/%Y")

        return formatted_date

    def test_run(self):
        command = 'select * from Tumors;'

        sql_obj = MySQLConnector()
        sql_obj.set_sql_information(
            host='localhost',
            user='root',
            password='DeusFortitudoMea99#',
            database='etb_project_db'
        )
        sql_obj.establish_connection()
        results = sql_obj.issue_command(command)
        sql_obj.close_connection()

        self.wid = QWidget()

        lab_1 = QLabel(self.wid)
        lab_1.setText('Command Used: '+ command)
        lab_1.setStyleSheet('font-weight: bold;')

        text_area = QTextEdit(self.wid)
        text_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_area.setReadOnly(True)
        for each in results:
            text_area.append(str(each))
        # text_area.setText(str(results))

        lay = QVBoxLayout(self.wid)
        lay.addWidget(lab_1, alignment=Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(text_area)

        self.wid.show()

        print(f'Received results:\n{str(results)}')
