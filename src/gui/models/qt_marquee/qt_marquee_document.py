from src.core.pyqt_core import *


class QtDocument(QTextDocument):
    def __init__(self, parent=None):
        super().__init__(parent)

        if parent != None:
            self.setParent(parent)

    def drawContents(self, painter: QPainter, rect=QRectF()):
        painter.save()
        paint_context = QAbstractTextDocumentLayout.PaintContext()
        paint_context.palette.setColor(QPalette.ColorRole.Text, painter.pen().color())

        # painter.setPen(self._color)

        if rect.isValid():
            painter.setClipRect(rect)
            paint_context.clip = rect

        self.documentLayout().draw(painter, paint_context)
        painter.restore()