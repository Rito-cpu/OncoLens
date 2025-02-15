from functools import partial

from src.core.pyqt_core import *
from src.core.image_functions import Functions
from src.core.json.json_settings import Settings
from .py_div import PyDiv
from .py_title_button import PyTitleButton

# GLOBALS
_is_maximized = False
_old_size = QSize()

# PY TITLE BAR
# Top bar with move application, maximize, restore, minimize,
# close buttons and extra buttons
class PyTitleBar(QWidget):
    # SIGNALS
    clicked = pyqtSignal(QWidget)   # (object)
    released = pyqtSignal(QWidget)  # (object)

    def __init__(
        self,
        parent,
        app_parent,
        logo_image = "logo_top_100x22.svg",
        logo_width = 100,
        buttons = None,
        dark_one = "#1b1e23",
        bg_color = "#343b48",
        div_color = "#3c4454",
        bttn_bg_color = "#343b48",
        bttn_bg_color_hover = "#3c4454",
        bttn_bg_color_pressed = "#2c313c",
        icon_color = "#c3ccdf",
        icon_color_hover = "#dce1ec",
        icon_color_pressed = "#edf0f5",
        icon_color_active = "#f5f6f9",
        context_color = "#6c99f4",
        text_foreground = "#8a95aa",
        radius = 8,
        font_family = "Segoe UI",
        title_size = 10,
        is_custom_title_bar = True,
    ):
        super().__init__()

        settings = Settings()
        self.settings = settings.items

        # PARAMETERS
        self._logo_image = logo_image
        self._dark_one = dark_one
        self._bg_color = bg_color
        self._div_color = div_color
        self._parent = parent
        self._app_parent = app_parent
        self._bttn_bg_color = bttn_bg_color
        self._bttn_bg_color_hover = bttn_bg_color_hover
        self._bttn_bg_color_pressed = bttn_bg_color_pressed
        self._context_color = context_color
        self._icon_color = icon_color
        self._icon_color_hover = icon_color_hover
        self._icon_color_pressed = icon_color_pressed
        self._icon_color_active = icon_color_active
        self._font_family = font_family
        self._title_size = title_size
        self._text_foreground = text_foreground
        self._is_custom_title_bar = is_custom_title_bar

        # SETUP UI
        self.setup_ui()

        # ADD BG COLOR
        self.bg.setStyleSheet(f"background-color: {bg_color}; border-radius: {radius}px;")

        # SET LOGO AND WIDTH
        self.top_logo.setMinimumWidth(logo_width)
        self.top_logo.setMaximumWidth(logo_width)
        #self.top_logo.setPixmap(Functions.set_svg_image(logo_image))

        # MOVE WINDOW / MAXIMIZE / RESTORE
        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if parent.isMaximized():
                self.maximize_restore()
                #self.resize(_old_size)
                curso_x = parent.pos().x()
                curso_y = event.globalPosition().y() - QCursor.pos().y()
                parent.move(curso_x, curso_y)
            # MOVE WINDOW
            if event.buttons() == Qt.MouseButton.LeftButton:
                parent.move(parent.pos() + event.globalPosition().toPoint() - parent.dragPos)
                parent.dragPos = event.globalPosition().toPoint()
                event.accept()

        # MOVE APP WIDGETS
        if is_custom_title_bar:
            self.top_logo.mouseMoveEvent = moveWindow
            self.div_1.mouseMoveEvent = moveWindow
            self.title_label.mouseMoveEvent = moveWindow
            self.div_2.mouseMoveEvent = moveWindow
            self.div_3.mouseMoveEvent = moveWindow

        # MAXIMIZE / RESTORE
        if is_custom_title_bar:
            self.top_logo.mouseDoubleClickEvent = self.maximize_restore
            self.div_1.mouseDoubleClickEvent = self.maximize_restore
            self.title_label.mouseDoubleClickEvent = self.maximize_restore
            self.div_2.mouseDoubleClickEvent = self.maximize_restore

        # ADD WIDGETS TO TITLE BAR
        # self.bg_layout.addWidget(self.top_logo)
        # self.bg_layout.addWidget(self.div_1)
        self.bg_layout.addWidget(self.title_label) #, alignment=Qt.AlignmentFlag.AlignCenter)
        self.bg_layout.addWidget(self.div_2)

        # ADD BUTTONS BUTTONS
        # Functions
        self.minimize_button.released.connect(lambda: parent.showMinimized())
        self.maximize_restore_button.released.connect(lambda: self.maximize_restore())
        self.close_button.released.connect(lambda: parent.close())

        # Extra BTNs layout
        self.bg_layout.addLayout(self.custom_buttons_layout)

        # ADD Buttons
        if is_custom_title_bar:
            self.bg_layout.addWidget(self.minimize_button)
            self.bg_layout.addWidget(self.maximize_restore_button)
            self.bg_layout.addWidget(self.close_button)

        self._menu_list = []

    # ADD BUTTONS TO TITLE BAR
    # Add btns and emit signals
    def add_menus(self, parameters):
        if parameters != None and len(parameters) > 0:
            for parameter in parameters:
                _bttn_icon = Functions.set_svg_icon(parameter['bttn_icon'])
                _bttn_id = parameter['bttn_id']
                _bttn_tooltip = parameter['bttn_tooltip']
                _is_active = parameter['is_active']

                self.menu = PyTitleButton(
                    self._parent,
                    self._app_parent,
                    bttn_id = _bttn_id,
                    tooltip_text = _bttn_tooltip,
                    dark_one = self._dark_one,
                    bg_color = self._bg_color,
                    bg_color_hover = self._bttn_bg_color_hover,
                    bg_color_pressed = self._bttn_bg_color_pressed,
                    icon_color = self._icon_color,
                    icon_color_hover = self._icon_color_active,
                    icon_color_pressed = self._icon_color_pressed,
                    icon_color_active = self._icon_color_active,
                    context_color = self._context_color,
                    text_foreground = self._text_foreground,
                    icon_path = _bttn_icon,
                    is_active = _is_active
                )
                self._menu_list.append(self.menu)
                self._menu_list[-1].clicked.connect(partial(self.bar_bttn_clicked, self._menu_list[-1]))
                self._menu_list[-1].released.connect(partial(self.bar_bttn_released, self._menu_list[-1]))
                # self.menu.clicked.connect(self.btn_clicked)
                # self.menu.released.connect(self.btn_released)

                # ADD TO LAYOUT
                self.custom_buttons_layout.addWidget(self.menu)
                self.menu.setDisabled(True)

            # ADD DIV
            if self._is_custom_title_bar:
                self.custom_buttons_layout.addWidget(self.div_3)

    # TITLE BAR MENU EMIT SIGNALS
    def bar_bttn_clicked(self, wid):
        # self.clicked.emit(self.menu)
        self.clicked.emit(wid)

    def bar_bttn_released(self, wid):
        # self.released.emit(self.menu)
        self.released.emit(wid)

    # SET TITLE BAR TEXT
    def set_title(self, title):
        self.title_label.setText(title)

    # MAXIMIZE / RESTORE
    # maximize and restore parent window
    def maximize_restore(self, e = None):
        global _is_maximized
        global _old_size

        # CHANGE UI AND RESIZE GRIP
        def change_ui():
            if _is_maximized:
                self._parent.ui.central_widget_layout.setContentsMargins(0,0,0,0)
                self._parent.ui.window.set_stylesheet(border_radius = 0, border_size = 0)
                self.maximize_restore_button.set_icon(Functions.set_svg_icon("icon_restore.svg"))
            else:
                self._parent.ui.central_widget_layout.setContentsMargins(10,10,10,10)
                self._parent.ui.window.set_stylesheet(border_radius = 10, border_size = 2)
                self.maximize_restore_button.set_icon(Functions.set_svg_icon("icon_maximize.svg"))

        # CHECK EVENT
        if self._parent.isMaximized():
            _is_maximized = False
            self._parent.showNormal()
            change_ui()
        else:
            _is_maximized = True
            _old_size = QSize(self._parent.width(), self._parent.height())
            self._parent.showMaximized()
            change_ui()

    # SETUP APP
    def setup_ui(self):
        # ADD MENU LAYOUT
        self.title_bar_layout = QVBoxLayout(self)
        self.title_bar_layout.setContentsMargins(0,0,0,0)

        # ADD BG
        self.bg = QFrame()

        # ADD BG LAYOUT
        self.bg_layout = QHBoxLayout(self.bg)
        self.bg_layout.setContentsMargins(10,0,5,0)
        self.bg_layout.setSpacing(0)

        # DIVS
        self.div_1 = PyDiv(self._div_color)
        self.div_2 = PyDiv(self._div_color)
        self.div_3 = PyDiv(self._div_color)

        # LEFT FRAME WITH MOVE APP
        self.top_logo = QLabel()
        self.logo_svg = QSvgWidget()
        self.logo_svg.load(Functions.set_svg_image(self._logo_image))
        self.top_logo_layout = QVBoxLayout(self.top_logo)
        self.top_logo_layout.setContentsMargins(0,0,0,0)
        self.top_logo_layout.addWidget(self.logo_svg, Qt.AlignmentFlag.AlignCenter, Qt.AlignmentFlag.AlignCenter)

        # TITLE LABEL
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.title_label.setStyleSheet(f'font: {self._title_size}pt "{self._font_family}"')

        # CUSTOM BUTTONS LAYOUT
        self.custom_buttons_layout = QHBoxLayout()
        self.custom_buttons_layout.setContentsMargins(0,0,0,0)
        self.custom_buttons_layout.setSpacing(3)

        # MINIMIZE BUTTON
        self.minimize_button = PyTitleButton(
            self._parent,
            self._app_parent,
            tooltip_text = "Close app",
            dark_one = self._dark_one,
            bg_color = self._bttn_bg_color,
            bg_color_hover = self._bttn_bg_color_hover,
            bg_color_pressed = self._bttn_bg_color_pressed,
            icon_color = self._icon_color,
            icon_color_hover = self._icon_color_hover,
            icon_color_pressed = self._icon_color_pressed,
            icon_color_active = self._icon_color_active,
            context_color = self._context_color,
            text_foreground = self._text_foreground,
            radius = 6,
            icon_path = Functions.set_svg_icon("icon_minimize.svg")
        )

        # MAXIMIZE / RESTORE BUTTON
        self.maximize_restore_button = PyTitleButton(
            self._parent,
            self._app_parent,
            tooltip_text = "Maximize app",
            dark_one = self._dark_one,
            bg_color = self._bttn_bg_color,
            bg_color_hover = self._bttn_bg_color_hover,
            bg_color_pressed = self._bttn_bg_color_pressed,
            icon_color = self._icon_color,
            icon_color_hover = self._icon_color_hover,
            icon_color_pressed = self._icon_color_pressed,
            icon_color_active = self._icon_color_active,
            context_color = self._context_color,
            text_foreground = self._text_foreground,
            radius = 6,
            icon_path = Functions.set_svg_icon("icon_maximize.svg")
        )

        # CLOSE BUTTON
        self.close_button = PyTitleButton(
            self._parent,
            self._app_parent,
            tooltip_text = "Close app",
            dark_one = self._dark_one,
            bg_color = self._bttn_bg_color,
            bg_color_hover = self._bttn_bg_color_hover,
            bg_color_pressed = self._context_color,
            icon_color = self._icon_color,
            icon_color_hover = self._icon_color_hover,
            icon_color_pressed = self._icon_color_active,
            icon_color_active = self._icon_color_active,
            context_color = self._context_color,
            text_foreground = self._text_foreground,
            radius = 6,
            icon_path = Functions.set_svg_icon("icon_close.svg")
        )

        # ADD TO LAYOUT
        self.title_bar_layout.addWidget(self.bg)

    # Change Bar Title
    def change_title(self, new_title: str) -> None:
        self.title_label.setText(new_title)
