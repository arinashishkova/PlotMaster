# controllers/character_controller.py

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem

from models.character import Character
from views.forms.character_form import CharacterForm
from widgets.delete_dialog import DeleteDialog
from widgets.message_dialog import WarningDialog
from database import db

class CharacterController:
    def __init__(self, view, get_current_scenario_fn):
        self.view = view
        self._get_scenario = get_current_scenario_fn

        self.tab = self.view.detail.characters_tab

        self.tab.btn_new_char.clicked.connect(self.on_new_character)
        self.tab.btn_edit_char.clicked.connect(self.on_edit_character)
        self.tab.btn_delete_char.clicked.connect(self.on_delete_character)
        self.tab.char_list.currentItemChanged.connect(self.on_char_selected)

    def load_characters(self):
        """Загружает персонажей текущего сценария в алфавитном порядке (без учета регистра)."""
        scen = self._get_scenario()
        if not scen:
            return

        # Получаем персонажей и сортируем по имени без учета регистра
        characters = (Character
                    .select()
                    .where(Character.scenario == scen)
                    .order_by(Character.name.collate('NOCASE')))

        # Обновляем список персонажей
        lw = self.tab.char_list
        lw.clear()
        for ch in characters:
            it = QListWidgetItem(ch.name)
            it.setData(Qt.UserRole, ch.id)
            lw.addItem(it)

        # Сбрасываем детали
        self.tab.lbl_char_name.clear()
        self.tab.lbl_char_role.clear()
        self.tab.char_desc.clear()
        self.tab.char_note.clear()

        # Обновляем список в вкладке «Отношения»
        try:
            rel_tab = self.view.detail.relations_tab
            rel_tab.char_list.clear()
            for ch in characters:
                it = QListWidgetItem(ch.name)
                it.setData(Qt.UserRole, ch.id)
                rel_tab.char_list.addItem(it)
        except AttributeError:
            pass

    # Остальные методы остаются без изменений
    def on_char_selected(self, current, previous):
        """При выборе персонажа показывает его имя, роль, описание и заметку."""
        if not current:
            self.tab.lbl_char_name.clear()
            self.tab.lbl_char_role.clear()
            self.tab.char_desc.clear()
            self.tab.char_note.clear()
            return

        cid = current.data(Qt.UserRole)
        ch = Character.get_by_id(cid)
        self.tab.lbl_char_name.setText(ch.name)
        self.tab.lbl_char_role.setText(ch.role or "")
        self.tab.char_desc.setPlainText(ch.description or "")
        self.tab.char_note.setPlainText(ch.note or "")

    def on_new_character(self):
        """Открывает немодальное окно создания персонажа."""
        scen = self._get_scenario()
        if not scen:
            WarningDialog(
                parent=self.view,
                title="Внимание",
                message="Сначала выберите сценарий"
            ).exec_()
            return

        form = CharacterForm(parent=self.view, scenario_id=scen.id)
        form.saved.connect(self._create_character)
        form.show()

    def _create_character(self, data):
        """Создает нового персонажа и обновляет списки."""
        try:
            Character.create(**data)
            self.load_characters()
        except Exception as e:
            WarningDialog(
                parent=self.view,
                title="Ошибка",
                message=f"Не удалось создать персонажа: {str(e)}"
            ).exec_()

    def on_edit_character(self):
        """Открывает немодальное окно редактирования персонажа."""
        sel = self.tab.char_list.currentItem()
        if not sel:
            WarningDialog(
                parent=self.view,
                title="Внимание",
                message="Выберите персонажа для редактирования"
            ).exec_()
            return

        cid = sel.data(Qt.UserRole)
        ch = Character.get_by_id(cid)
        form = CharacterForm(
            parent=self.view,
            scenario_id=self._get_scenario().id,
            character=ch
        )
        form.saved.connect(lambda data, ch=ch: self._update_character(ch, data))
        form.show()

    def _update_character(self, ch, data):
        """Обновляет данные персонажа и обновляет списки."""
        try:
            for key, val in data.items():
                setattr(ch, key, val)
            ch.save()
            self.load_characters()
        except Exception as e:
            WarningDialog(
                parent=self.view,
                title="Ошибка",
                message=f"Не удалось обновить персонажа: {str(e)}"
            ).exec_()

    def on_delete_character(self):
        """Удаляет персонажа с подтверждением."""
        sel = self.tab.char_list.currentItem()
        if not sel:
            WarningDialog(
                parent=self.view,
                title="Внимание",
                message="Выберите персонажа для удаления"
            ).exec_()
            return

        character = Character.get_by_id(sel.data(Qt.UserRole))
        
        dialog = DeleteDialog(
            parent=self.view,
            message=character.name,
            object_type="персонажа"
        )
        
        dialog.exec_()
        
        if dialog.clickedButton() == dialog.yes_button:
            try:
                with db.atomic():
                    character.delete_instance(recursive=True)
                    self.load_characters()
            except Exception as e:
                WarningDialog(
                    parent=self.view,
                    title="Ошибка",
                    message=f"Не удалось удалить персонажа: {str(e)}"
                ).exec_()