from src.core.pyqt_core import *
from src.core.image_functions import Functions
from src.core.json.json_themes import Themes
from src.gui.models.qt_clickable_icon import QtMenuIcon
from src.gui.models.qt_clickable_label import QtClickableLabel


class QtSectionalWidget(QWidget):
    def __init__(
        self,
        section_title: str,
        icon_name: str,
        collapsed_info: str,
        expanded_info: str,
        title_font: int = 16,
        body_font: int = 12,
        icon_size: int = 70,
        custom_expanded_height: int = 200,
        use_custom_widget: QWidget = None,
        parent=None
    ):
        super().__init__(parent)

        if parent is not None:
            self.parent = parent

        themes = Themes()
        self.themes = themes.items

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self._section_title = section_title
        self._icon_path = Functions.set_svg_icon(icon_name)
        self._collapsed_info = collapsed_info
        self._expanded_info = expanded_info
        self._title_font = title_font
        self._body_font = body_font
        self._icon_size = icon_size
        self._custom_height = custom_expanded_height
        self._use_custom_widget = use_custom_widget
        self.is_expanded = False
        self.animation_duration = 400

        self._setup_widget()

        self.title_label.clicked.connect(self.title_clicked)
        self.section_icon.clicked.connect(self.toggle_collapsed)

    def _setup_widget(self):
        self.outermost_frame = QFrame(self)
        self.outermost_frame.setObjectName('outermost_frame')
        self.outermost_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.outermost_frame.setFrameShadow(QFrame.Shadow.Plain)
        self.outermost_frame.setStyleSheet(f"""
            QFrame#outermost_frame {{
                border: 2px solid {self.themes['app_color']['dark_three']};
                border-radius: 10px;
                background: {self.themes['app_color']['bg_two']};
            }}
        """)

        icon_frame = QFrame(self.outermost_frame)
        icon_frame.setObjectName('icon_frame')
        icon_frame.setFrameShape(QFrame.Shape.NoFrame)
        icon_frame.setFrameShadow(QFrame.Shadow.Plain)

        # orange color: #f4ac3c
        # Green: #1ee16c
        self.section_icon = QtMenuIcon(
            icon_name=self._icon_path,
            icon_size=self._icon_size,
            color="#f4ac3c",
            set_checkable=True,
            parent=self.outermost_frame
        )
        self.section_icon.setObjectName('sectional_icon')

        icon_layout = QVBoxLayout(icon_frame)
        icon_layout.setObjectName('icon_layout')
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.addWidget(self.section_icon, alignment=Qt.AlignmentFlag.AlignCenter)

        right_side_frame = QFrame(self.outermost_frame)
        right_side_frame.setObjectName('right_side_frame')
        right_side_frame.setFrameShape(QFrame.Shape.NoFrame)
        right_side_frame.setFrameShadow(QFrame.Shadow.Plain)

        self.title_label = QtClickableLabel(
            text=self._section_title,
            font_size=self._title_font,
            bold=True,
            hyperlink_label=False,
            parent=right_side_frame
        )

        self.info_area_stack = QStackedWidget(right_side_frame)
        self.info_area_stack.setObjectName('info_area_stack')
        #self.info_area_stack.setStyleSheet('border: 2px solid black;')
        self.info_area_stack.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.collapsed_text_area = QTextEdit(self.info_area_stack)
        self.collapsed_text_area.setObjectName('collapsed_info')
        self.collapsed_text_area.setMinimumWidth(325)
        self.collapsed_text_area.setReadOnly(True)
        self.collapsed_text_area.setText(self._collapsed_info)
        self.collapsed_text_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.collapsed_text_area.setStyleSheet(f'border: none; background: {self.themes["app_color"]["bg_two"]}; font-size: {self._body_font}px;')
        self.adjust_collapsed_widget_height()

        self.expanded_widget_area = QWidget(self.info_area_stack)
        self.expanded_widget_area.setMinimumHeight(self._custom_height)
        expanded_layout = QVBoxLayout(self.expanded_widget_area)
        expanded_layout.setContentsMargins(65, 0, 65, 10)
        if self._use_custom_widget is not None:
            expanded_layout.addWidget(self._use_custom_widget)
        else:
            expanded_label = QLabel(self.expanded_widget_area)
            expanded_label.setText(self._expanded_info)
            expanded_layout.addWidget(expanded_label)
        self.stack_expanded_height = self.expanded_widget_area.size().height()

        self.info_area_stack.addWidget(self.collapsed_text_area)
        self.info_area_stack.addWidget(self.expanded_widget_area)
        self.info_area_stack.setCurrentWidget(self.collapsed_text_area)
        self.set_stack_widget_height(self.is_expanded)

        right_side_layout = QVBoxLayout(right_side_frame)
        right_side_layout.setObjectName("right_side_layout")
        right_side_layout.setContentsMargins(0, 0, 0, 0)
        right_side_layout.setSpacing(10)
        right_side_layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        right_side_layout.addWidget(self.info_area_stack)
        # right_side_layout.addStretch(1)

        outermost_frame_layout = QHBoxLayout(self.outermost_frame)
        outermost_frame_layout.setContentsMargins(25, 10, 25, 10)
        outermost_frame_layout.setSpacing(18)
        outermost_frame_layout.addWidget(icon_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        outermost_frame_layout.addWidget(right_side_frame)

        #grid_filler = QWidget()
        #outermost_frame_layout = QGridLayout(self.outermost_frame)
        #outermost_frame_layout.setObjectName('outermost_frame_layout')
        #outermost_frame_layout.setContentsMargins(5, 15, 30, 15)
        #outermost_frame_layout.setSpacing(15)
        #outermost_frame_layout.addWidget(self.section_icon, 0, 0, 3, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        #outermost_frame_layout.addWidget(title_label, 0, 1, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        #outermost_frame_layout.addWidget(self.info_area_stack, 1, 1, 2, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        #outermost_frame_layout.addWidget(grid_filler, 2, 3, 1, 1)

        main_layout = QVBoxLayout(self)
        main_layout.setObjectName('main_layout')
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.outermost_frame)

        # --- Create collapsible animation settings ---
        self.collapsed_height = self.sizeHint().height() + 4
        self.expanded_height = self.collapsed_height + self.expanded_widget_area.size().height()

        self.toggle_animation = QParallelAnimationGroup()
        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"minimumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self, b"maximumHeight"))
        self.toggle_animation.addAnimation(QPropertyAnimation(self.outermost_frame, b"maximumHeight"))

        start_height = self.collapsed_height if not self.is_expanded else self.expanded_height
        end_height = self.expanded_height if not self.is_expanded else self.collapsed_height

        for index in range(0, self.toggle_animation.animationCount() - 1):
            section_animation: QPropertyAnimation
            section_animation = self.toggle_animation.animationAt(index)
            section_animation.setDuration(self.animation_duration)
            section_animation.setStartValue(start_height)
            section_animation.setEndValue(end_height)
        
        content_animation: QPropertyAnimation
        content_animation = self.toggle_animation.animationAt(self.toggle_animation.animationCount() - 1)
        content_animation.setDuration(self.animation_duration)
        content_animation.setStartValue(start_height)
        content_animation.setEndValue(end_height)

        #self.setMinimumWidth(self.sizeHint().width() * 2)
        self.setMaximumWidth(self.sizeHint().width() * 2)

    def title_clicked(self):
        icon_pos = self.section_icon.pos()
        event = QMouseEvent(QEvent.Type.MouseButtonPress, QPointF(icon_pos), Qt.MouseButton.LeftButton, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
        self.section_icon.mousePressEvent(event)

    def toggle_collapsed(self):
        # Set the current index first before starting the animation
        self.is_expanded = not self.is_expanded

        if self.is_expanded:
            self.info_area_stack.setCurrentWidget(self.expanded_widget_area)
            self.toggle_animation.setDirection(QAbstractAnimation.Direction.Forward)
            self.section_icon.resize_icon(self._icon_size*1.4)
        else:
            self.info_area_stack.setCurrentWidget(self.collapsed_text_area)
            self.toggle_animation.setDirection(QAbstractAnimation.Direction.Backward)
            self.section_icon.resize_icon(self._icon_size)
        self.set_stack_widget_height(self.is_expanded)

        # Start the animation
        self.toggle_animation.start()

    def set_stack_widget_height(self, is_expanded: bool):
        if is_expanded:
            self.info_area_stack.setFixedHeight(self.stack_expanded_height)
        else:
            self.info_area_stack.setFixedHeight(self.stack_minimized_height)

    def adjust_collapsed_widget_height(self):
        doc_height = self.collapsed_text_area.document().size().height()
        margin_top = self.collapsed_text_area.contentsMargins().top()
        margin_bottom = self.collapsed_text_area.contentsMargins().bottom()

        self.collapsed_text_area.setFixedHeight(doc_height + margin_top + margin_bottom + 4)
        self.stack_minimized_height = self.collapsed_text_area.size().height()+4

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Set custom color, font, or other properties if needed
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        #painter.setBrush(QColor(200, 200, 255))  # Set a background color
        #painter.drawRoundedRect(self.rect(), 10, 10)  # Draw a rounded rectangle as the background

        # Draw text in the center
        #painter.setPen(QColor(50, 50, 50))
        #font = QFont("Arial", 12, QFont.Weight.Bold)
        #painter.setFont(font)
        #painter.drawText(self.rect(), "Custom Widget", alignment=Qt.AlignmentFlag.AlignCenter)
