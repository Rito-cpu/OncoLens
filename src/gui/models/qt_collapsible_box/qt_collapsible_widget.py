import gc

from src.core.pyqt_core import *
from src.core.app_config import IMG_RSC_PATH
from src.core.json.json_themes import Themes
from src.gui.models.py_toggle import PyToggle


class QtCollapsibleWidget(QWidget):
    def __init__(
        self,
        title: str,
        help_msg: str = '',
        animation_duration: int=400,
        radius: int=13,
        point_size: int=14,
        parent=None
    ):
        super().__init__()

        if parent is not None:
            self.setParent(parent)

        self._title = title
        self._help_msg = help_msg
        self._animation_duration = animation_duration
        self._radius = radius
        self._point_size = point_size
        self._message_window = None

        themes = Themes()
        self.themes = themes.items

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Setup Ui
        self._setup_widget()

        # Set Signals
        self.collapse_toggle.clicked.connect(self.toggle_collapsed)

    def _setup_widget(self):
        container_frame = QFrame(self)
        container_frame.setObjectName('container_widget')
        container_frame.setFrameShape(QFrame.Shape.NoFrame)
        container_frame.setFrameShadow(QFrame.Shadow.Plain)

        # --- Header Box ---
        header_area = QFrame(container_frame)
        header_area.setObjectName('header_area')
        header_area.setFrameShape(QFrame.Shape.NoFrame)
        header_area.setFrameShadow(QFrame.Shadow.Plain)

        icon_path = str(IMG_RSC_PATH / "downloads" / "bqm.png")

        self.help_bttn = QToolButton(header_area)
        self.help_bttn.setObjectName('help_bttn')
        self.help_bttn.setIcon(QIcon(icon_path))
        self.help_bttn.setIconSize(QSize(30, 30))
        self.help_bttn.setStyleSheet('background: none; border: none;')
        self.help_bttn.setCursor(Qt.CursorShape.PointingHandCursor)

        toggle_frame = QFrame(header_area)
        toggle_frame.setObjectName('toggle_frame')
        toggle_frame.setFrameShape(QFrame.Shape.NoFrame)
        toggle_frame.setFrameShadow(QFrame.Shadow.Plain)

        default_label = QLabel(toggle_frame)
        default_label.setObjectName('default_label')
        default_label.setText('(Default)')
        default_label.setStyleSheet(f'font-size: 12px; color: {self.themes["app_color"]["text_color"]};')

        self.collapse_toggle = PyToggle(
            width=34,
            height=20,
            ellipse_y=2,
            bg_color = self.themes['app_color']['text_color'],
            circle_color = self.themes['app_color']['yellow_bg'],
            active_color = self.themes['app_color']['blue_bg'],
            parent=toggle_frame
        )
        self.collapse_toggle.setObjectName('collapse_toggle')
        self.collapse_toggle.setChecked(True)

        toggle_layout = QVBoxLayout(toggle_frame)
        toggle_layout.setObjectName('toggle_layout')
        toggle_layout.setContentsMargins(0, 0, 0, 0)
        toggle_layout.setSpacing(1)
        toggle_layout.addWidget(default_label, alignment=Qt.AlignmentFlag.AlignCenter)
        toggle_layout.addWidget(self.collapse_toggle, alignment=Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(container_frame)
        title_label.setObjectName('title_label')
        title_label.setText(self._title)
        title_label.setStyleSheet(f'font-size: 16px; color: {self.themes["app_color"]["text_color"]};')

        header_layout = QHBoxLayout(header_area)
        header_layout.setObjectName('header_layout')
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(10)
        header_layout.addWidget(self.help_bttn)
        header_layout.addWidget(title_label)
        header_layout.addWidget(toggle_frame)

        self.header_line = QFrame(container_frame)
        self.header_line.setFrameShape(QFrame.Shape.HLine)
        self.header_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.header_line.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self.header_line.setMaximumHeight(1)
        self.header_line.setStyleSheet("background: black;")

        # --- Content Container Initialization ---
        self.imported_content = None

        self.scroll_contents = QWidget()
        self.scroll_contents.setObjectName("scroll_contents")
        self.scroll_contents.setStyleSheet("background-color: transparent; border: none;")

        self.scroll_contents_layout = QVBoxLayout(self.scroll_contents)
        self.scroll_contents_layout.setObjectName(u"scroll_contents_layout")
        self.scroll_contents_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_contents_layout.setSpacing(0)

        groupbox_template = """
            QScrollArea {{
                border: none;
                border-radius: {_radius}px;
                background-color: {_bg_color_one};
            }}
        """
        custom_style = groupbox_template.format(
            _radius = self._radius,
            _bg_color_one = self.themes['app_color']['yellow_bg']
        )
        
        scroll_area_container = QFrame(container_frame)
        scroll_area_container.setObjectName('scroll_area_container')
        scroll_area_container.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area_container.setFrameShadow(QFrame.Shadow.Plain)

        self.scroll_area = QScrollArea(scroll_area_container)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setStyleSheet(custom_style)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(self.scroll_contents)

        scroll_area_layout = QVBoxLayout(scroll_area_container)
        scroll_area_layout.setObjectName('scroll_area_layout')
        scroll_area_layout.setContentsMargins(18, 0, 0, 0)
        scroll_area_layout.addWidget(self.scroll_area)

        # --- Set as collapsed ---
        self.scroll_area.setMaximumHeight(0)
        self.scroll_area.setMinimumHeight(0)

        self.toggle_animation = QParallelAnimationGroup()
        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self.scroll_area, b"maximumHeight"))

        container_layout = QGridLayout(container_frame)
        container_layout.setContentsMargins(5, 5, 5, 5)
        container_layout.setVerticalSpacing(5)
        container_layout.addWidget(header_area, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        container_layout.addWidget(self.header_line, 0, 2, 1, 1)
        container_layout.addWidget(scroll_area_container, 1, 0, 1, 3)
        
        main_layout = QVBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container_frame)

    def set_content(self, content: QWidget, new_duarion: int = None):
        # self._toggle(False)
        self.clear_layout()

        if new_duarion is not None:
            self._animation_duration = new_duarion

        self.imported_content = content
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

    def toggle_collapsed(self, collapsed: bool):
        if collapsed:
            #self.collapse_toggle.setChecked(False)
            self.toggle_animation.setDirection(QAbstractAnimation.Direction.Backward)
        else:
            #self.collapse_toggle.setChecked(True)
            self.toggle_animation.setDirection(QAbstractAnimation.Direction.Forward)
        self.toggle_animation.start()
    
    def using_default(self):
        return self.collapse_toggle.isChecked()

    def collapse_widget(self):
        self.collapse_toggle.setChecked(False)
        self.toggle_collapsed(False)

    def clear_layout(self):
        self.imported_content = None

        if self.scroll_contents_layout.count() > 0:
            for index in reversed(range(self.scroll_contents_layout.count())):
                widget = self.scroll_contents_layout.itemAt(index).widget()
                widget.setParent(None)
                del widget
            gc.collect()

    def on_msg_close(self):
        self._message_window = None

    def set_empty(self):
        null_container = QWidget()
        null_container.setObjectName('null_container')

        null_label = QLabel(null_container)
        null_label.setObjectName('null_label')
        null_label.setText('Empty')
        null_label.setStyleSheet(f'font-size: 12px; color: {self.themes["app_color"]["text_color"]}')

        null_layout = QVBoxLayout(null_container)
        null_layout.setObjectName('null_layout')
        null_layout.setContentsMargins(5, 5, 5, 5)
        null_layout.addWidget(null_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.set_content(content=null_container, new_duarion=150)

    def get_content_widget(self) -> QWidget:
        return self.imported_content