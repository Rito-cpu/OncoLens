import pandas as pd

from src.core.pyqt_core import *
from src.gui.models.py_table_widget import PyTableWidget

class NonSystemicSettings(QWidget):
    def __init__(
            self,
            *args,
            reuseable_data=None,
            parent=None
        ) -> None:
        super().__init__()

        self._lesion_names, self._tx_names, self._tx_on_dates, self.nonsystemic_table = args
        self._reuseable_data = reuseable_data

        # --- Finds nonsystemic treatments ---
        holder = []
        holder_2 = []
        for index in range(len(self._tx_names)):
            if 'rad' in self._tx_names[index].lower() or 'surg' in self._tx_names[index].lower():
                holder.append(self._tx_names[index])
                # holder_2.append(self._tx_on_dates[index])
                test = f"{self._tx_names[index]} ({self._tx_on_dates[index].strftime('%m-%d-%Y')})"
                holder_2.append(test)
        self._tx_names = holder
        self._tx_on_dates = holder_2

        self._num_lesions = len(self._lesion_names)
        self._num_tx = len(self._tx_names)

        self.setup_widget()

    def setup_widget(self):
        self.nonsystemic_table.setRowCount(self._num_tx)
        self.nonsystemic_table.setColumnCount(self._num_lesions)
        self.nonsystemic_table.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.nonsystemic_table.setHorizontalHeaderLabels(self._lesion_names)
        self.nonsystemic_table.setVerticalHeaderLabels(self._tx_on_dates)
        self.nonsystemic_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.nonsystemic_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.nonsystemic_table.resizeRowsToContents()
        self.nonsystemic_table.horizontalHeader().show()
        self.nonsystemic_table.verticalHeader().show()
        # self.nonsystemic_table.setFixedHeight(self.nonsystemic_table.verticalHeader().length() + self.nonsystemic_table.horizontalHeader().height() + 10)
        self.nonsystemic_table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nonsystemic_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.nonsystemic_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.nonsystemic_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.nonsystemic_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        for row_index in range(self._num_tx):
            for col_index in range(self._num_lesions):
                checkbox = QCheckBox()

                if self._reuseable_data is not None and self._reuseable_data[row_index][col_index] == 1:
                    checkbox.setChecked(True)
                else:
                    checkbox.setChecked(False)
                checkbox_cell = QWidget()
                checkbox_cell.setObjectName(u"checkbox_cell")

                checkbox_layout = QHBoxLayout(checkbox_cell)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)
                checkbox_layout.addWidget(checkbox)
                checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                self.nonsystemic_table.setCellWidget(row_index, col_index, checkbox_cell)

        _main_layout = QVBoxLayout(self)
        _main_layout.setContentsMargins(0, 0, 0, 0)
        _main_layout.addWidget(self.nonsystemic_table)

    def get_matrix(self):
        matrix_values = []
        for row_index in range(self._num_tx):
            col_values = []
            for col_index in range(self._num_lesions):
                cell_widget = self.nonsystemic_table.cellWidget(row_index, col_index)
                if cell_widget is None:
                    continue

                cell_layout = cell_widget.layout()
                cell_checkbox = cell_layout.itemAt(0).widget()
                value = 1 if cell_checkbox.isChecked() else 0
                col_values.append(value)
            matrix_values.append(col_values)

        matrix_df = pd.DataFrame(matrix_values)
        print(matrix_df)
        print(self._lesion_names)
        print(self._tx_names)
        matrix_df.columns = self._lesion_names
        matrix_df.index = self._tx_names

        matrix_dict = {
            "dataframe": matrix_df,
            "array": matrix_df.to_numpy()
        }

        return matrix_dict
