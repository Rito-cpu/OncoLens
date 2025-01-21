from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from .py_table_widget import PyTableWidget


class QtConeTable(QFrame):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        if parent != None:
            self.setParent(parent)

        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        themes = Themes()
        self.themes = themes.items

        self.setup_widget()

    def setup_widget(self):
        self.nonsystemic_table = PyTableWidget(
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

        self.nonsystemic_table.setColumnCount(7)
        self.nonsystemic_table.setHorizontalHeaderLabels(["Use Cone", "Min Efficacy", "Max Efficacy", "Min Resistance", "Max Resistance", "Min Sensitivity", "Max Sensitivity"])
        self.nonsystemic_table.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.nonsystemic_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.nonsystemic_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.nonsystemic_table.resizeRowsToContents()
        self.nonsystemic_table.horizontalHeader().show()
        self.nonsystemic_table.verticalHeader().show()
        self.nonsystemic_table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nonsystemic_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.nonsystemic_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.nonsystemic_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.nonsystemic_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.nonsystemic_table)

    def set_cone_settings(self, cone_settings_list):
        self.nonsystemic_table.setRowCount(len(cone_settings_list))
        self.nonsystemic_table.setVerticalHeaderLabels(cone_settings_list)

        for row in range(len(cone_settings_list)):
            use_cones_checkbox = QCheckBox(self.nonsystemic_table)
            use_cones_checkbox.setChecked(False)

            self.nonsystemic_table.setCellWidget(row, 0, use_cones_checkbox)

            # use_cones_checkbox.setChecked(tx_name["use_cones"])

            for col in range(self.nonsystemic_table.columnCount()-1):
                spin_box = QDoubleSpinBox(self.nonsystemic_table)
                # spin_box.setValue(cone_settings[parameter])
                spin_box.setValue(1.0)
                self.nonsystemic_table.setCellWidget(row, col + 1, spin_box)


    def get_cone_settings(self):
        cone_settings_list = []

        for row in range(self.rowCount()):
            use_cones_checkbox = self.cellWidget(row, 0)
            min_drug_kill = float(self.item(row, 1).text())
            max_drug_kill = float(self.item(row, 2).text())
            min_resistance = float(self.item(row, 3).text())
            max_resistance = float(self.item(row, 4).text())
            min_sensitivity = float(self.item(row, 5).text())
            max_sensitivity = float(self.item(row, 6).text())

            cone_settings_list.append({
                "use_cones": use_cones_checkbox.isChecked(),
                "min_drug_kill": min_drug_kill,
                "max_drug_kill": max_drug_kill,
                "min_resistance": min_resistance,
                "max_resistance": max_resistance,
                "min_sensitivity": min_sensitivity,
                "max_sensitivity": max_sensitivity,
            })

        return cone_settings_list
