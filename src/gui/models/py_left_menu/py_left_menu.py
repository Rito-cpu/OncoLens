from functools import partial
from src.core.pyqt_core import *
from src.core.image_functions import *
from .py_left_menu_button import PyLeftMenuButton
from .py_div import PyDiv

# PY LEFT MENU
class PyLeftMenu(QWidget):
    # SIGNALS
    clicked = pyqtSignal(QWidget)   # (object)
    released = pyqtSignal(QWidget)  # (object)

    def __init__(
        self,
        parent = None,
        app_parent = None,
        dark_one = "#1b1e23",
        dark_three = "#21252d",
        dark_four = "#272c36",
        bg_one = "#2c313c",
        icon_color = "#c3ccdf",
        icon_color_hover = "#dce1ec",
        icon_color_pressed = "#edf0f5",
        icon_color_active = "#f5f6f9",
        context_color = "#568af2",
        text_foreground = "#8a95aa",
        text_active = "#dce1ec",
        duration_time = 500,
        radius = 8,
        minimum_width = 50,
        maximum_width = 240,
        icon_path = "icon_arrow_right.svg",
        icon_path_close = "icon_menu_close.svg",
        toggle_text = "Hide Menu",
        toggle_tooltip = "Show menu"
    ):
        super().__init__()

        # PROPERTIES
        self._dark_one = dark_one
        self._dark_three = dark_three
        self._dark_four = dark_four
        self._bg_one = bg_one
        self._icon_color = icon_color
        self._icon_color_hover = icon_color_hover
        self._icon_color_pressed = icon_color_pressed
        self._icon_color_active = icon_color_active
        self._context_color = context_color
        self._text_foreground = text_foreground
        self._text_active = text_active
        self._duration_time = duration_time
        self._radius = radius
        self._minimum_width = minimum_width
        self._maximum_width = maximum_width
        self._icon_path = Functions.set_svg_icon(icon_path)
        self._icon_path_close = Functions.set_svg_icon(icon_path_close)

        # SET PARENT
        self._parent = parent
        self._app_parent = app_parent

        # SETUP WIDGETS
        self.setup_ui()

        # SET BG COLOR
        self.bg.setStyleSheet(f"background: {dark_one}; border-radius: {radius};")

        # TOGGLE BUTTON AND DIV MENUS
        self.toggle_button = PyLeftMenuButton(
            app_parent,
            text = toggle_text,
            tooltip_text = toggle_tooltip,
            dark_one = self._dark_one,
            dark_three = self._dark_three,      # change self._dark_three to choose the bg of the hide tab
            dark_four = self._dark_four,
            bg_one = self._bg_one,
            icon_color = self._icon_color,
            icon_color_hover = self._icon_color_active,
            icon_color_pressed = self._icon_color_pressed,
            icon_color_active = self._icon_color_active,
            context_color = self._context_color,
            text_foreground = self._text_foreground,
            text_active = self._text_active,
            icon_path = icon_path
        )
        self.toggle_button.clicked.connect(self.toggle_animation)
        self.div_top = PyDiv(dark_four)

        # ADD TO TOP LAYOUT
        self.top_layout.addWidget(self.toggle_button)
        self.top_layout.addWidget(self.div_top)

        # ADD TO BOTTOM LAYOUT
        self.div_bottom = PyDiv(dark_four)
        self.div_bottom.hide()
        self.bottom_layout.addWidget(self.div_bottom)

        self._menu_list = []

    # ADD BUTTONS TO LEFT MENU
    # Add btns and emit signals
    def add_menus(self, parameters):
        if parameters != None:
            for parameter in parameters:
                _bttn_icon = parameter['bttn_icon']
                _bttn_id = parameter['bttn_id']
                _bttn_text = parameter['bttn_text']
                _bttn_tooltip = parameter['bttn_tooltip']
                _show_top = parameter['show_top']
                _is_active = parameter['is_active']

                # if _btn_id in ["btn_add_user", "btn_new_file", "btn_open_file", "btn_save", "btn_info", "btn_settings"]:
                #     continue

                self.menu = PyLeftMenuButton(
                    self._app_parent,
                    text = _bttn_text,
                    bttn_id = _bttn_id,
                    tooltip_text = _bttn_tooltip,
                    dark_one = self._dark_one,
                    dark_three = self._dark_three,
                    dark_four = self._dark_four,
                    bg_one = self._bg_one,
                    icon_color = self._icon_color,
                    icon_color_hover = self._icon_color_active,
                    icon_color_pressed = self._icon_color_pressed,
                    icon_color_active = self._icon_color_active,
                    context_color = self._context_color,
                    text_foreground = self._text_foreground,
                    text_active = self._text_active,
                    icon_path = _bttn_icon,
                    is_active = _is_active
                )
                self._menu_list.append(self.menu)
                # self.menu.clicked.connect(self.btn_clicked)
                # self.menu.released.connect(self.btn_released)
                self._menu_list[-1].clicked.connect(partial(self.menu_bttn_clicked, self._menu_list[-1]))
                self._menu_list[-1].released.connect(partial(self.menu_bttn_released, self._menu_list[-1]))

                # ADD TO LAYOUT
                if _show_top:
                    self.top_layout.addWidget(self.menu)
                else:
                    self.div_bottom.show()
                    self.bottom_layout.addWidget(self.menu)

    # LEFT MENU EMIT SIGNALS
    def menu_bttn_clicked(self, wid):     # (self)
        # self.clicked.emit(self.menu)
        self.clicked.emit(wid)

    def menu_bttn_released(self, wid):    # (self)
        # self.released.emit(self.menu)
        self.released.emit(wid)

    # EXPAND / RETRACT LEF MENU
    def toggle_animation(self):
        # CREATE ANIMATION
        self.animation = QPropertyAnimation(self._parent, b"minimumWidth")
        self.animation.stop()
        if self.width() == self._minimum_width:
            self.animation.setStartValue(self.width())
            self.animation.setEndValue(self._maximum_width)
            self.toggle_button.set_active_toggle(True)
            self.toggle_button.set_icon(self._icon_path_close)
        else:
            self.animation.setStartValue(self.width())
            self.animation.setEndValue(self._minimum_width)
            self.toggle_button.set_active_toggle(False)
            self.toggle_button.set_icon(self._icon_path)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.setDuration(self._duration_time)
        self.animation.start()

    # SELECT ONLY ONE BTN
    def select_only_one(self, widget: str):
        for btn in self.findChildren(QPushButton):
            if btn.objectName() == widget:
                btn.set_active(True)
            else:
                btn.set_active(False)

    # SELECT ONLY ONE TAB BTN
    def select_only_one_tab(self, widget: str):
        for btn in self.findChildren(QPushButton):
            if btn.objectName() == widget:
                btn.set_active_tab(True)
            else:
                btn.set_active_tab(False)

    # DESELECT ALL BTNs
    def deselect_all(self):
        for btn in self.findChildren(QPushButton):
            btn.set_active(False)

    # DESELECT ALL TAB BTNs
    def deselect_all_tab(self):
        for btn in self.findChildren(QPushButton):
            btn.set_active_tab(False)

    # SETUP APP
    def setup_ui(self):
        # ADD MENU LAYOUT
        self.left_menu_layout = QVBoxLayout(self)
        self.left_menu_layout.setContentsMargins(0,0,0,0)

        # ADD BG
        self.bg = QFrame()

        # TOP FRAME
        self.top_frame = QFrame()

        # BOTTOM FRAME
        self.bottom_frame = QFrame()

        # ADD LAYOUTS
        self._layout = QVBoxLayout(self.bg)
        self._layout.setContentsMargins(0,0,0,0)

        # TOP LAYOUT
        self.top_layout = QVBoxLayout(self.top_frame)
        self.top_layout.setContentsMargins(0,0,0,0)
        self.top_layout.setSpacing(1)

        # BOTTOM LAYOUT
        self.bottom_layout = QVBoxLayout(self.bottom_frame)
        self.bottom_layout.setContentsMargins(0,0,0,8)
        self.bottom_layout.setSpacing(1)

        # ADD TOP AND BOTTOM FRAME
        self._layout.addWidget(self.top_frame, 0, Qt.AlignmentFlag.AlignTop)
        self._layout.addWidget(self.bottom_frame, 0, Qt.AlignmentFlag.AlignBottom)

        # ADD BG TO LAYOUT
        self.left_menu_layout.addWidget(self.bg)
