from src.core.pyqt_core import *
from .styles import *


class QtCircleProgressBar(QWidget):
    def __init__(self,
                title: str,
                border_radius_one: int=150,
                border_radius_two: int=135,
                non_progress_color: str="rgba(255, 0, 127, 0)",
                progress_color: str="rgba(85, 170, 255, 255)",
                color_three: str="rgba(77, 77, 127, 120)",
                bg_color_main: str="rgb(77, 77, 127)",
                text_color: str="#FFFFFF",
                msg_bg_color: str="rgb(93, 93, 154)",
                stop_one: float=0.749,
                stop_two: float=0.750,
                parent=None
                ) -> None:
        super().__init__()

        if parent != None:
            self.setParent(parent)

        self._title = title
        self._border_radius_one = border_radius_one
        self._border_radius_two = border_radius_two
        self._non_progress_color = non_progress_color
        self._progress_color = progress_color
        self._color_three = color_three
        self._bg_color_main = bg_color_main
        self._text_color = text_color
        self._msg_bg_color = msg_bg_color
        self._stop_one = stop_one
        self._stop_two = stop_two

        self.setup_widget()

    def setup_widget(self):
        progress_bar_base = QFrame(self)
        progress_bar_base.setObjectName(u"progress_base")
        progress_bar_base.setStyleSheet("background: none;")
        progress_bar_base.setFixedSize(336, 336)
        progress_bar_base.setFrameShape(QFrame.Shape.NoFrame)
        progress_bar_base.setFrameShadow(QFrame.Shadow.Raised)

        self.circular_progress = QFrame(progress_bar_base)
        self.circular_progress.setObjectName(u"circular_progress")
        self.circular_progress.setGeometry(QRect(10, 10, 300, 300))
        self.circular_progress.setFrameShape(QFrame.Shape.NoFrame)
        self.circular_progress.setFrameShadow(QFrame.Shadow.Raised)
        circular_progress_style = progress_bar_template.format(
            _object_name=self.circular_progress.objectName(),
            _border_radius=self._border_radius_one,
            _color_one=self._non_progress_color,
            _color_two=self._progress_color,
            _stop_one=self._stop_one,
            _stop_two=self._stop_two
        )
        self.circular_progress.setStyleSheet(circular_progress_style)

        circular_background = QFrame(progress_bar_base)
        circular_background.setObjectName(u"circrular_bg")
        circular_background.setGeometry(QRect(10, 10, 300, 300))
        circular_background.setFrameShape(QFrame.Shape.NoFrame)
        circular_background.setFrameShadow(QFrame.Shadow.Raised)
        background_style = circle_background_template.format(
            _object_name=circular_background.objectName(),
            _border_radius=self._border_radius_one,
            _color_three=self._color_three
        )
        circular_background.setStyleSheet(background_style)

        container = QFrame(progress_bar_base)
        container.setObjectName(u"container")
        container.setGeometry(QRect(25, 25, 270, 270))
        container.setFrameShape(QFrame.Shape.NoFrame)
        container.setFrameShadow(QFrame.Shadow.Raised)
        container_style = container_template.format(
            _object_name=container.objectName(),
            _border_radius=self._border_radius_two,
            _color_four=self._bg_color_main
        )
        container.setStyleSheet(container_style)

        progress_status_widget = QWidget(container)
        progress_status_widget.setObjectName(u"status_widget")
        progress_status_widget.setStyleSheet("background: none;")
        progress_status_widget.setGeometry(QRect(40, 50, 193, 191))

        title_label = QLabel(progress_status_widget)
        title_label.setObjectName(u"title_label")
        title_label.font().setPointSize(15)
        title_label.setMinimumSize(QSize(0, 30))
        title_label.setMaximumSize(QSize(16777215, 30))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_style = label_template.format(
            _object_name=title_label.objectName(),
            _color_five=self._text_color
        )
        title_label.setStyleSheet(title_style)

        self.percentage_label = QLabel(progress_status_widget)
        self.percentage_label.setObjectName(u"percentage_label")
        self.percentage_label.font().setPointSize(70)
        self.percentage_label.setMinimumSize(QSize(0, 100))
        self.percentage_label.setMaximumSize(QSize(16777215, 100))
        self.percentage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        percentage_style = label_template.format(
            _object_name=self.percentage_label.objectName(),
            _color_five=self._text_color
        )
        self.percentage_label.setStyleSheet(percentage_style)

        self.load_status_label = QLabel(progress_status_widget)
        self.load_status_label.setObjectName(u"load_status_label")
        self.load_status_label.setMinimumSize(QSize(0, 25))
        self.load_status_label.setMaximumSize(QSize(165, 25))
        self.load_status_label.font().setPointSize(11)
        self.load_status_label.setFrameShape(QFrame.Shape.NoFrame)
        self.load_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_style = label_template_two.format(
            _object_name=self.load_status_label.objectName(),
            _color_six=self._msg_bg_color,
            _color_five=self._text_color
        )
        self.load_status_label.setStyleSheet(status_style)

        grid_layout = QGridLayout(progress_status_widget)
        grid_layout.setObjectName(u"grid_layout")
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.addWidget(title_label, 0, 0, 1, 1)
        grid_layout.addWidget(self.percentage_label, 1, 0, 1, 1)
        grid_layout.addWidget(self.load_status_label, 2, 0, 1, 1)
        grid_layout.setHorizontalSpacing(6)
        grid_layout.setVerticalSpacing(6)

        circular_background.raise_()
        self.circular_progress.raise_()
        container.raise_()

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 120))

        circular_background.setGraphicsEffect(self.shadow)

        translation = u"<html><head/><body><p><span style=\" font-weight:600; color:#9b9bff;\">Processing:</span> @title</p></body></html>"
        translation = translation.replace("@title", self._title)

        title_label.setText(QCoreApplication.translate("CircleProgressBar", translation, None))

        self.percentage_label.setText(QCoreApplication.translate("CircleProgressBar",
                                                                u"<p><span style=\" font-size:70pt;\">0</span><span style=\" font-size:58pt; "
                                                                u"vertical-align:super;\">%</span></p>",
                                                                None))

        self.load_status_label.setText(QCoreApplication.translate("CircleProgressBar", u"", None))

        _main_layout = QVBoxLayout(self)
        _main_layout.addWidget(progress_bar_base, alignment=Qt.AlignmentFlag.AlignCenter)
        # self.setLayout(_main_layout)

    def set_text(self, text: str) -> None:
        self.load_status_label.setText(QCoreApplication.translate("CircleProgressBar", text, None))

    def set_value(self, value: float) -> None:
        # GET PROGRESS BAR VALUE, CONVERT TO FLOAT AND INVERT VALUES
        # stop works of 1.000 to 0.000
        progress = (100 - value) / 100.0

        # GET NEW VALUES
        if progress == 0:
            # stop_one, stop_two = str(0), str(0)
            stop_one = 0
            stop_two = 0
        else:
            # stop_one, stop_two = str(progress - 0.001), str(progress)
            stop_one = progress - 0.001
            stop_two = progress

        # SET VALUES TO NEW STYLESHEET
        circular_progress_style = progress_bar_template.format(
            _object_name=self.circular_progress.objectName(),
            _border_radius=self._border_radius_one,
            _color_one=self._non_progress_color,
            _color_two=self._progress_color,
            _stop_one=stop_one,
            _stop_two=stop_two
        )

        # APPLY STYLESHEET WITH NEW VALUES
        self.circular_progress.setStyleSheet(circular_progress_style)

        text_template = """<p><span style=" font-size:68pt;">{VALUE}</span><span style=" font-size:58pt; vertical-align:super;">%</span></p>"""

        # REPLACE VALUE
        new_text = text_template.replace("{VALUE}", str(value))

        # APPLY NEW PERCENTAGE TEXT
        self.percentage_label.setText(new_text)
