# views/main_window.py

from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt
from utils.dotted_background import DottedBackgroundMixin

class MainWindow(QMainWindow, DottedBackgroundMixin):
    def __init__(self):
        QMainWindow.__init__(self)
        DottedBackgroundMixin.__init__(self)
        
        self.setWindowTitle("PlotMaster")
        self.resize(1280, 920)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # Подготовим страницы и стек
        self.init_pages()
        self.setup_stack()

    def init_pages(self):
        from views.welcome_page import WelcomePage
        from views.scenario_page import ScenarioPage
        from views.about_page import AboutPage
        from views.scenario_detail_page import ScenarioDetailPage

        self.welcome = WelcomePage()
        self.scenario = ScenarioPage()
        self.about = AboutPage()
        self.detail = ScenarioDetailPage()

    def setup_stack(self):
        self.stack = QStackedWidget()
        self.stack.addWidget(self.welcome)   # 0
        self.stack.addWidget(self.scenario)  # 1
        self.stack.addWidget(self.about)     # 2
        self.stack.addWidget(self.detail)    # 3
        self.setCentralWidget(self.stack)

    def show_welcome(self):
        self.stack.setCurrentWidget(self.welcome)

    def show_scenario(self):
        self.stack.setCurrentWidget(self.scenario)

    def show_about(self):
        self.stack.setCurrentWidget(self.about)

    def show_detail(self):
        self.stack.setCurrentWidget(self.detail)