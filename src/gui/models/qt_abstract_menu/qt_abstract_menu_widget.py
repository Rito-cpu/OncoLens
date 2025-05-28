import pathlib

from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from .qt_abstract_settings import QtAbstractSettings
from .qt_abstract_file import QtAbstractFileEntry
from .qt_abstract_plot import QtAbstractPlot


class QtAbstractMenu(QWidget):
    menu_changed = pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super().__init__(parent)

        if parent is not None:
            self.setParent(parent)

        themes = Themes()
        self.themes = themes.items

        self._setup_widget()
        self.stacked_menu.currentChanged.connect(self.emit_menu)
        self.stacked_menu.currentChanged.connect(self.change_title)
        #self._abstract_file_page.submit_data_bttn.clicked.connect(self.set_settings_page)
        self._abstract_file_page.change_scene.connect(self.file_submitted)

    def _setup_widget(self):
        self.settings_title = QLabel(self)
        self.settings_title.setObjectName('settings_title')
        self.settings_title.setText('')
        self.settings_title.setStyleSheet('font-size: 18px; font-weight: bold;')
        self.settings_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        overall_frame = QFrame(self)
        overall_frame.setObjectName('overall_Frame')
        overall_frame.setFrameShape(QFrame.Shape.NoFrame)
        overall_frame.setFrameShadow(QFrame.Shadow.Plain)

        self.stacked_menu = QStackedWidget(overall_frame)
        self._abstract_file_page = QtAbstractFileEntry(parent=self.stacked_menu)
        self._abstract_file_page.setObjectName('abstract_file_page')
        self._abstract_settings_page = QtAbstractSettings(parent=self.stacked_menu)
        self._abstract_settings_page.setObjectName('abstract_settings_page')
        self._abstract_plot_page = QtAbstractPlot(parent=self.stacked_menu)
        self._abstract_plot_page.setObjectName('abstract_plot_page')

        self.stacked_menu.setObjectName('stacked_menu')
        self.stacked_menu.insertWidget(0, self._abstract_file_page)
        self.stacked_menu.insertWidget(1, self._abstract_settings_page)
        self.stacked_menu.insertWidget(2, self._abstract_plot_page)
        self.stacked_menu.setCurrentIndex(0)
        self.settings_title.setText(self.stacked_menu.currentWidget().title)

        overall_layout = QVBoxLayout(overall_frame)
        overall_layout.setSpacing(15)
        overall_layout.setContentsMargins(5, 5, 5, 5)
        overall_layout.addWidget(self.stacked_menu)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.settings_title)
        main_layout.addWidget(overall_frame)

    def set_settings_page(self):
        self.stacked_menu.setCurrentWidget(self._abstract_settings_page)

    def set_file_page(self):
        self.stacked_menu.setCurrentWidget(self._abstract_file_page)

    def set_plot_page(self):
        self.stacked_menu.setCurrentWidget(self._abstract_plot_page)

    def file_submitted(self, file_settings: dict):
        self._abstract_settings_page.import_info(file_settings)
        self.set_settings_page()

    def emit_menu(self):
        self.menu_changed.emit(self.stacked_menu.currentWidget())

    def current_widget(self):
        return self.stacked_menu.currentWidget()

    def change_title(self):
        current_wid = self.stacked_menu.currentWidget()
        self.settings_title.setText(current_wid.title)
