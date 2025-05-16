# controllers/genre_controller.py

from sqlite3 import IntegrityError
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem

from models.scenario import Scenario
from models.genre import Genre
from models.scenario_genre import ScenarioGenre
from views.forms.genre_form import GenreForm
from views.forms.genre_scenario_form import GenreScenarioForm
from widgets.delete_dialog import DeleteDialog
from widgets.message_dialog import WarningDialog
from database import db


class GenreController:
    def __init__(self, view):
        self.view = view
        self.current_scenario = None

        sp = self.view.scenario
        sp.list.currentItemChanged.connect(self.on_scenario_selected)
        sp.btn_new_genre.clicked.connect(self.on_new_genre)
        sp.btn_add_genre.clicked.connect(self.on_add_genre)
        sp.btn_remove_genre.clicked.connect(self.on_remove_genre)

    def on_scenario_selected(self, current, previous):
        if current:
            sid = current.data(Qt.UserRole)
            self.current_scenario = Scenario.get_by_id(sid)
            self.load_genres()
        else:
            self.current_scenario = None
            self.view.scenario.genre_list.clear()

    # загрузка жанров к выбраному сценарию
    def load_genres(self):
        lw = self.view.scenario.genre_list
        lw.clear()
        for sg in ScenarioGenre.select().where(ScenarioGenre.scenario == self.current_scenario):
            g = sg.genre
            itm = QListWidgetItem(g.name)
            itm.setData(Qt.UserRole, g.id)
            lw.addItem(itm)

    # открытие окна создания жанра
    def on_new_genre(self):
        form = GenreForm(parent=self.view)
        form.saved.connect(self._create_genre)
        form.show()

    def _create_genre(self, data):
        """Слот: создавать новый жанр и обновлять списки."""
        name = data.get('name', '').strip()
        if not name:
            return

        try:
            Genre.create(name=name)
        except IntegrityError:
            WarningDialog(
                parent=self.view,
                title="Жанр уже существует",
                message=f"Жанр «{name}» уже есть в списке."
            ).exec_()

    # добавление жанра к теккущему сценарию
    def on_add_genre(self):
        if not self.current_scenario:
            WarningDialog(
                parent=self.view,
                title="Внимание",
                message="Сначала выберите сценарий"
            ).exec_()
            return

        # Собираем ID уже добавленных жанров
        used_ids = [
            sg.genre_id
            for sg in ScenarioGenre.select().where(ScenarioGenre.scenario == self.current_scenario)
        ]

        # Открываем форму на выбор из оставшихся
        form = GenreScenarioForm(
            parent=self.view,
            scenario=self.current_scenario,
            exclude_ids=used_ids
        )
        form.saved.connect(self._add_genre)
        form.show() 

    # привязывание жанра к сценарию и обновление списка
    def _add_genre(self, genre):
        try:
            ScenarioGenre.create(scenario=self.current_scenario, genre=genre)
            self.load_genres()
        except IntegrityError:
            WarningDialog(
                parent=self.view,
                title="Жанры",
                message=f"Жанр «{genre.name}» уже привязан к сценарию."
            ).exec_()
        except Exception as e:
            WarningDialog(
                parent=self.view,
                title="Ошибка",
                message=f"Не удалось добавить жанр: {e}"
            ).exec_()

    # удаление жанра из сценария
    def on_remove_genre(self):
        sel = self.view.scenario.genre_list.currentItem()
        if not sel:
            WarningDialog(
                parent=self.view,
                title="Внимание",
                message="Сначала выберите жанр"
            ).exec_()
            return

        gid = sel.data(Qt.UserRole)
        genre = Genre.get_by_id(gid)

        dialog = DeleteDialog(
            parent=self.view,
            message=genre.name,
            object_type="жанра"
        )
        dialog.exec_()

        if dialog.clickedButton() == dialog.yes_button:
            try:
                with db.atomic():
                    ScenarioGenre.delete().where(
                        (ScenarioGenre.scenario == self.current_scenario) &
                        (ScenarioGenre.genre == genre)
                    ).execute()
                self.load_genres()
            except Exception as e:
                WarningDialog(
                    parent=self.view,
                    title="Ошибка",
                    message=f"Не удалось удалить жанр: {e}"
                ).exec_()
