# -*- coding: utf-8 -*-

from src.core.pyqt_core import *
from src.core.image_functions import Functions
from src.gui.models import *


class Ui_MainPages(object):
    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        MainPages.resize(860, 600)

        self.main_pages_layout = QVBoxLayout(MainPages)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)

        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")

        # ***********************************
        # * Home page Frame/Layout creation *
        # ***********************************
        self.home_menu_container = QWidget()
        self.home_menu_container.setObjectName(u"home_page")
        self.home_menu_container.setStyleSheet(u"font-size: 14pt")

        _home_menu_layout = QVBoxLayout(self.home_menu_container)
        _home_menu_layout.setContentsMargins(5, 5, 5, 5)
        _home_menu_layout.setSpacing(20)
        _home_menu_layout.setObjectName(u"page_1_layout")

        home_upper_frame = QFrame(self.home_menu_container)
        home_upper_frame.setObjectName(u"logo_frame")
        home_upper_frame.setFrameShape(QFrame.Shape.NoFrame)
        home_upper_frame.setFrameShadow(QFrame.Shadow.Raised)

        home_label = QLabel(home_upper_frame)
        home_label.setObjectName(u"label")
        home_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        home_label.setText(QCoreApplication.translate("MainPages", u"Home Directory", None))
        home_label.setStyleSheet('font-size: 16px; font-weight: bold;')

        self.logo = QFrame(home_upper_frame)
        self.logo.setObjectName(u"logo")
        self.logo.setMinimumSize(QSize(325, 325))
        self.logo.setMaximumSize(QSize(325, 325))
        self.logo.setFrameShape(QFrame.Shape.NoFrame)
        self.logo.setFrameShadow(QFrame.Shadow.Raised)

        _logo_svg = QSvgWidget(Functions.set_svg_image("coe_blue_image.svg"))

        self.logo_layout = QVBoxLayout(self.logo)
        self.logo_layout.setSpacing(0)
        self.logo_layout.setObjectName(u"logo_layout")
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.addWidget(_logo_svg, Qt.AlignmentFlag.AlignCenter, Qt.AlignmentFlag.AlignCenter)

        home_upper_layout = QVBoxLayout(home_upper_frame)
        home_upper_layout.setContentsMargins(0, 0, 0, 0)
        home_upper_layout.setSpacing(50)
        home_upper_layout.addWidget(home_label, alignment=Qt.AlignmentFlag.AlignCenter)
        home_upper_layout.addWidget(self.logo, alignment=Qt.AlignmentFlag.AlignCenter)

        self.directory_frame = QFrame(self.home_menu_container)
        self.directory_frame.setObjectName(u"welcome_base")
        self.directory_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.directory_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.directory_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.dir_entry_interaction = QHBoxLayout()
        self.dir_entry_interaction.setObjectName(u'dir_entry_interaction')
        self.dir_entry_interaction.setContentsMargins(5, 5, 5, 5)
        self.dir_entry_interaction.setSpacing(15)

        self.bttn_holder = QVBoxLayout()
        self.bttn_holder.setObjectName(u'bttn_holder')
        self.bttn_holder.setContentsMargins(0, 22, 0, 0)

        self.project_dir_frame = QFrame(self.directory_frame)
        self.project_dir_frame.setObjectName(u'project_dir_frame')
        self.project_dir_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.project_dir_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.project_dir_frame.setStyleSheet("""
            QFrame#project_dir_frame {{
                background: {_bg_color};
                border-radius: 6px;
            }}
        """.format(_bg_color="rgba(255, 255, 255, 175)"))

        dir_intro_label = QLabel(self.project_dir_frame)
        dir_intro_label.setObjectName(u'dir_intro_label')
        dir_intro_label.setText('Project Directory:')
        dir_intro_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.project_dir_layout = QHBoxLayout(self.project_dir_frame)
        self.project_dir_layout.setObjectName(u'project_dir_layout')
        self.project_dir_layout.setContentsMargins(0, 3, 0, 3)
        self.project_dir_layout.setSpacing(5)
        self.project_dir_layout.addStretch(1)
        self.project_dir_layout.addWidget(dir_intro_label)

        self.directory_frame_layout = QVBoxLayout(self.directory_frame)
        self.directory_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.directory_frame_layout.setSpacing(5)
        self.directory_frame_layout.setObjectName(u"center_page_layout")
        self.directory_frame_layout.addLayout(self.dir_entry_interaction)
        self.directory_frame_layout.addWidget(self.project_dir_frame)
        # self.directory_frame_layout.addWidget(self.directory_label)

        _home_menu_layout.addStretch(1)
        _home_menu_layout.addWidget(home_upper_frame, 0, Qt.AlignmentFlag.AlignHCenter)
        _home_menu_layout.addStretch(1)
        _home_menu_layout.addWidget(self.directory_frame, 0, Qt.AlignmentFlag.AlignHCenter)
        _home_menu_layout.addStretch(1)
        self.pages.addWidget(self.home_menu_container)

        # *****************************
        # **** ETB data import page ****
        # *****************************
        self.etb_file_subpage = QWidget()
        self.etb_file_subpage.setObjectName(u"etb_page_1")

        self.file_center_layout = QVBoxLayout(self.etb_file_subpage)
        self.file_center_layout.setSpacing(5)
        self.file_center_layout.setObjectName(u"page_2_layout")
        self.file_center_layout.setContentsMargins(5, 5, 5, 5)

        self.file_scroll_area = QScrollArea(self.etb_file_subpage)
        self.file_scroll_area.setObjectName(u"scroll_area")
        self.file_scroll_area.setStyleSheet(u"background: transparent;")
        self.file_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.file_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.file_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.file_scroll_area.setWidgetResizable(True)

        self.file_scroll_contents = QWidget()
        self.file_scroll_contents.setObjectName(u"contents")
        self.file_scroll_contents.setGeometry(QRect(0, 0, 840, 580))
        # self.etb_scroll_contents.setStyleSheet(u"border: 2px solid lightblue;")
        self.file_scroll_contents.setStyleSheet(u"background: transparent;")

        font = QFont()
        font.setPointSize(16)
        self.import_data_title = QLabel(self.file_scroll_contents)
        self.import_data_title.setObjectName(u"import_data_title")
        self.import_data_title.setMaximumSize(QSize(16777215, 40))
        self.import_data_title.setStyleSheet("font-size: 18px; font-weight: bold; text-decoration: underline;")
        self.import_data_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.file_content_layout = QVBoxLayout(self.file_scroll_contents)
        self.file_content_layout.setSpacing(15)
        self.file_content_layout.setObjectName(u"file_content_layout")
        self.file_content_layout.setContentsMargins(5, 5, 5, 5)
        # self.file_content_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.file_content_layout.addWidget(self.import_data_title)

        self.file_scroll_area.setWidget(self.file_scroll_contents)

        self.file_center_layout.addWidget(self.file_scroll_area)

        self.pages.addWidget(self.etb_file_subpage)

        # *****************************
        # **** ETB Parameters Page ****
        # *****************************
        self.etb_settings_subpage = QWidget()
        self.etb_settings_subpage.setObjectName(u"etb_page_2")

        self.parameter_scroll_contents = QWidget()
        self.parameter_scroll_contents.setObjectName(u"parameter_contents")
        self.parameter_scroll_contents.setGeometry(QRect(0, 0, 840, 580))
        self.parameter_scroll_contents.setStyleSheet(u"background: transparent;")

        parameter_scroll_area = QScrollArea(self.etb_settings_subpage)
        parameter_scroll_area.setObjectName(u"parameter_scroll_area")
        parameter_scroll_area.setStyleSheet(u"background: transparent;")
        parameter_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        parameter_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        parameter_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        parameter_scroll_area.setWidgetResizable(True)
        parameter_scroll_area.setWidget(self.parameter_scroll_contents)

        self.parameter_title = QLabel(self.parameter_scroll_contents)
        self.parameter_title.setObjectName(u"title_label")
        self.parameter_title.setMaximumSize(QSize(16777215, 40))
        # self.parameter_title.font().setPointSize(22)
        # self.parameter_title.font().setBold(True)
        self.parameter_title.setStyleSheet(u"font-size: 16pt; font-weight: bold;")
        self.parameter_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.parameter_scroll_layout = QVBoxLayout(self.parameter_scroll_contents)
        self.parameter_scroll_layout.setObjectName(u"parameter_scroll_layout")
        self.parameter_scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.parameter_scroll_layout.setSpacing(15)
        # self.parameter_scroll_layout.addWidget(self.parameter_title)

        self.parameter_center_layout = QVBoxLayout(self.etb_settings_subpage)
        self.parameter_center_layout.setSpacing(5)
        self.parameter_center_layout.setContentsMargins(15, 5, 15, 5)
        self.parameter_center_layout.setObjectName(u"etb_parameter_layout")
        self.parameter_center_layout.addWidget(self.parameter_title)
        self.parameter_center_layout.addWidget(parameter_scroll_area)

        self.pages.addWidget(self.etb_settings_subpage)

        # ***********************
        # **** ETB Plot Page ****
        # ***********************
        self.etb_plot_subpage = QWidget()
        self.etb_plot_subpage.setObjectName(u"etb_page_3")

        plot_scroll_contents = QWidget()
        plot_scroll_contents.setObjectName(u"plot_contents")
        plot_scroll_contents.setGeometry(QRect(0, 0, 840, 580))
        plot_scroll_contents.setStyleSheet(u"background: transparent;")

        self.plot_stack_menu = QStackedWidget(plot_scroll_contents)
        self.plot_stack_menu.setObjectName('plot_stack_menu')
        self.plot_stack_menu.setContentsMargins(0, 0, 0, 0)

        self.plot_scroll_layout = QVBoxLayout(plot_scroll_contents)
        self.plot_scroll_layout.setObjectName(u"plot_scroll_layout")
        self.plot_scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.plot_scroll_layout.setSpacing(15)
        # self.plot_scroll_layout.addWidget(self.plot_title)
        self.plot_scroll_layout.addWidget(self.plot_stack_menu)

        plot_scroll_area = QScrollArea(self.etb_plot_subpage)
        plot_scroll_area.setObjectName(u"plot_scroll_area")
        plot_scroll_area.setStyleSheet(u"background: transparent;")
        plot_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        # plot_scroll_area.setFrameShadow(QFrame.Shadow.Raised)
        plot_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        plot_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        plot_scroll_area.setWidgetResizable(True)
        plot_scroll_area.setWidget(plot_scroll_contents)

        self.plot_menu_center_layout = QVBoxLayout(self.etb_plot_subpage)
        self.plot_menu_center_layout.setSpacing(5)
        self.plot_menu_center_layout.setContentsMargins(5, 5, 5, 5)
        self.plot_menu_center_layout.setObjectName(u"etb_plot_layout")
        self.plot_menu_center_layout.addWidget(plot_scroll_area)

        self.pages.addWidget(self.etb_plot_subpage)

        ##############################
        #   Upload & Modeling Page   #
        ##############################
        self.data_model_selection_page = QWidget()
        self.data_model_selection_page.setObjectName("data_model_selection_page")

        self.data_model_content = QWidget()
        self.data_model_content.setObjectName("data_model_content")
        self.data_model_content.setGeometry(QRect(0, 0, 840, 580))
        self.data_model_content.setStyleSheet("background: transparent;")

        self.data_model_content_frame = QFrame(self.data_model_content)
        self.data_model_content_frame.setObjectName('data_model_content_frame')
        self.data_model_content_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.data_model_content_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.data_model_frame_layout = QHBoxLayout(self.data_model_content_frame)
        self.data_model_frame_layout.setObjectName('data_model_frame_layout')
        self.data_model_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.data_model_frame_layout.setSpacing(10)

        data_model_scroll_area = QScrollArea(self.data_model_selection_page)
        data_model_scroll_area.setObjectName("data_model_scroll_area")
        data_model_scroll_area.setStyleSheet("background: transparent;")
        data_model_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        data_model_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        data_model_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        data_model_scroll_area.setWidgetResizable(True)
        data_model_scroll_area.setWidget(self.data_model_content)

        self.data_model_title = QLabel(self.data_model_selection_page)
        self.data_model_title.setObjectName("data_model_title")
        self.data_model_title.setMaximumSize(QSize(16777215, 40))
        self.data_model_title.setStyleSheet("font-size: 18px; font-weight: bold; text-decoration: underline;")
        self.data_model_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.data_model_scroll_layout = QVBoxLayout(self.data_model_content)
        self.data_model_scroll_layout.setObjectName('data_model_scroll_layout')
        self.data_model_scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.data_model_scroll_layout.setSpacing(25)
        self.data_model_scroll_layout.addWidget(self.data_model_content_frame)

        self.data_model_page_layout = QVBoxLayout(self.data_model_selection_page)
        self.data_model_page_layout.setObjectName(u"result_page_layout")
        self.data_model_page_layout.setContentsMargins(15, 5, 15, 5)
        self.data_model_page_layout.setSpacing(5)
        self.data_model_page_layout.addWidget(self.data_model_title)
        self.data_model_page_layout.addWidget(data_model_scroll_area)

        self.pages.addWidget(self.data_model_selection_page)

        ##########################
        # Modeling Settings Page #
        ##########################
        self.modeling_settings_page = QWidget()
        self.modeling_settings_page.setObjectName("modeling_settings_page")

        self.modeling_settings_content = QWidget()
        self.modeling_settings_content.setObjectName("modeling_settings_content")
        self.modeling_settings_content.setGeometry(QRect(0, 0, 840, 580))
        self.modeling_settings_content.setStyleSheet("background: transparent;")

        self.modeling_content_frame = QFrame(self.modeling_settings_content)
        self.modeling_content_frame.setObjectName('modeling_content_frame')
        self.modeling_content_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.modeling_content_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.modeling_frame_layout = QHBoxLayout(self.modeling_content_frame)
        self.modeling_frame_layout.setObjectName('modeling_frame_layout')
        self.modeling_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.modeling_frame_layout.setSpacing(10)

        modeling_settings_scroll_area = QScrollArea(self.modeling_settings_page)
        modeling_settings_scroll_area.setObjectName("modeling_settings_scroll_area")
        modeling_settings_scroll_area.setStyleSheet("background: transparent;")
        modeling_settings_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        modeling_settings_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        modeling_settings_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        modeling_settings_scroll_area.setWidgetResizable(True)
        modeling_settings_scroll_area.setWidget(self.modeling_settings_content)

        self.modeling_settings_title = QLabel(self.modeling_settings_page)
        self.modeling_settings_title.setObjectName("modeling_settings_title")
        self.modeling_settings_title.setMaximumSize(QSize(16777215, 40))
        self.modeling_settings_title.setStyleSheet("font-size: 18px; font-weight: bold; text-decoration: underline;")
        self.modeling_settings_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.modeling_settings_scroll_layout = QVBoxLayout(self.modeling_settings_content)
        self.modeling_settings_scroll_layout.setObjectName('modeling_settings_scroll_layout')
        self.modeling_settings_scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.modeling_settings_scroll_layout.setSpacing(25)
        self.modeling_settings_scroll_layout.addWidget(self.modeling_content_frame)

        self.modeling_settings_page_layout = QVBoxLayout(self.modeling_settings_page)
        self.modeling_settings_page_layout.setObjectName("modeling_settings_page_layout")
        self.modeling_settings_page_layout.setContentsMargins(15, 5, 15, 5)
        self.modeling_settings_page_layout.setSpacing(5)
        self.modeling_settings_page_layout.addWidget(self.modeling_settings_title)
        self.modeling_settings_page_layout.addWidget(modeling_settings_scroll_area)

        self.pages.addWidget(self.modeling_settings_page)

        #############################
        # Enhanced Modeling Results #
        #############################
        self.enhanced_results_page = QWidget()
        self.enhanced_results_page.setObjectName("enhanced_results_page")

        self.enhanced_results_content = QWidget()
        self.enhanced_results_content.setObjectName("enhanced_results_content")
        self.enhanced_results_content.setGeometry(QRect(0, 0, 840, 580))
        self.enhanced_results_content.setStyleSheet("background: transparent;")

        self.results_content_frame = QFrame(self.enhanced_results_content)
        self.results_content_frame.setObjectName("results_content_frame")
        self.results_content_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.results_content_frame.setFrameShadow(QFrame.Shadow.Plain)

        self.results_content_layout = QHBoxLayout(self.results_content_frame)
        self.results_content_layout.setObjectName("results_content_layout")
        self.results_content_layout.setContentsMargins(0, 0, 0, 0)
        self.results_content_layout.setSpacing(10)

        enhanced_results_scroll_area = QScrollArea(self.enhanced_results_page)
        enhanced_results_scroll_area.setObjectName("enhanced_results_scroll_area")
        enhanced_results_scroll_area.setStyleSheet("background: transparent;")
        enhanced_results_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        enhanced_results_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        enhanced_results_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        enhanced_results_scroll_area.setWidgetResizable(True)
        enhanced_results_scroll_area.setWidget(self.enhanced_results_content)

        self.enhanced_results_title = QLabel(self.enhanced_results_page)
        self.enhanced_results_title.setObjectName("enhanced_results_title")
        self.enhanced_results_title.setMaximumSize(QSize(16777215, 40))
        self.enhanced_results_title.setStyleSheet("font-size: 18px; font-weight: bold; text-decoration: underline;")
        self.enhanced_results_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.enhanced_results_scroll_layout = QVBoxLayout(self.enhanced_results_content)
        self.enhanced_results_scroll_layout.setObjectName('enhanced_results_scroll_layout')
        self.enhanced_results_scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.enhanced_results_scroll_layout.setSpacing(25)
        self.enhanced_results_scroll_layout.addWidget(self.results_content_frame)

        self.enhanced_results_page_layout = QVBoxLayout(self.enhanced_results_page)
        self.enhanced_results_page_layout.setObjectName("enhanced_results_page_layout")
        self.enhanced_results_page_layout.setContentsMargins(15, 5, 15, 5)
        self.enhanced_results_page_layout.setSpacing(5)
        self.enhanced_results_page_layout.addWidget(self.enhanced_results_title)
        self.enhanced_results_page_layout.addWidget(enhanced_results_scroll_area)

        self.pages.addWidget(self.enhanced_results_page)

        # **************************************
        # *** Abstract Visualizer Page Setup ***
        # **************************************
        self.abstract_visualizer_page = QWidget()
        self.abstract_visualizer_page.setObjectName("abstract_visualizer_page")

        self.visualizer_scroll_content = QWidget()
        self.visualizer_scroll_content.setObjectName("visualizer_scroll_content")
        self.visualizer_scroll_content.setGeometry(QRect(0, 0, 840, 580))
        self.visualizer_scroll_content.setStyleSheet("background: transparent;")

        visualizer_scroll_area = QScrollArea(self.abstract_visualizer_page)
        visualizer_scroll_area.setObjectName("visualizer_scroll_area")
        visualizer_scroll_area.setStyleSheet("background: transparent;")
        visualizer_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        visualizer_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        visualizer_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        visualizer_scroll_area.setWidgetResizable(True)
        visualizer_scroll_area.setWidget(self.visualizer_scroll_content)

        self.visualizer_page_title = QLabel(self.abstract_visualizer_page)
        self.visualizer_page_title.setObjectName("visualizer_page_title")
        self.visualizer_page_title.setMaximumSize(QSize(16777215, 40))
        self.visualizer_page_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.visualizer_page_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.visualizer_page_title.hide()

        self.visualizer_scroll_layout = QVBoxLayout(self.visualizer_scroll_content)
        self.visualizer_scroll_layout.setObjectName('visualizer_scroll_layout')
        self.visualizer_scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.visualizer_scroll_layout.setSpacing(25)

        self.abstract_visualizer_page_layout = QVBoxLayout(self.abstract_visualizer_page)
        self.abstract_visualizer_page_layout.setObjectName("abstract_visualizer_page_layout")
        self.abstract_visualizer_page_layout.setContentsMargins(15, 5, 15, 5)
        self.abstract_visualizer_page_layout.setSpacing(5)
        self.abstract_visualizer_page_layout.addWidget(self.visualizer_page_title)
        self.abstract_visualizer_page_layout.addWidget(visualizer_scroll_area)

        self.pages.addWidget(self.abstract_visualizer_page)

        # Page 3 Frame/Layout creation
        self.rosetta_model_page = QWidget()
        self.rosetta_model_page.setObjectName(u"rosetta_page_1")
        self.rosetta_model_page.setStyleSheet(u"QFrame {\n"
            "	font-size: 16pt;\n"
            "}")

        self.page_3_layout = QVBoxLayout(self.rosetta_model_page)
        self.page_3_layout.setObjectName(u"page_3_layout")

        self.empty_page_label = QLabel(self.rosetta_model_page)
        self.empty_page_label.setObjectName(u"empty_page_label")
        self.empty_page_label.setFont(font)
        self.empty_page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.page_3_layout.addWidget(self.empty_page_label)

        #self.pages.addWidget(self.rosetta_model_page)

        self.main_pages_layout.addWidget(self.pages)


        self.retranslate_ui(MainPages)

        self.pages.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainPages)
    # setupUi

    def retranslate_ui(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
        self.import_data_title.setText(QCoreApplication.translate("MainPages", u"Upload Dataset", None))
        self.parameter_title.setText(QCoreApplication.translate("MainPages", u"Parameter Selection", None))
        self.empty_page_label.setText(QCoreApplication.translate("MainPages", u"Rosetta Page\nNot Yet Available", None))
        self.data_model_title.setText(QCoreApplication.translate("MainPages", u"Data Upload & Model Selection", None))
        self.modeling_settings_title.setText(QCoreApplication.translate("MainPages", u"Modeling Settings", None))
        self.enhanced_results_title.setText(QCoreApplication.translate("MainPages", u"Modeling Results", None))
    # retranslateUi
