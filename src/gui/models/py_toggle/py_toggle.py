from src.core.pyqt_core import *


class PyToggle(QCheckBox):
    def __init__(
        self,
        width: int=50,
        height: int=28,
        ellipse_y: int = 3,
        bg_color: str="#777",
        circle_color: str="#DDD",
        active_color: str="#00BCFF",
        animation_curve = QEasingCurve.Type.OutBounce,
        parent=None
    ):
        super().__init__()
        self.setFixedSize(width, height)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # **** Arguments ****
        self._ellipse_y = ellipse_y
        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color

        self._position = 3
        self.animation = QPropertyAnimation(self, b"position")
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(500)
        self.stateChanged.connect(self.setup_animation)

    @pyqtProperty(float)
    def position(self):
        return self._position

    @position.setter
    def position(self, pos):
        self._position = pos
        self.update()

    # START STOP ANIMATION
    def setup_animation(self, value):
        self.animation.stop()
        if value:
            self.animation.setEndValue(self.width() - (self.width()*0.52))
        else:
            self.animation.setEndValue(self.width()*0.08)
        self.animation.start()

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setFont(QFont("Avenir", 9))

        # SET PEN
        p.setPen(Qt.PenStyle.NoPen)

        # DRAW ELLIPSE
        ellipse_size = self.height() * 0.8
        ellipse_x = self._position + (self.width() - ellipse_size) / 2
        ellipse_y = (self.height() - ellipse_size) / 2

        if not self.isChecked():
            p.setBrush(QColor(self._bg_color))
            p.drawRoundedRect(0, 0, self.width(), self.height(), self.height() / 2, self.height() / 2)
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._position, self._ellipse_y, ellipse_size, ellipse_size)
        else:
            p.setBrush(QColor(self._active_color))
            p.drawRoundedRect(0, 0, self.width(), self.height(), self.height() / 2, self.height() / 2)
            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._position, self._ellipse_y, ellipse_size, ellipse_size)

        p.end()
