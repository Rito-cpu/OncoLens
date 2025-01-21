from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.gui.models.qt_combo_widget import QtComboBox


class QtModelSelectionArea(QWidget):
    def __init__(
        self,
        font_size: int = 13,
        parent=None
    ):
        super().__init__()
        if parent is not None:
            self.setParent(parent)

        themes = Themes()
        self.themes = themes.items

        self._font_size = font_size
        self.collapsed_description = """Section to change which mathematical model to display in settings and use for modeling."""
        self.expanded_description = """"""
        
        self._setup_widget()

        self.model_combo_box.currentTextChanged.connect(self.model_changed)

    def _setup_widget(self):
        outer_frame = QFrame(self)
        outer_frame.setObjectName("outer_frame")
        outer_frame.setFrameShape(QFrame.Shape.NoFrame)
        outer_frame.setFrameShadow(QFrame.Shadow.Plain)
        outer_frame.setStyleSheet(f"QFrame#outer_frame{{background: {self.themes['app_color']['white']}; border-radius: 8px;}}")

        model_area = QFrame(outer_frame)
        model_area.setObjectName("model_area")
        model_area.setFrameShape(QFrame.Shape.NoFrame)
        model_area.setFrameShadow(QFrame.Shadow.Plain)

        selection_label = QLabel(model_area)
        selection_label.setObjectName("selection_label")
        selection_label.setText("Mathematical Model:")
        selection_label.setStyleSheet(f'font-size: {self._font_size}px; color: {self.themes["app_color"]["dark_one"]}; font-weight: bold;')
        selection_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.model_combo_box = QtComboBox(
            bg_color=self.themes["app_color"]["dark_three"],
            text_color=self.themes["app_color"]["white"],
            font_size=14,
            parent=model_area
        )
        self.model_combo_box.setObjectName('model_combo_box')
        # TODO: Add model class names here after finalizing model classes in src.core
        self.model_combo_box.addItems(['GDRS', 'SR', 'Test 3'])
        self.model_combo_box.setCurrentIndex(0)
        self.model_combo_box.setFixedHeight(30)
        self.model_combo_box.setMinimumWidth(150)

        model_area_layout = QHBoxLayout(model_area)
        model_area_layout.setObjectName("model_area_layout")
        model_area_layout.setContentsMargins(0, 0, 0, 0)
        model_area_layout.setSpacing(7)
        model_area_layout.addWidget(selection_label, alignment=Qt.AlignmentFlag.AlignCenter)
        model_area_layout.addWidget(self.model_combo_box, alignment=Qt.AlignmentFlag.AlignCenter)
        model_area.setMaximumWidth(model_area_layout.sizeHint().width()+5)

        description_frame = QFrame(outer_frame)
        description_frame.setObjectName("description_frame")
        description_frame.setFrameShape(QFrame.Shape.NoFrame)
        description_frame.setFrameShadow(QFrame.Shadow.Plain)
        description_frame.setStyleSheet(f"QFrame#description_frame{{border: 1px solid black; border-radius: 8px;}}")
        description_frame.setMinimumWidth(400)
        #description_frame.setMaximumWidth(700)

        helper_label_frame = QFrame(description_frame)
        helper_label_frame.setObjectName("helper_label_frame")
        helper_label_frame.setFrameShape(QFrame.Shape.NoFrame)
        helper_label_frame.setFrameShadow(QFrame.Shadow.Plain)

        helper_label = QLabel(helper_label_frame)
        helper_label.setObjectName("helper_label")
        helper_label.setText("You Have Selected:")
        helper_label.setStyleSheet(f"font-size: {self._font_size-1}px; color: {self.themes['app_color']['dark_one']};")
        helper_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._dynamic_model_label = QLabel(helper_label_frame)
        self._dynamic_model_label.setObjectName("dynamic_model_label")
        self._dynamic_model_label.setStyleSheet(f"font-size: {self._font_size-1}px; color: {self.themes['app_color']['dark_one']}; font-weight: bold;")
        self._dynamic_model_label.setText(self.model_combo_box.currentText())
        self._dynamic_model_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        helper_label_layout = QHBoxLayout(helper_label_frame)
        helper_label_layout.setObjectName("helper_label_layout")
        helper_label_layout.setContentsMargins(0, 0, 0, 0)
        helper_label_layout.setSpacing(7)
        helper_label_layout.addWidget(helper_label, alignment=Qt.AlignmentFlag.AlignCenter)
        helper_label_layout.addWidget(self._dynamic_model_label, alignment=Qt.AlignmentFlag.AlignCenter)
        helper_label_frame.setMaximumWidth(helper_label_layout.sizeHint().width()+5)

        description_area = QTextEdit(description_frame)
        description_area.setObjectName("description_area")
        description_area.setText("This is a test description. The model class will contain a description variable that will be retrieved and placed here when ready.")
        description_area.setReadOnly(True)
        description_area.setStyleSheet(f"font-size: {self._font_size-1}px; color: {self.themes['app_color']['text_description']};")
        description_area.setMinimumWidth(400)
        description_area.setAlignment(Qt.AlignmentFlag.AlignCenter)

        description_layout = QVBoxLayout(description_frame)
        description_layout.setObjectName("description_layout")
        description_layout.setContentsMargins(10, 10, 10, 10)
        description_layout.setSpacing(7)
        description_layout.addWidget(helper_label_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        description_layout.addWidget(description_area, alignment=Qt.AlignmentFlag.AlignCenter)

        outer_frame_layout = QVBoxLayout(outer_frame)
        outer_frame_layout.setObjectName("outer_frame_layout")
        outer_frame_layout.setContentsMargins(65, 10, 65, 10)
        outer_frame_layout.addWidget(model_area, alignment=Qt.AlignmentFlag.AlignCenter)
        outer_frame_layout.addWidget(description_frame)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(outer_frame)

    def model_changed(self):
        self._dynamic_model_label.setText(self.model_combo_box.currentText())

    def get_collapsed_description(self):
        return self.collapsed_description
    
    def get_expanded_description(self):
        return self.expanded_description
