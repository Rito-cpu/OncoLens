import os
import pathlib

from src.core.pyqt_core import *
from src.core.app_config import IMG_RSC_PATH
from src.gui.models.qt_line_button.qt_custom_line_edit import EnhancedLineEdit
from src.gui.models.qt_line_button.styles import *


class QtButtonLineEdit(QGroupBox):
    button_clicked = pyqtSignal(bool)
    entry_changed = pyqtSignal(str)

    def __init__(
            self,
            title: str,
            title_size: int=15,
            text_size: int=13,
            title_color: str="white",
            color_one: str="black",
            color_two: str="#c8c8c8",
            color_three: str = "white",
            border_color: str="#1ee16c",
            border_radius: int=8,
            top_margin: int=15,
            bg: str="white",
            left_spacing: int=14,
            mode: str = "folder",
            parent=None
        ):
        super(QtButtonLineEdit, self).__init__()

        if parent != None:
            self.setParent(parent)

        self._title_size = title_size
        self._text_size = text_size
        self._title_color = title_color
        self._color_one = color_one
        self._color_two = color_two
        self._color_three = color_three
        self._border_color = border_color
        self._border_radius = border_radius
        self._top_margin = top_margin
        self._bg = bg
        self._left_spacing = left_spacing
        self._mode = mode

        self.setTitle(title)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # *****************************
        # **** Create Image Pixmap ****
        # *****************************
        _default_icon = "downloads/openFileIcon_default.png"
        _pressed_icon = "downloads/openFileIcon_pressed.png"
        self._icon_default = QPixmap(os.path.abspath(os.path.join(IMG_RSC_PATH, _default_icon)))
        self._icon_pressed = QPixmap(os.path.abspath(os.path.join(IMG_RSC_PATH, _pressed_icon)))

        # **** Setup widget ****
        self.setup_widget()

        # *************************
        # **** Connect Signals ****
        # *************************
        self.enhanced_line_edit.textChanged.connect(self.emit_text_entry)
        self.image_bttn.pressed.connect(self._image_pressed)
        self.image_bttn.released.connect(self._image_released)
        self.image_bttn.clicked.connect(self.button_clicked.emit)      # Link signals to act as an entire button
        # self.image_bttn.clicked.connect(self._initiate_excel_dialog)
        self.image_bttn.clicked.connect(self._initiate_file_dialog)

    def setup_widget(self):
        # ****************************************
        # **** Create Button Line Edit Widget ****
        # ****************************************
        self.enhanced_line_edit = EnhancedLineEdit(self)
        self.enhanced_line_edit.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.enhanced_line_edit.setFrame(QFrame.Shape.NoFrame)
        self.enhanced_line_edit.setPlaceholderText("Type in Valid File Path")
        self.enhanced_line_edit.setCursor(Qt.CursorShape.IBeamCursor)

        self.image_bttn = QToolButton(self.enhanced_line_edit)
        self.image_bttn.setIcon(QIcon(self._icon_default))
        self.image_bttn.setIconSize(QSize(19, 19))
        self.image_bttn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.image_bttn.setStyleSheet("border: none; padding: 0px; background: transparent;")

        # *******************************
        # **** Set Sizing for Widget ****
        # *******************************
        frame_width = self.enhanced_line_edit.style().pixelMetric(QStyle.PixelMetric.PM_DefaultFrameWidth)
        bttn_size = self.image_bttn.sizeHint()

        right_padding = bttn_size.width() + frame_width + 10
        minimum_width = max(self.enhanced_line_edit.minimumSizeHint().width(), bttn_size.width() + frame_width * 2 + 2)
        minimum_height = max(self.enhanced_line_edit.minimumSizeHint().height(), bttn_size.height() + frame_width * 2 + 2)
        self.enhanced_line_edit.setMinimumSize(minimum_width, minimum_height)

        # ***********************************
        # **** Create Styles for Widgets ****
        # ***********************************
        custom_focus_style = focused_template.format(
            _title_size=self._title_size,
            _text_size=self._text_size,
            _title_color=self._title_color,
            _color_one=self._color_one,
            _color_three=self._color_three,
            _border_radius=self._border_radius,
            _top_margin=self._top_margin,
            _bg=self._bg,
            _left_spacing=self._left_spacing,
            _right_padding=right_padding
        )

        custom_unfocus_style = unfocused_template.format(
            _title_size=self._title_size,
            _text_size=self._text_size,
            _color_two=self._color_two,
            _border_radius=self._border_radius,
            _top_margin=self._top_margin,
            _left_spacing=self._left_spacing,
            _right_padding=right_padding
        )

        self.setStyleSheet(custom_focus_style)
        self.enhanced_line_edit.import_sheets(custom_focus_style, custom_unfocus_style)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(7, 2, 0, 2)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.enhanced_line_edit)

    def _image_pressed(self):
        self.image_bttn.setIcon(QIcon(self._icon_pressed))

    def _image_released(self):
        self.image_bttn.setIcon(QIcon(self._icon_default))

    def clear_text(self):
        self.enhanced_line_edit.clear()

    def emit_text_entry(self):
        self.entry_changed.emit(self.enhanced_line_edit.text())

    def text(self):
        return self.enhanced_line_edit.text()

    def set_text(self, text: str):
        self.enhanced_line_edit.setText(text)

    def resizeEvent(self, event):
        button_size = self.image_bttn.sizeHint()
        frame_width = self.enhanced_line_edit.style().pixelMetric(QStyle.PixelMetric.PM_DefaultFrameWidth)

        move_width = int(self.enhanced_line_edit.rect().right() - frame_width - button_size.width() - 5)
        move_height = int((self.enhanced_line_edit.rect().bottom() + 1 - button_size.height()) / 2)
        self.image_bttn.move(move_width, move_height)
        super().resizeEvent(event)

    def _initiate_excel_dialog(self):
        """
        File search dialog box that returns a user-selected path.

        :return:
        None
        """
        home = str(pathlib.Path.home())
        file_filter = 'Data File (*.xlsx);; Excel File(*.xlsx)'

        file_name, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a data file',
            directory=home,
            filter=file_filter,
            initialFilter='Excel File (*.xlsx)'
        )

        self.enhanced_line_edit.setText(file_name)

    def _initiate_file_dialog(self):
        """
        File search dialog that returns a user-selected path.

        :return:
        None
        """
        home = str(pathlib.Path.home())

        dialog = QFileDialog(self)
        dialog.setDirectory(home)
        if self._mode == "folder":
            dialog.setWindowTitle("Select a Directory")
            dialog.setFileMode(QFileDialog.FileMode.Directory)
            dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)
        else:
            dialog.setWindowTitle("Select a File")
            dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
            dialog.setNameFilter("All Files (*)")

        if dialog.exec():
            selected_path = dialog.selectedFiles()[0]
            self.enhanced_line_edit.setText(selected_path)

        #folder_name = QFileDialog.getExistingDirectory(
        #    parent=self,
        #    caption='Select a directory',
        #    directory=home,
        #)

        #self.enhanced_line_edit.setText(folder_name)
