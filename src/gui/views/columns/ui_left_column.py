from src.core.pyqt_core import *


class Ui_LeftColumn(object):
    def setupUi(self, LeftColumn):
        if not LeftColumn.objectName():
            LeftColumn.setObjectName(u"LeftColumn")
        LeftColumn.resize(240, 600)

        self.main_pages_layout = QVBoxLayout(LeftColumn)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)

        self.menus = QStackedWidget(LeftColumn)
        self.menus.setObjectName(u"menus")

        self.settings_menu = QWidget()
        self.settings_menu.setObjectName(u"menu_1")

        self.verticalLayout = QVBoxLayout(self.settings_menu)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)

        self.btn_1_widget = QWidget(self.settings_menu)
        self.btn_1_widget.setObjectName(u"btn_1_widget")
        self.btn_1_widget.setMinimumSize(QSize(0, 40))
        self.btn_1_widget.setMaximumSize(QSize(16777215, 40))

        self.btn_1_layout = QVBoxLayout(self.btn_1_widget)
        self.btn_1_layout.setSpacing(0)
        self.btn_1_layout.setObjectName(u"btn_1_layout")
        self.btn_1_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.btn_1_widget)

        self.btn_2_widget = QWidget(self.settings_menu)
        self.btn_2_widget.setObjectName(u"btn_2_widget")
        self.btn_2_widget.setMinimumSize(QSize(0, 40))
        self.btn_2_widget.setMaximumSize(QSize(16777215, 40))

        self.btn_2_layout = QVBoxLayout(self.btn_2_widget)
        self.btn_2_layout.setSpacing(0)
        self.btn_2_layout.setObjectName(u"btn_2_layout")
        self.btn_2_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.btn_2_widget)

        self.btn_3_widget = QWidget(self.settings_menu)
        self.btn_3_widget.setObjectName(u"btn_3_widget")
        self.btn_3_widget.setMinimumSize(QSize(0, 40))
        self.btn_3_widget.setMaximumSize(QSize(16777215, 40))

        self.btn_3_layout = QVBoxLayout(self.btn_3_widget)
        self.btn_3_layout.setSpacing(0)
        self.btn_3_layout.setObjectName(u"btn_3_layout")
        self.btn_3_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.btn_3_widget)

        self.label_1 = QLabel(self.settings_menu)
        self.label_1.setObjectName(u"label_1")

        font = QFont()
        font.setPointSize(16)

        self.label_1.setFont(font)
        self.label_1.setStyleSheet(u"font-size: 16pt")
        self.label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_1)

        self.menus.addWidget(self.settings_menu)

        self.info_menu = QWidget()
        self.info_menu.setObjectName(u"menu_2")

        self.verticalLayout_2 = QVBoxLayout(self.info_menu)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)

        self.btn_4_widget = QWidget(self.info_menu)
        self.btn_4_widget.setObjectName(u"btn_4_widget")
        self.btn_4_widget.setMinimumSize(QSize(0, 40))
        self.btn_4_widget.setMaximumSize(QSize(16777215, 40))

        self.btn_4_layout = QVBoxLayout(self.btn_4_widget)
        self.btn_4_layout.setSpacing(0)
        self.btn_4_layout.setObjectName(u"btn_4_layout")
        self.btn_4_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.btn_4_widget)

        self.label_2 = QLabel(self.info_menu)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"font-size: 16pt")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_3 = QLabel(self.info_menu)
        self.label_3.setObjectName(u"label_3")

        font1 = QFont()
        font1.setPointSize(9)

        self.label_3.setFont(font1)
        self.label_3.setStyleSheet(u"font-size: 9pt")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_3.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_3)

        self.menus.addWidget(self.info_menu)

        self.etb_column_menu = QWidget()
        self.etb_column_menu.setObjectName(u"etb_column_container")

        self.etb_column_layout = QVBoxLayout(self.etb_column_menu)
        self.etb_column_layout.setSpacing(5)
        self.etb_column_layout.setObjectName(u"etb_column_layout")
        self.etb_column_layout.setContentsMargins(5, 5, 5, 5)

        label = QLabel(self.etb_column_menu)
        label.setText("Place 3 buttons!")

        bt_1 = QPushButton(self.etb_column_menu)
        bt_1.setText("Input File Page")

        bt_2 = QPushButton(self.etb_column_menu)
        bt_2.setText("Parameters Page")

        bt_3 = QPushButton(self.etb_column_menu)
        bt_3.setText("Plot Page")

        self.etb_column_layout.addWidget(label)
        self.etb_column_layout.addWidget(bt_1)
        self.etb_column_layout.addWidget(bt_2)
        self.etb_column_layout.addWidget(bt_3)

        self.menus.addWidget(self.etb_column_menu)

        self.main_pages_layout.addWidget(self.menus)


        self.retranslateUi(LeftColumn)

        self.menus.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(LeftColumn)
    # setupUi

    def retranslateUi(self, LeftColumn):
        LeftColumn.setWindowTitle(QCoreApplication.translate("LeftColumn", u"Form", None))
        self.label_1.setText(QCoreApplication.translate("LeftColumn", u"Menu 1 - Left Menu", None))
        self.label_2.setText(QCoreApplication.translate("LeftColumn", u"No information\nto display yet.", None))
        self.label_3.setText(QCoreApplication.translate("LeftColumn", u"Widgets can be added here.", None))
    # retranslateUi

