from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.gui.models.qt_combo_widget import QtComboBox
from src.gui.models.py_table_widget import PyTableWidget
from src.gui.models.qt_cone_widget import QtConeWidget


class QtComparisonConeWidget(QWidget):
    NUM_REGIMENS: int = 3
    REGIMENS: list[str] = ['A', 'B', 'C']

    def __init__(
            self,
            lesion_names: list,
            treatments: dict,
            num_lesions: int,
            num_drugs: int,
            bg_color: str = 'black',
            text_color: str = 'white',
            font_size: int = 12,
            parent=None
        ):
        super().__init__()

        if parent != None:
            self.setParent(parent)

        self.setObjectName(u'comparison_settings')
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self._lesion_names = lesion_names
        self._treatments = treatments
        self._num_lesions = num_lesions
        self._num_drugs = num_drugs
        self._bg_color = bg_color
        self._text_color= text_color
        self._font_size = font_size

        themes = Themes()
        self.themes = themes.items

        # Only want to have 1 cone if 1 drug is available
        if num_drugs == 1:
            self.change_num_regimens(1)

        self.setup_widget()
        self.setStyleSheet("""
            QWidget#comparison_settings {{
                background: {theme};
                border: none;
                border-radius: 8px;
            }}
        """.format(theme=self.themes["app_color"]["green_two"]))

    def setup_widget(self):
        lesion_interaction_frame = QFrame(self)
        lesion_interaction_frame.setObjectName(u'lesion_interaction_frame')
        lesion_interaction_frame.setFrameShape(QFrame.Shape.NoFrame)
        lesion_interaction_frame.setFrameShadow(QFrame.Shadow.Raised)
        lesion_interaction_frame.setStyleSheet('background: rgba(255, 255, 255, 175); border-radius: 8px;')

        self.dropdown_label = QLabel(lesion_interaction_frame)
        self.dropdown_label.setObjectName(u'dropdown_label')
        self.dropdown_label.setText("Apply Comparison Cone(s) to:")
        self.dropdown_label.setStyleSheet("""
            QLabel {{
                color: {color};
                font-size: {text}px;
                background: transparent;
            }}
        """.format(color=self._bg_color, text=self._font_size))

        self.lesion_dropdown = QtComboBox(
            bg_color=self.themes["app_color"]["dark_one"],
            text_color=self.themes["app_color"]["white"],
            parent=lesion_interaction_frame
        )
        self.lesion_dropdown.setObjectName(u'lesion_dropdown')
        self.lesion_dropdown.addItems(self._lesion_names)
        self.lesion_dropdown.setCurrentIndex(0)
        self.lesion_dropdown.setFixedSize(95, 25)

        dropdown_interaction_layout = QFormLayout(lesion_interaction_frame)
        dropdown_interaction_layout.setObjectName(u'dropdown_interaction_layout')
        dropdown_interaction_layout.addRow(self.dropdown_label, self.lesion_dropdown)

        self._regimen_table = PyTableWidget(
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
                context_color = self.themes["app_color"]["context_color"],
                font_size=11,
                parent=self
            )
        self._regimen_table.setObjectName(u'regimen_table')
        self._regimen_table.setMinimumWidth(250)
        self._regimen_table.setRowCount(self._num_drugs)
        self._regimen_table.setColumnCount(self.NUM_REGIMENS)
        self._regimen_table.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self._regimen_table.setHorizontalHeaderLabels(self.REGIMENS)
        self._regimen_table.setVerticalHeaderLabels(self._treatments.keys())
        self._regimen_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._regimen_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self._regimen_table.resizeRowsToContents()
        self._regimen_table.horizontalHeader().show()
        self._regimen_table.verticalHeader().show()
        self._regimen_table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self._regimen_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._regimen_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._regimen_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self._regimen_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.column_chbx_dict = {}
        for row_index in range(self._num_drugs):
            for col_index in range(self.NUM_REGIMENS):
                if self.REGIMENS[col_index] not in self.column_chbx_dict:
                    self.column_chbx_dict[self.REGIMENS[col_index]] = []

                checkbox_cell = QWidget(self._regimen_table)
                checkbox_cell.setObjectName(u"checkbox_cell")

                checkbox = QCheckBox(checkbox_cell)
                checkbox.setChecked(False)
                self.column_chbx_dict[self.REGIMENS[col_index]].append(checkbox)

                checkbox_layout = QHBoxLayout(checkbox_cell)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)
                checkbox_layout.addWidget(checkbox)
                checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                self._regimen_table.setCellWidget(row_index, col_index, checkbox_cell)

        scroll_center = QWidget()
        scroll_center.setObjectName(u'scroll_center')

        scroll_layout = QVBoxLayout(scroll_center)
        scroll_layout.setObjectName(u'scroll_layout')
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(15)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMaximumHeight(300)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(scroll_center)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border-radius: 8px;
                border: none;
            }
        """)

        self.settings_list = []
        for key, value in self._treatments.items():
            cone_setting = QtConeWidget(header=key, averages=value, parent=scroll_center)
            self.settings_list.append(cone_setting)

            scroll_layout.addWidget(cone_setting)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        main_layout.addWidget(lesion_interaction_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self._regimen_table, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.scroll_area, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setMinimumSize(main_layout.sizeHint())

    def change_num_regimens(self, new_value: int):
        self.NUM_REGIMENS = new_value
        self.REGIMENS = ['A']

    def get_target_lesion(self):
        return self.lesion_dropdown.currentText()

    def get_active_columns(self):
        active_columns = []

        for key in self.column_chbx_dict.keys():
            for chbx in self.column_chbx_dict[key]:
                if chbx.isChecked():
                    active_columns.append(key)
                    break

        return active_columns

    def create_regimen_schedule(self):
        active_columns = self.get_active_columns()
        drug_plan = {}
        # TODO: Scenario where no drug is selected!!

        for key in self.column_chbx_dict.keys():
            if key in active_columns:
                drug_plan[key] = []
                for index in range(len(self.column_chbx_dict[key])):
                    if self.column_chbx_dict[key][index].isChecked():
                        drug_plan[key].append(self._treatments[index])
                if len(drug_plan[key]) == 2:
                    drug_plan[key] = drug_plan[key][0] + '+' + drug_plan[key][1]
                elif len(drug_plan[key]) > 2:
                    cocktail = drug_plan[key][0]
                    for name in drug_plan[key][1:]:
                        cocktail += '+' + name
                    drug_plan[key] = cocktail
            else:
                continue

        return drug_plan

    def get_checked_rows(self, regimen: str):
        if regimen == 'A':
            column_index = 0
        elif regimen == 'B':
            column_index = 1
        else:
            column_index = 2

        selected_drugs = []
        for row in range(self._regimen_table.rowCount()):
            checkbox_item = self._regimen_table.cellWidget(row, column_index)
            if isinstance(checkbox_item, QWidget):
                child_chbx = checkbox_item.findChild(QCheckBox)
                if child_chbx.isChecked():
                    row_name = self._regimen_table.verticalHeaderItem(row).text()
                    selected_drugs.append(row_name)

        return selected_drugs

    def check_duplicate_regimens(self, regimen_dict: dict):
        flattened_values = [item for sublist in regimen_dict.values() for item in sublist]

        # Check if the number of unique values is equal to the total number of values
        if len(flattened_values) != len(set(flattened_values)):
            return 'Error: dup found'
        else:
            return "The dictionary values are unique."

    def get_comparison_settings(self):
        active_regimens = self.get_active_columns()
        if len(active_regimens) == 0:
            return None

        target_lesion = self.get_target_lesion()

        # Get active treatments per regimen and store in a dictionary
        regimens = {}
        for current_regimen in active_regimens:
            selected_rows = self.get_checked_rows(current_regimen)
            regimens[current_regimen] = selected_rows

        result = self.check_duplicate_regimens(regimens)
        # print(f'Result: {result}')

        # Get each lesions values
        drug_widgets = {}
        drug_setting: QtConeWidget
        for drug_setting in self.settings_list:
            name = drug_setting.get_header()
            drug_widgets[name] = drug_setting

        settings = {
            'target_lesion': target_lesion,
            'regimens': regimens,
            'num_regimens': len(active_regimens),
            'drugs': drug_widgets
        }

        return settings

    def get_num_regimens(self):
        return self.NUM_REGIMENS

    def get_regimens(self):
        return self.REGIMENS

    def get_average_values(self):
        average_list = {}

        widget: QtConeWidget
        for widget in self.settings_list:
            average_list[widget.get_header()] = widget.get_average_values()

        return average_list

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, o, p, self)
