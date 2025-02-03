import gc

from src.core.pyqt_core import *
from .styles import *


class SettingsGroupBox(QWidget):
    def __init__(
        self,
        title: str,
        animation_duration: int=400,
        color: str="black",
        radius: int=13,
        bg_color_one: str="rgba(12, 205, 163, 255)",
        bg_color_two: str="rgba(29, 209, 167, 255)",
        bg_color_three: str="rgba(193, 252, 211, 255)",
        point_size: int=14,
        parent=None
    ) -> None:
        super().__init__()

        if parent is not None:
            self.setParent(parent)

        self._title = title
        self._animation_duration = animation_duration
        self._color = color
        self._radius = radius
        self._bg_color_one = bg_color_one
        self._bg_color_two = bg_color_two
        self._bg_color_three = bg_color_three
        self._point_size = point_size

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Setup Ui
        self.set_widget()

        # Set Signals
        self.toggle_button.toggled.connect(self._toggle)

    def set_widget(self):
        # --- Header Box ---
        self.toggle_button = QToolButton()
        self.toggle_button.setStyleSheet("border: none; color: {}; font: {}pt;".format(self._color, self._point_size))
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.ArrowType.RightArrow)
        self.toggle_button.setIconSize(QSize(9, 9))
        self.toggle_button.setText(self._title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(False)
        self.toggle_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.header_line = QFrame()
        self.header_line.setFrameShape(QFrame.Shape.HLine)
        self.header_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.header_line.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.header_line.setMaximumHeight(1)
        self.header_line.setStyleSheet("background: black;")

        # --- Content Container Initialization ---
        self._main_content = None

        self.scroll_contents = QWidget()
        self.scroll_contents.setObjectName(u"contents")
        self.scroll_contents.setObjectName("ContentContainer")
        self.scroll_contents.setStyleSheet("background-color: transparent; border: none;")

        self.scroll_contents_layout = QVBoxLayout(self.scroll_contents)
        self.scroll_contents_layout.setObjectName(u"scroll_contents_layout")
        self.scroll_contents_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_contents_layout.setSpacing(0)

        # custom_style = groupbox_gradient_template.format(
        #     _radius = self._radius,
        #     _bg_color_one = self._bg_color_one,
        #     _bg_color_two = self._bg_color_two,
        #     _bg_color_three = self._bg_color_three
        # )
        custom_style = groupbox_template.format(
            _radius = self._radius,
            _bg_color_one = self._bg_color_two
        )
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setStyleSheet(custom_style)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(self.scroll_contents)

        scroll_area_layout = QVBoxLayout()
        scroll_area_layout.setContentsMargins(18, 0, 0, 0)
        scroll_area_layout.addWidget(self.scroll_area)

        # --- Set as collapsed ---
        self.scroll_area.setMaximumHeight(0)
        self.scroll_area.setMinimumHeight(0)

        self.toggle_animation = QParallelAnimationGroup()
        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self.scroll_area, b"maximumHeight"))

        row = 0
        main_layout = QGridLayout(self)
        main_layout.setVerticalSpacing(5)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.toggle_button, row, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(self.header_line, row, 2, 1, 1)
        main_layout.addLayout(scroll_area_layout, row + 1, 0, 1, 3)

    def set_content(self, content: QWidget, new_duarion: int = None) -> None:
        # self._toggle(False)
        self._clear_layout()

        if new_duarion != None:
            self._animation_duration = new_duarion

        self._main_content = content
        self.scroll_contents_layout.addWidget(content)
        collapsed_height = self.sizeHint().height() - self.scroll_area.maximumHeight()
        content_height = content.sizeHint().height()

        for index in range(0, self.toggle_animation.animationCount() - 1):
            section_animation = self.toggle_animation.animationAt(index)
            section_animation.setDuration(self._animation_duration)
            section_animation.setStartValue(collapsed_height)
            section_animation.setEndValue(collapsed_height + content_height)
            # section_animation.setEndValue(250)

        content_animation = self.toggle_animation.animationAt(self.toggle_animation.animationCount() - 1)
        content_animation.setDuration(self._animation_duration)
        content_animation.setStartValue(0)
        content_animation.setEndValue(content_height)

        self._animation_duration = 400

    def _toggle(self, collapsed: bool) -> None:
        if collapsed:
            self.toggle_button.setArrowType(Qt.ArrowType.DownArrow)
            self.toggle_animation.setDirection(QAbstractAnimation.Direction.Forward)
        else:
            self.toggle_button.setArrowType(Qt.ArrowType.RightArrow)
            self.toggle_animation.setDirection(QAbstractAnimation.Direction.Backward)
        self.toggle_animation.start()

    def is_expanded(self):
        return self.toggle_button.isChecked()

    def collapse_widget(self):
        self.toggle_button.setChecked(False)
        self._toggle(False)

    def _clear_layout(self) -> None:
        self._main_content = None

        if self.scroll_contents_layout.count() > 0:
            for index in reversed(range(self.scroll_contents_layout.count())):
                widget = self.scroll_contents_layout.itemAt(index).widget()
                widget.setParent(None)
                del widget
            gc.collect()

    def set_empty(self) -> None:
        null_container = QWidget()
        null_container.setStyleSheet(data_template.format(_font_size=12))

        null_label = QLabel(text='Empty', parent=null_container)

        null_layout = QVBoxLayout(null_container)
        null_layout.addWidget(null_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.set_content(content=null_container, new_duarion=150)

    def get_content_widget(self) -> QWidget:
        return self._main_content if not None else -1
