from src.core.pyqt_core import *
from src.gui.models.py_table_widget.style import style


class PyTableWidget(QTableWidget):
    def __init__(
        self,
        radius = 8,
        color = "#FFF",
        bg_color = "#444",
        selection_color = "#FFF",
        header_horizontal_color = "#333",
        header_vertical_color = "#444",
        bottom_line_color = "#555",
        grid_line_color = "#555",
        scroll_bar_bg_color = "#FFF",
        scroll_bar_btn_color = "#333",
        context_color = "#00ABE8",
        font_size: int = 12,
        parent=None
    ):
        super().__init__()

        if parent != None:
            self.setParent(parent)

        # PARAMETERS
        style_template = style.format(
            _font_size=font_size,
            _radius = radius,
            _color = color,
            _bg_color = bg_color,
            _header_horizontal_color = header_horizontal_color,
            _header_vertical_color = header_vertical_color,
            _selection_color = selection_color,
            _bottom_line_color = bottom_line_color,
            _grid_line_color = grid_line_color,
            _scroll_bar_bg_color = scroll_bar_bg_color,
            _scroll_bar_btn_color = scroll_bar_btn_color,
            _context_color = context_color,
        )
        self.setStyleSheet(style_template)

    def sizeHint(self):
        # Calculate the height based on the number of rows and the height of each row
        total_height = sum(self.rowHeight(row) for row in range(self.rowCount()))
        # Add a bit of extra space (for headers, etc.) if needed
        total_height += self.horizontalHeader().height() + 4

        return QSize(self.width(), total_height)
