from src.core.pyqt_core import *
from .qt_marquee_document import QtDocument


class QtMarqueeLabel(QLabel):
    paused = False

    def __init__(
            self,
            color: str = 'black',
            speed: int = 20,
            mode: str = 'LR',
            parent=None
        ):
        super().__init__(parent)

        if parent != None:
            self.setParent(parent)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._color = QColor(color)
        self._speed = speed
        self._mode = mode

        self.padding_space = 1
        self._pos_x = 0

        self.document = QtDocument(self)
        self.document.setUseDesignMetrics(True)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.translate)

        self.update()

    def setText(self, new_text: str, mode: str = "LR"):
        font = self.font()
        self.font_metric = QFontMetrics(font)

        self.document.setDefaultFont(font)
        self.document.setDocumentMargin(1)

        if self.timer.isActive() :
            self.timer.stop()

        # If new_text is longer than the QLabel
        if self.font_metric.horizontalAdvance(new_text) > self.width():
            self.padding_space = int(self.width() / self.font_metric.horizontalAdvance(' '))
            long_string = ' ' * self.padding_space + new_text + ' ' * self.padding_space

            self.document.clear()
            self.document.setTextWidth(self.font_metric.horizontalAdvance(long_string) + 22)
            self.document.setPlainText(long_string)

            self.set_mode(mode)
            self.timer.start(self._speed)
        else:   # new_text is shorter than QLabel
            self.document.clear()
            self.document.setPlainText(new_text)
            self.repaint()

    def set_mode(self, new_mode: str):
        if new_mode == "RL":
            self._pos_x = 0
        elif new_mode == "LR":
            self._pos_x = -(self.document.textWidth() - self.font_metric.horizontalAdvance(" " * self.padding_space) - 10)
        else:
            self._pos_x = -(self.document.textWidth() - self.font_metric.horizontalAdvance(" " * self.padding_space) - 10)
            self.fstr = True

        self._mode = new_mode

    @pyqtSlot()
    def translate(self):
        if not self.paused:
            if self._mode == "RL":
                if self.width() - self._pos_x < self.document.textWidth():
                    self._pos_x -= 1
                else:
                    self._pos_x = 0
            elif self._mode == "LR":
                if self._pos_x <= 0:
                    self._pos_x += 1
                else:
                    self._pos_x = -(self.document.textWidth() - self.font_metric.horizontalAdvance(" " * self.padding_space) - 10)
            else:
                if self.fstr:
                    if self._pos_x <= 0:
                        self._pos_x += 1
                    else:
                        self._pos_x = 0
                        self.fstr = False
                else:
                    if self.width() - self._pos_x < self.document.textWidth():
                        self._pos_x -= 1
                    else:
                        self._pos_x = -(self.document.textWidth() - self.font_metric.horizontalAdvance(" " * self.padding_space) - 10)
                        self.fstr = True

        self.repaint()

    def event(self, event):
        if event.type() == QEvent.Type.Enter:
            self.paused = True
        elif event.type() == QEvent.Type.Leave:
            self.paused = False

        return super().event(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self._color)

        painter.translate(self._pos_x, 0)
        self.document.drawContents(painter)

        return super().paintEvent(event)
