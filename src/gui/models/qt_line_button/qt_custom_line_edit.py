from src.core.pyqt_core import *


class EnhancedLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__()
        if parent != None:
            self.setParent(parent)

    def import_sheets(self, focused_style, unfocused_style):
        self._focused_style = focused_style
        self._unfocused_style = unfocused_style

    def focusInEvent(self, event):
        self.parent().setStyleSheet(self._focused_style)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.parent().setStyleSheet(self._unfocused_style)
        super().focusOutEvent(event)
