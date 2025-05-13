# controllers/main_controller.py

from PyQt5.QtWidgets import QMessageBox, QMainWindow
from PyQt5.QtCore import Qt
from models.scenario import Scenario

from controllers.scenario_controller import ScenarioController
from controllers.character_controller import CharacterController
from controllers.chapter_controller import ChapterController
from controllers.artifact_controller import ArtifactController
from controllers.location_controller import LocationController
from controllers.event_controller import EventController
from controllers.genre_controller import GenreController
from controllers.manage_genre_controller import ManageGenreController
from controllers.relation_controller import RelationController
from controllers.save_load_controller import SaveLoadController

from views.overview_view import ScenarioOverview
from views.genre_management_dialog import GenreManagementForm

class MainController:
    def __init__(self, window):
        self.view = window
        self.current_scenario = None

        # Инициализация контроллеров
        self.init_controllers()
        
        # Настройка навигации
        self.setup_navigation()
        
        # Стартовый экран
        self.view.show_welcome()

    def init_controllers(self):
        """Инициализация всех контроллеров"""
        self.scenario_ctrl = ScenarioController(
            view=self.view,
            on_select_fn=self.show_scenario_detail,
            on_manage_genres_fn=self.open_manage_genres
        )
        
        self.character_ctrl = CharacterController(
            view=self.view,
            get_current_scenario_fn=lambda: self.current_scenario
        )
        
        self.chapter_ctrl = ChapterController(
            view=self.view,
            get_current_scenario_fn=lambda: self.current_scenario
        )
        
        self.art_ctrl = ArtifactController(
            view=self.view,
            get_current_scenario_fn=lambda: self.current_scenario
        )
        
        self.loc_ctrl = LocationController(
            view=self.view,
            get_current_scenario_fn=lambda: self.current_scenario
        )
        
        self.ev_ctrl = EventController(
            view=self.view,
            get_current_scenario_fn=lambda: self.current_scenario
        )
        
        self.genre_ctrl = GenreController(self.view)
        
        self.relation_ctrl = RelationController(
            view=self.view,
            get_current_scenario_fn=lambda: self.current_scenario
        )
        
        self.save_load_ctrl = SaveLoadController(
            view=self.view,
            scenario_controller=self.scenario_ctrl
        )

    def setup_navigation(self):
        """Настройка соединений сигналов и слотов"""
        w = self.view.welcome
        w.btn_start.clicked.connect(self.handle_start)
        w.btn_about.clicked.connect(self.view.show_about)
        w.btn_exit.clicked.connect(self.exit_app)

        self.view.scenario.btn_home.clicked.connect(self.view.show_welcome)
        self.view.about.btn_back.clicked.connect(self.view.show_welcome)
        self.view.detail.btn_back.clicked.connect(self.view.show_scenario)
        self.view.detail.btn_overview.clicked.connect(self.show_overview)

    def handle_start(self):
        """Обработчик кнопки 'Начать'"""
        self.scenario_ctrl.load_scenarios()
        self.view.show_scenario()
    
    def exit_app(self):
        """Закрытие приложения с подтверждением"""
        msg_box = QMessageBox(self.view)
        msg_box.setWindowTitle('Подтверждение выхода')
        msg_box.setText('Вы уверены, что хотите выйти из программы?')
        msg_box.setIcon(QMessageBox.Question)
        
        # Настройка русскоязычных кнопок
        yes_button = msg_box.addButton("Да", QMessageBox.YesRole)
        no_button = msg_box.addButton("Нет", QMessageBox.NoRole)
        msg_box.setDefaultButton(no_button)
        
        msg_box.exec_()
    
        if msg_box.clickedButton() == yes_button:
            self.view.close()

    def show_scenario_detail(self, scen: Scenario):
        """Показ деталей сценария"""
        self.current_scenario = scen

        dp = self.view.detail
        dp.lbl_title.setText(scen.title)
        dp.lbl_description.setText(scen.description or "")
        dp.lbl_notes.setText(scen.note or "")

        # Обновление всех вкладок
        self.update_all_tabs()
        
        self.view.show_detail()

    def update_all_tabs(self):
        """Обновление всех вкладок данных"""
        self.character_ctrl.load_characters()
        self.chapter_ctrl.load_chapters()
        self.art_ctrl.load_artifacts()
        self.loc_ctrl.load_locations()  
        self.ev_ctrl.load()
        self.genre_ctrl.load_genres()
        self.relation_ctrl.load_relations()

    def open_manage_genres(self):
        """Открытие формы управления жанрами"""
        form = GenreManagementForm(parent=self.view)
        form.show()
        
        # Обновляем список жанров в текущем сценарии, если он выбран
        if self.current_scenario:
            self.genre_ctrl.load_genres()

    def show_overview(self):
        """Показ полного обзора сценария"""
        if not self.current_scenario:
            QMessageBox.warning(self.view, "Внимание", "Сначала выберите сценарий")
            return

        dlg = ScenarioOverview(parent=self.view, scenario=self.current_scenario)
        dlg.exec_()