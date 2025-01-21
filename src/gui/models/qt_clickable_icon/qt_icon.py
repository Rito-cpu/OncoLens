from src.core.pyqt_core import *
from src.core.image_functions import Functions
from src.core.json.json_themes import Themes


class QtMenuIcon(QLabel):
    clicked = pyqtSignal(bool)

    def __init__(
        self,
        icon_name: str,
        icon_size: int,
        color: str = None,
        set_checkable: bool = False,
        parent=None
    ):
        super().__init__()

        if parent is not None:
            self.setParent(parent)

        themes = Themes()
        self.themes = themes.items

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(icon_size, icon_size)

        self._color = self.themes["app_color"]["dark_three"] if color is None else color
        self._icon_path = Functions.set_svg_icon(icon_name)
        self._is_toggle_active = False
        self.set_checkable = set_checkable
        self.checked = True
        if self.set_checkable:
            self.checked = False

        self.set_svg_icon_to_label(self._icon_path)

    def mousePressEvent(self, ev):
        if not self.set_checkable:
            self.checked = not(self.checked)
            self.clicked.emit(self.checked)
        else:
            self.clicked.emit(True)
        return super().mousePressEvent(ev)

    def set_svg_icon_to_label(self, svg_path: str):
            # Create an SVG renderer
            renderer = QSvgRenderer(svg_path)
            
            # Create a QPixmap to render the SVG onto
            pixmap = QPixmap(self.size())  # Size it to the label dimensions
            pixmap.fill(Qt.GlobalColor.transparent)  # Optional: make background transparent

            # Paint the SVG onto the QPixmap
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.setCompositionMode(painter.CompositionMode.CompositionMode_SourceIn)
            painter.fillRect(pixmap.rect(), QColor(self._color))
            painter.end()

            # Set the QPixmap to the QLabel
            self.setPixmap(
                pixmap.scaled(
                    self.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )

            # Ensure the QLabel will resize the icon as it changes size
            self.setScaledContents(True)

    def resize_icon(self, new_size: int):
        self.setFixedSize(new_size, new_size)