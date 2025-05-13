# controllers/artifact_controller.py

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem, QHBoxLayout
from utils.dotted_background import DottedBackgroundMixin
from widgets.delete_dialog import DeleteDialog
from widgets.message_dialog import WarningDialog

from models.artifact import Artifact
from views.forms.artifact_form import ArtifactForm

class ArtifactController:
    def __init__(self, view, get_current_scenario_fn):
        self.view = view
        self._get_scenario = get_current_scenario_fn

        self.tab = self.view.detail.artifacts_tab

        self.tab.btn_new_art.clicked.connect(self.on_new_artifact)
        self.tab.btn_edit_art.clicked.connect(self.on_edit_artifact)
        self.tab.btn_delete_art.clicked.connect(self.on_delete_artifact)
        self.tab.art_list.currentItemChanged.connect(self.on_art_selected)

    def load_artifacts(self):
        """Загружает артефакты текущего сценария в алфавитном порядке (без учета регистра)."""
        scen = self._get_scenario()
        if not scen:
            return

        # Получаем артефакты и сортируем по имени без учета регистра
        artifacts = (Artifact
                    .select()
                    .where(Artifact.scenario == scen)
                    .order_by(Artifact.name.collate('NOCASE')))

        # Обновляем список артефактов
        lw = self.tab.art_list
        lw.clear()
        for art in artifacts:
            it = QListWidgetItem(art.name)
            it.setData(Qt.UserRole, art.id)
            lw.addItem(it)

        # Сбрасываем детали
        self.tab.art_title.clear()
        self.tab.art_desc.clear()
        self.tab.art_note.clear()

    def on_art_selected(self, current, previous):
        """При выборе артефакта показывает его название, описание и заметку."""
        if not current:
            self.tab.art_title.clear()
            self.tab.art_desc.clear()
            self.tab.art_note.clear()
            return

        art_id = current.data(Qt.UserRole)
        art = Artifact.get_by_id(art_id)
        self.tab.art_title.setText(art.name)
        self.tab.art_desc.setPlainText(art.description or "")
        self.tab.art_note.setPlainText(art.note or "")

    def on_new_artifact(self):
        """Открывает немодальное окно создания артефакта."""
        scen = self._get_scenario()
        if not scen:
            WarningDialog(
                parent=self.view,
                title="Внимание",
                message="Сначала выберите сценарий"
            ).exec_()
            return

        form = ArtifactForm(parent=self.view, scenario_id=scen.id)
        form.saved.connect(self._create_artifact)
        form.show()

    def _create_artifact(self, data):
        """Создает новый артефакт и обновляет список."""
        try:
            Artifact.create(**data)
            self.load_artifacts()
        except Exception as e:
            WarningDialog(
                parent=self.view,
                title="Ошибка",
                message=f"Не удалось создать артефакт: {str(e)}"
            ).exec_()

    def on_edit_artifact(self):
        """Открывает немодальное окно редактирования артефакта."""
        sel = self.tab.art_list.currentItem()
        if not sel:
            WarningDialog(
                parent=self.view,
                title="Внимание",
                message="Выберите артефакт для редактирования"
            ).exec_()
            return

        art_id = sel.data(Qt.UserRole)
        art = Artifact.get_by_id(art_id)
        form = ArtifactForm(
            parent=self.view,
            scenario_id=self._get_scenario().id,
            artifact=art
        )
        form.saved.connect(lambda data, art=art: self._update_artifact(art, data))
        form.show()

    def _update_artifact(self, art, data):
        """Обновляет данные артефакта и обновляет список."""
        try:
            for key, val in data.items():
                setattr(art, key, val)
            art.save()
            self.load_artifacts()
        except Exception as e:
            WarningDialog(
                parent=self.view,
                title="Ошибка",
                message=f"Не удалось обновить артефакт: {str(e)}"
            ).exec_()

    def on_delete_artifact(self):
        """Удаляет артефакт с подтверждением."""
        sel = self.tab.art_list.currentItem()
        if not sel:
            WarningDialog(
                parent=self.view,
                title="Внимание",
                message="Выберите артефакт для удаления"
            ).exec_()
            return

        art = Artifact.get_by_id(sel.data(Qt.UserRole))
        
        dialog = DeleteDialog(
            parent=self.view,
            message=art.name,
            object_type="артефакт"
        )
        dialog.exec_()
        
        if dialog.clickedButton() == dialog.yes_button:
            try:
                art.delete_instance()
                self.load_artifacts()
            except Exception as e:
                WarningDialog(
                    parent=self.view,
                    title="Ошибка",
                    message=f"Не удалось удалить артефакт: {str(e)}"
                ).exec_()