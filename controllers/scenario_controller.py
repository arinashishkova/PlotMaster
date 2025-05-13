# controllers/scenario_controller.py

from PyQt5.QtCore    import Qt
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem

from models.scenario          import Scenario
from views.forms.scenario_form import ScenarioForm
from widgets.delete_dialog    import DeleteDialog
from widgets.message_dialog  import WarningDialog
from database                 import db


class ScenarioController:
    def __init__(self, view, on_select_fn, on_manage_genres_fn):
        self.view = view
        self.on_select_callback = on_select_fn
        self.on_manage_genres   = on_manage_genres_fn

        sp = self.view.scenario
        sp.list.currentItemChanged.connect(self.display_scenario_details)
        sp.btn_new.clicked.connect(self.on_new_scenario)
        sp.btn_edit.clicked.connect(self.on_edit_scenario)
        sp.btn_delete.clicked.connect(self.on_delete_scenario)
        sp.btn_continue.clicked.connect(self.on_continue_scenario)
        sp.btn_manage_genres.clicked.connect(self.on_manage_genres)

    def load_scenarios(self):
        """Загружает список всех сценариев."""
        lw = self.view.scenario.list
        lw.clear()
        for scen in Scenario.select().order_by(Scenario.title):
            item = QListWidgetItem(scen.title)
            item.setData(Qt.UserRole, scen.id)
            lw.addItem(item)
        self.clear_scenario_details()

    def clear_scenario_details(self):
        """Очищает поля описания/заметок/жанров."""
        sp = self.view.scenario
        sp.desc_view.clear()
        sp.note_view.clear()
        sp.genre_list.clear()

    def display_scenario_details(self, current, previous):
        """Показывает описание/заметки/жанры выбранного сценария."""
        if not current:
            return self.clear_scenario_details()

        scen = Scenario.get_by_id(current.data(Qt.UserRole))
        sp   = self.view.scenario

        sp.desc_view.setPlainText(scen.description or "")
        sp.note_view.setPlainText(scen.note        or "")

        sp.genre_list.clear()
        for sg in scen.scenario_genres:
            sp.genre_list.addItem(sg.genre.name)

    def on_new_scenario(self):
        """Новый сценарий через ScenarioForm."""
        form = ScenarioForm(parent=self.view)

        def _save(data):
            try:
                with db.atomic():
                    Scenario.create(**data)
                self.load_scenarios()
            except Exception as e:
                QMessageBox.critical(
                    self.view,
                    "Ошибка",
                    f"Не удалось создать сценарий:\n{e}",
                    QMessageBox.Ok
                )

        form.saved.connect(_save)
        form.show()

    def on_edit_scenario(self):
        """Редактирует выбранный сценарий."""
        current = self.view.scenario.list.currentItem()
        if not current:
            WarningDialog(
                parent=self.view,
                title="Внимание",
                message="Сначала выберите сценарий для редактирования"
            ).exec_()
            return

        scen = Scenario.get_by_id(current.data(Qt.UserRole))
        form = ScenarioForm(parent=self.view, scenario=scen)

        def _save(data):
            try:
                with db.atomic():
                    scen.title       = data['title']
                    scen.description = data.get('description')
                    scen.note        = data.get('note')
                    scen.save()
                self.load_scenarios()

            except Exception as e:
                QMessageBox.critical(
                    self.view,
                    "Ошибка",
                    f"Не удалось обновить сценарий:\n{e}",
                    QMessageBox.Ok
                )

        form.saved.connect(_save)
        form.show()

    def on_delete_scenario(self):
        """Удаляет выбранный сценарий с подтверждением."""
        current = self.view.scenario.list.currentItem()
        if not current:
            WarningDialog(
                parent=self.view,
                title="Внимание",
                message="Сначала выберите сценарий для удаления"
            ).exec_()
            return

        scen = Scenario.get_by_id(current.data(Qt.UserRole))
        dlg = DeleteDialog(
            parent=self.view,
            title="Подтвердите удаление сценария",
            message=scen.title,
            object_type="сценарий"
        )
        dlg.exec_()
        if dlg.clickedButton() is dlg.yes_button:
            try:
                with db.atomic():
                    scen.delete_instance(recursive=True)
                self.load_scenarios()

            except Exception as e:
                QMessageBox.critical(
                    self.view,
                    "Ошибка",
                    f"Не удалось удалить сценарий:\n{e}",
                    QMessageBox.Ok
                )

    def on_continue_scenario(self):
        """Переходит к работе с выбранным сценарием."""
        current = self.view.scenario.list.currentItem()
        if not current:
            WarningDialog(
                parent=self.view,
                title="Внимание",
                message="Сначала выберите сценарий для продолжения"
            ).exec_()
            return

        scen = Scenario.get_by_id(current.data(Qt.UserRole))

        # Обновляем заголовок/описание/заметки
        dv = self.view.detail
        dv.lbl_title      .setText(scen.title)
        dv.lbl_description.setText(scen.description or "")
        dv.lbl_notes      .setText(scen.note        or "")

        # Обновляем жанры
        genres = ", ".join(g.genre.name for g in scen.scenario_genres)
        dv.lbl_genres.setText(f"Жанры: {genres}" if genres else "Жанры: —")

        # Вызываем callback, который поднимет остальные вкладки
        self.on_select_callback(scen)
