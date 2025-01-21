from src.core.pyqt_core import *
from .qt_canvas import QtMplCanvas
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure


class QtPlotMenu(QWidget):
    def __init__(self,
                fig: Figure,
                ax,
                dpi: int=100,
                parent=None):
        super().__init__()

        if parent != None:
            self.setParent(parent)

        self._fig = fig
        self._ax = ax
        self._dpi = dpi

        self.setup_widget()

    def setup_widget(self):
        self.setStyleSheet("background: transparent;")

        self._canvas = QtMplCanvas(fig=self._fig, ax=self._ax, parent=self)
        self._canvas.set_dpi(self._dpi)

        self.navigation_toolbar = NavigationToolbar2QT(self._canvas, self)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(15)
        main_layout.addWidget(self.navigation_toolbar)
        main_layout.addWidget(self._canvas, stretch=1)

    def draw(self):
        self._canvas.draw()

    def get_axes(self):
        return self._canvas.get_axes()
