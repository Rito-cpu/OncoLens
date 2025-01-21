from src.core.pyqt_core import *


class Ui_RightColumn(object):
    def setupUi(self, RightColumn):
        if not RightColumn.objectName():
            RightColumn.setObjectName(u"RightColumn")
        RightColumn.resize(240, 600)

        self.main_pages_layout = QVBoxLayout(RightColumn)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)

        self.menus = QStackedWidget(RightColumn)
        self.menus.setObjectName(u"menus")

        # Menu 1 page setup
        self.menu_1 = QWidget()
        self.menu_1.setObjectName(u"menu_1")

        self.verticalLayout = QVBoxLayout(self.menu_1)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)

        self.btn_1_widget = QWidget(self.menu_1)
        self.btn_1_widget.setObjectName(u"btn_1_widget")
        self.btn_1_widget.setMinimumSize(QSize(0, 40))
        self.btn_1_widget.setMaximumSize(QSize(16777215, 40))

        self.btn_1_layout = QVBoxLayout(self.btn_1_widget)
        self.btn_1_layout.setSpacing(0)
        self.btn_1_layout.setObjectName(u"btn_1_layout")
        self.btn_1_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.btn_1_widget)

        self.label_1 = QLabel(self.menu_1)
        self.label_1.setObjectName(u"label_1")

        font = QFont()
        font.setPointSize(16)

        self.label_1.setFont(font)
        self.label_1.setStyleSheet(u"font-size: 16pt")
        self.label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_1)

        self.menus.addWidget(self.menu_1)

        # ETB menu page
        self.etb_menu_page = QWidget()
        self.etb_menu_page.setObjectName(u"etb_menu_page")

        self.etb_page_layout = QVBoxLayout(self.etb_menu_page)
        self.etb_page_layout.setObjectName(u"etb_center_layout")
        self.etb_page_layout.setSpacing(5)
        self.etb_page_layout.setContentsMargins(5, 5, 5, 5)

        self.etb_submenu_label = QLabel(self.etb_menu_page)
        self.etb_submenu_label.setObjectName(u"title_label")
        self.etb_submenu_label.setMaximumSize(QSize(16777215, 40))
        self.etb_submenu_label.setStyleSheet(u"font-size: 16pt;")
        self.etb_submenu_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.etb_bttn_frame = QFrame(self.etb_menu_page)
        self.etb_bttn_frame.setObjectName(u"bttn_frame")
        self.etb_bttn_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.etb_bttn_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.etb_bttn_layout = QVBoxLayout(self.etb_bttn_frame)
        self.etb_bttn_layout.setObjectName(u"button_layout")
        self.etb_bttn_layout.setContentsMargins(5, 5, 5, 5)
        self.etb_bttn_layout.setSpacing(75)

        self.etb_page_layout.addWidget(self.etb_submenu_label)
        self.etb_page_layout.addStretch(1)
        self.etb_page_layout.addWidget(self.etb_bttn_frame)
        self.etb_page_layout.addStretch(1)

        self.menus.addWidget(self.etb_menu_page)

        ###################################
        #   Enhanced Modeling Sub Menu   #
        ###################################
        self.enhanced_modeling_submenu = QWidget()
        self.enhanced_modeling_submenu.setObjectName("enhanced_modeling_submenu")

        self.enhanced_modeling_submenu_layout = QVBoxLayout(self.enhanced_modeling_submenu)
        self.enhanced_modeling_submenu_layout.setObjectName("enhanced_modeling_submenu_layout")
        self.enhanced_modeling_submenu_layout.setSpacing(5)
        self.enhanced_modeling_submenu_layout.setContentsMargins(5, 5, 5, 5)

        self.enhanced_modeling_title = QLabel(self.enhanced_modeling_submenu)
        self.enhanced_modeling_title.setObjectName("enhanced_modeling_title")
        self.enhanced_modeling_title.setMaximumSize(QSize(16777215, 40))
        self.enhanced_modeling_title.setStyleSheet("font-size: 16pt;")
        self.enhanced_modeling_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.enhanced_modeling_bttn_frame = QFrame(self.enhanced_modeling_submenu)
        self.enhanced_modeling_bttn_frame.setObjectName("enhanced_modeling_bttn_frame")
        self.enhanced_modeling_bttn_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.enhanced_modeling_bttn_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.enhanced_modeling_bttn_layout = QVBoxLayout(self.enhanced_modeling_bttn_frame)
        self.enhanced_modeling_bttn_layout.setObjectName("enhanced_modeling_bttn_layout")
        self.enhanced_modeling_bttn_layout.setContentsMargins(5, 5, 5, 5)
        self.enhanced_modeling_bttn_layout.setSpacing(75)

        self.enhanced_modeling_submenu_layout.addWidget(self.enhanced_modeling_title)
        self.enhanced_modeling_submenu_layout.addStretch(1)
        self.enhanced_modeling_submenu_layout.addWidget(self.enhanced_modeling_bttn_frame)
        self.enhanced_modeling_submenu_layout.addStretch(1)

        self.menus.addWidget(self.enhanced_modeling_submenu)

        # Menu 2 page setup
        self.menu_2 = QWidget()
        self.menu_2.setObjectName(u"menu_2")

        self.verticalLayout_2 = QVBoxLayout(self.menu_2)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)

        self.btn_2_widget = QWidget(self.menu_2)
        self.btn_2_widget.setObjectName(u"btn_2_widget")
        self.btn_2_widget.setMinimumSize(QSize(0, 40))
        self.btn_2_widget.setMaximumSize(QSize(16777215, 40))

        self.btn_2_layout = QVBoxLayout(self.btn_2_widget)
        self.btn_2_layout.setSpacing(0)
        self.btn_2_layout.setObjectName(u"btn_2_layout")
        self.btn_2_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.btn_2_widget)

        self.label_2 = QLabel(self.menu_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"font-size: 16pt")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_3 = QLabel(self.menu_2)
        self.label_3.setObjectName(u"label_3")

        font1 = QFont()
        font1.setPointSize(9)

        self.label_3.setFont(font1)
        self.label_3.setStyleSheet(u"font-size: 9pt")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_3.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_3)

        self.menus.addWidget(self.menu_2)

        self.main_pages_layout.addWidget(self.menus)


        self.retranslateUi(RightColumn)

        self.menus.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(RightColumn)
    # setupUi

    def retranslateUi(self, RightColumn):
        RightColumn.setWindowTitle(QCoreApplication.translate("RightColumn", u"Form", None))
        self.etb_submenu_label.setText(QCoreApplication.translate("RightColumn", u"Modeling Menus", None))
        self.enhanced_modeling_title.setText(QCoreApplication.translate("RightColumn", u"Enhanced Modeling Menus", None))
        self.label_1.setText(QCoreApplication.translate("RightColumn", u"Menu 1 - Right Menu", None))
        self.label_2.setText(QCoreApplication.translate("RightColumn", u"Rosetta Sub-Page\nMenu", None))
        self.label_3.setText(QCoreApplication.translate("RightColumn", u"Currently Unavailable", None))
    # retranslateUi
