from src.core.pyqt_core import *


class QtExclusiveComboGroup(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._combo_boxes = []
        self._role = Qt.ItemDataRole.UserRole + 500

    def add_combo(self, combo: QComboBox):
        combo.activated.connect(
            lambda: self.handleActivated(combo))
        self._combo_boxes.append(combo)

    def handleActivated(self, target: QComboBox):
        index = target.currentIndex()
        groupid = id(target)

        for combo in self._combo_boxes:
            if combo is target:
                continue
            previous = combo.findData(groupid, self._role)
            if previous >= 0:
                combo.view().setRowHidden(previous, False)
                combo.setItemData(previous, None, self._role)
            if index > 0:
                combo.setItemData(index, groupid, self._role)
                combo.view().setRowHidden(index, True)
