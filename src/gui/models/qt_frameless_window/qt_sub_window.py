from src.core.pyqt_core import *
from src.core.json.json_themes import Themes
from src.core.processing.etb_modeling import etb_process
from src.gui.models import *
from src.gui.models.qt_process import qt_process_thread
from src.gui.models.qt_message import QtMessage
from threading import Thread
from queue import Queue


class FramelessWindow(QWidget):
    close_signal = pyqtBoundSignal()
    reuse = pyqtSignal(list)      # pyqtSignal(np.ndarray)
    finished = pyqtSignal(dict)

    def __init__(
            self,
            corner_radius: int=11,
            radius: int=8,
            color: str="white",
            bg_color: str="black",
            bg_color_two: str="black",
            bg_color_hover: str="gray",
            bg_color_pressed: str="lightgray",
            circle_color: str="",
            active_color: str="",
            main_bg_color: str="white",
            widget: NonSystemicSettings=None,
            data: list=None,
            parent=None
        ):
        super().__init__()

        # **** Create class parameters ****
        self._corner_radius = corner_radius
        self._radius = radius
        self._color = color
        self._bg_color = bg_color
        self._bg_color_two = bg_color_two
        self._bg_color_hover = bg_color_hover
        self._bg_color_pressed = bg_color_pressed
        self._circle_color = circle_color
        self._active_color = active_color
        self._widget = widget
        self._data = data
        self._parent=parent

        # **** Window properties ****
        self.setObjectName(u"sub_window")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setMask(self.get_mask())
        self.setStyleSheet("""
            QWidget#sub_window {{
                background: {_bg};
                border: 0px solid black;
                border-radius: 13px;
            }}
        """.format(_bg=main_bg_color))

        # **** Setup UI widgets ****
        self.setup_widget()

        # *** Connect signals to slots ****
        self.close_button.clicked.connect(self.close)
        self.submit_button.clicked.connect(self.switch_menu)
        self.submit_button.clicked.connect(self.get_table_settings)

        self.old_pos = self.pos()

        self.show()

    def setup_widget(self):
        self.menu_stack = QStackedWidget(self)
        self.menu_stack.setContentsMargins(0, 0, 0, 0)

        # **** First menu ****
        table_frame = QFrame(self.menu_stack)
        table_frame.setObjectName(u"window_frame")
        table_frame.setFrameShape(QFrame.Shape.NoFrame)
        table_frame.setFrameShadow(QFrame.Shadow.Raised)

        reuse_frame = QFrame(table_frame)
        reuse_frame.setObjectName(u"reuse_frame")
        reuse_frame.setFrameShape(QFrame.Shape.NoFrame)
        reuse_frame.setFrameShadow(QFrame.Shadow.Raised)
        reuse_frame.setStyleSheet("background: {_bg}; border: None; border-radius: 12px;".format(_bg="gray"))
        reuse_frame.setFixedSize(175, 60)

        reuse_label = QLabel(reuse_frame)
        reuse_label.setObjectName(u"reuse_label")
        reuse_label.setText("Reuse Table")
        reuse_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        reuse_label.setStyleSheet("color: {_color};".format(_color=self._color))

        self.reuse_toggle = PyToggle(
            width=34,
            height=20,
            ellipse_y=2,
            bg_color = self._bg_color,
            circle_color = self._circle_color,
            active_color = self._active_color,
            parent=reuse_frame
        )
        self.reuse_toggle.setObjectName(u"reuse_toggle")
        self.reuse_toggle.setChecked(True)
        self.reuse_toggle.setCursor(Qt.CursorShape.PointingHandCursor)

        toggle_layout = QHBoxLayout(reuse_frame)
        toggle_layout.setSpacing(15)
        toggle_layout.addStretch(1)
        toggle_layout.addWidget(reuse_label)
        toggle_layout.addWidget(self.reuse_toggle)
        toggle_layout.addStretch(1)

        self.close_button = PyPushButton(
            text="Close",
            radius=self._radius,
            color=self._color,
            bg_color=self._bg_color,
            bg_color_hover=self._bg_color_hover,
            bg_color_pressed=self._bg_color_pressed,
            parent=table_frame
        )
        self.close_button.setObjectName(u"close_button")
        self.close_button.setMinimumHeight(40)
        self.close_button.setFixedWidth(185)

        self.submit_button = PyPushButton(
            text="Submit",
            radius=self._radius,
            color=self._color,
            bg_color=self._bg_color,
            bg_color_hover=self._bg_color_hover,
            bg_color_pressed=self._bg_color_pressed,
            parent=table_frame
        )
        self.submit_button.setObjectName(u"submit_button")
        self.submit_button.setMinimumHeight(40)
        self.submit_button.setFixedWidth(185)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(75)
        button_layout.addStretch(1)
        button_layout.addWidget(self.close_button)
        button_layout.addWidget(self.submit_button)
        button_layout.addStretch(1)

        frame_layout = QVBoxLayout(table_frame)
        frame_layout.setContentsMargins(5, 5, 5, 5)
        frame_layout.setSpacing(15)
        if self._widget:
            frame_layout.addWidget(self._widget)
        frame_layout.addWidget(reuse_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        frame_layout.addLayout(button_layout)

        self.menu_stack.addWidget(table_frame)
        self.menu_stack.setCurrentIndex(0)

        # **** Second menu ****
        progress_frame = QFrame(self.menu_stack)
        progress_frame.setObjectName(u"progress_frame")
        progress_frame.setFrameShape(QFrame.Shape.NoFrame)
        progress_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.circle_bar = QtCircleProgressBar(title="ETB Modeling", parent=progress_frame)
        self.circle_bar.set_text("Null")
        self.circle_bar.set_value(0)

        progress_layout = QVBoxLayout(progress_frame)
        progress_layout.addWidget(self.circle_bar)

        self.menu_stack.addWidget(progress_frame)

        # **** Set stack of widgets to main layout ****
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(9, 9, 9, 9)
        main_layout.addWidget(self.menu_stack)

        self.setFixedSize(550, 400)

    def switch_menu(self):
        self._data.append(self.get_table_settings())

        self.create_thread()
        self.menu_stack.setCurrentIndex(1)

        self.pass_saved_array()

    def create_thread(self):
        self.result_queue = Queue()

        self.modeling_process = qt_process_thread.QtProcessThread(method=etb_process, model_options=self._data)
        self.my_thread = Thread(target=self.modeling_process.run, args=(self.result_queue,), daemon=False)
        self.modeling_process.progress_signal.connect(self.report_progress)
        self.modeling_process.error_signal.connect(self.error_handler)

        self.my_thread.start()

    def report_progress(self, current_progress):
        self.circle_bar.set_value(current_progress)

        if current_progress == 100:
            self.circle_bar.set_text("Finished!")
            self.emit_plot()
        elif current_progress == 1:
            self.circle_bar.set_text("Importing Excel data...")
        elif current_progress == 15:
            self.circle_bar.set_text("Time calculations...")
        elif current_progress == 25:
            self.circle_bar.set_text("Structuring treament plot...")
        elif current_progress == 45:
            self.circle_bar.set_text("Preparing model data...")
        elif current_progress == 55:
            self.circle_bar.set_text("Nonsystemic treatments...")
        elif current_progress == 70:
            self.circle_bar.set_text("Running model...")
        elif current_progress == 85:
            self.circle_bar.set_text("Preparing model plot data...")
        elif current_progress == 90:
            self.circle_bar.set_text("Plotting model...")
        elif current_progress == 95:
            self.circle_bar.set_text("Plotting treatments...")
            self.circle_bar.set_value(100)
            self.circle_bar.set_text("Finished")

    def error_handler(self, exception):
        exception_msg, exception_traceback = exception
        proc_err_dialog = QtMessage(
            buttons={
                "Ok": QMessageBox.ButtonRole.AcceptRole
            },
            color=self._color,
            bg_color_one=self._bg_color,
            bg_color_two=self._bg_color_two,
            bg_color_hover=self._bg_color_hover,
            bg_color_pressed=self._bg_color_pressed
        )
        proc_err_dialog.setIcon(QMessageBox.Icon.Critical)
        proc_err_dialog.setCursor(Qt.CursorShape.PointingHandCursor)
        proc_err_dialog.setText("Encountered an error within modeling.")
        proc_err_dialog.setInformativeText("Error: " + str(exception_msg))
        proc_err_dialog.setDetailedText(exception_traceback)
        proc_err_dialog.exec()

        self.close()

    def get_table_settings(self):
        return self._widget.get_matrix()

    def pass_saved_array(self):
        pass_off = [self._data[-1]["array"], self.reuse_toggle.isChecked()]
        self.reuse.emit(pass_off)

    def emit_plot(self):
        plots = self.result_queue.get()
        self.finished.emit(plots)
        self.close()

    def get_mask(self):
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), self._corner_radius, self._corner_radius)
        return QRegion(path.toFillPolygon().toPolygon())

    def resizeEvent(self, event):
        self.setMask(self.get_mask())
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPosition().toPoint()

    def showEvent(self, event):
        if not event.spontaneous():
            screens = QApplication.screens()
            cursor_pos = QCursor.pos()

            for i in range(len(screens)):
                if screens[i].geometry().contains(cursor_pos):
                    screen = screens[i]
                    break
            rect = screen.geometry()
            window_size = self.size()

            left = rect.left() + (rect.width() - window_size.width()) / 2
            top = rect.top() + (rect.height() - window_size.height()) / 2

            self.setGeometry(QRect(left, top, window_size.width(), window_size.height()))

    def closeEvent(self, event):
        self.reuse_toggle.deleteLater()
        self.close_button.deleteLater()
        self.submit_button.deleteLater()
        self.circle_bar.deleteLater()

        super().closeEvent(event)
