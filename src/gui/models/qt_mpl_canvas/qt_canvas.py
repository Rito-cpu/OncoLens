from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure


class QtMplCanvas(FigureCanvasQTAgg):
    def __init__(self,
                fig: Figure,
                ax,
                width: int=5,
                height: int=4,
                parent=None) -> None:

        self.axes = ax
        super().__init__(fig)

    def set_dpi(self, dpi: int):
        self.figure.set_dpi(dpi)

    def get_axes(self):
        return self.axes
