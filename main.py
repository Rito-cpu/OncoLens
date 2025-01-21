#! /usr/bin/python
import os
import sys

from src.core.pyqt_core import *
from src.core.app_config import APP_ROOT, IMG_RSC_PATH
from src.main_window import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("macOS")

    # icon_loc = os.path.abspath(os.path.join(PROJ_ROOT, "coe_blue.ico"))
    # my_app.setWindowIcon(QIcon(icon_loc))

    main_window = MainWindow()
    main_window.show()

    app.exec()
