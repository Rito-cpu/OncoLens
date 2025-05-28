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

        ###################################
        # Abstract Visualization Sub-Page #
        ###################################
        self.abstract_visualizer_submenu = QWidget()
        self.abstract_visualizer_submenu.setObjectName(u"abstract_visualizer_submenu")

        self.abstract_vis_layout = QVBoxLayout(self.abstract_visualizer_submenu)
        self.abstract_vis_layout.setSpacing(5)
        self.abstract_vis_layout.setObjectName(u"abstract_vis_layout")
        self.abstract_vis_layout.setContentsMargins(5, 5, 5, 5)

        self.abstract_vis_title = QLabel(self.abstract_visualizer_submenu)
        self.abstract_vis_title.setObjectName(u"abstract_vis_title")
        self.abstract_vis_title.setFont(font)
        self.abstract_vis_title.setStyleSheet(u"font-size: 16pt")
        self.abstract_vis_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.abstract_vis_bttn_frame = QFrame(self.abstract_visualizer_submenu)
        self.abstract_vis_bttn_frame.setObjectName(u"abstract_vis_bttn_frame")
        self.abstract_vis_bttn_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.abstract_vis_bttn_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.abstract_vis_bttn_layout = QVBoxLayout(self.abstract_vis_bttn_frame)
        self.abstract_vis_bttn_layout.setObjectName(u"abstract_vis_bttn_layout")
        self.abstract_vis_bttn_layout.setContentsMargins(5, 5, 5, 5)
        self.abstract_vis_bttn_layout.setSpacing(75)

        self.abstract_vis_layout.addWidget(self.abstract_vis_title)
        self.abstract_vis_layout.addStretch(1)
        self.abstract_vis_layout.addWidget(self.abstract_vis_bttn_frame)
        self.abstract_vis_layout.addStretch(1)

        self.menus.addWidget(self.abstract_visualizer_submenu)

        # Finish setup
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
        self.abstract_vis_title.setText(QCoreApplication.translate("RightColumn", u"Abstract Visualizer Menus", None))
    # retranslateUi
