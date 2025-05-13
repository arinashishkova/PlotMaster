# controllers/relation_controller.py

from PyQt5.QtCore    import Qt
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem

from models.relation_type       import RelationType
from models.character_relation  import CharacterRelation
from views.forms.relation_form  import RelationForm
from widgets.delete_dialog import DeleteDialog
from database import db
from models.character import Character

class RelationController:
    def __init__(self, view, get_current_scenario_fn):
        """
        view                  — экземпляр MainWindow
        get_current_scenario_fn — функция, возвращающая текущий Scenario
        """
        self.view          = view
        self._get_scenario = get_current_scenario_fn
        self.tab           = self.view.detail.relations_tab

        # Подключаем сигналы к реальным именам кнопок из TabRelations
        self.tab.char_list.currentItemChanged    .connect(self.on_char_selected)
        self.tab.rel_type_list.currentItemChanged.connect(self.on_relation_type_selected)
        self.tab.btn_add   .clicked.connect(self.on_add_relation)
        self.tab.btn_edit  .clicked.connect(self.on_edit_relation)
        self.tab.btn_delete.clicked.connect(self.on_delete_relation)

    def load_relations(self):
        """
        Перезагрузить всё содержимое вкладки «Связи» для текущего выбранного персонажа.
        Вызывается из MainController.update_all_tabs().
        """
        # Сбрасываем список типов и участников
        self.tab.rel_type_list.clear()
        self.tab.participants_list.clear()
        # "Имитируем" повторный выбор персонажа, чтобы спуститься по логике on_char_selected
        current = self.tab.char_list.currentItem()
        self.on_char_selected(current, None)

    def on_char_selected(self, current, previous):
        """
        При выборе персонажа-источника заполняем список типов связей, которые у него есть.
        """
        self.tab.rel_type_list.clear()
        self.tab.participants_list.clear()
        if not current:
            return

        source_id = current.data(Qt.UserRole)
        # Все RelationType, в которые этот персонаж участвует как source
        types = (RelationType
                 .select()
                 .join(CharacterRelation)
                 .where(CharacterRelation.source == source_id)
                 .distinct())
        for rt in types:
            item = QListWidgetItem(rt.name)
            item.setData(Qt.UserRole, rt.id)
            self.tab.rel_type_list.addItem(item)

    def on_relation_type_selected(self, current, previous):
        """
        При выборе типа связи показываем участников этой связи.
        """
        self.tab.participants_list.clear()
        if not current:
            return

        src_item = self.tab.char_list.currentItem()
        if not src_item:
            return

        source_id = src_item.data(Qt.UserRole)
        rt_id     = current.data(Qt.UserRole)

        rels = CharacterRelation.select().where(
            (CharacterRelation.source == source_id) &
            (CharacterRelation.relation_type == rt_id)
        )
        for rel in rels:
            tgt = rel.target
            item = QListWidgetItem(tgt.name)
            item.setData(Qt.UserRole, tgt.id)
            self.tab.participants_list.addItem(item)

    def on_add_relation(self):
        """Открыть форму создания новой связи."""
        src_item = self.tab.char_list.currentItem()
        if not src_item:
            QMessageBox.warning(self.view, "Внимание", "Сначала выберите персонажа-источник")
            return

        source_id = src_item.data(Qt.UserRole)
        form = RelationForm(
            parent=self.view,
            scenario_id=self._get_scenario().id,
            source_id=source_id
        )
        form.saved.connect(
            lambda rel_type, targets: self._create_relation(source_id, rel_type, targets)
        )
        form.show()

    def _create_relation(self, source_id, rel_type_name, target_ids):
        """Слот: создаём RelationType (или берём существующий) и связи CharacterRelation."""
        scen = self._get_scenario()
        rt, _ = RelationType.get_or_create(name=rel_type_name, scenario=scen)
        for tid in target_ids:
            CharacterRelation.create(source=source_id, target=tid, relation_type=rt)
        self.load_relations()

    def on_edit_relation(self):
        """Открыть форму редактирования выбранного типа связи."""
        src_item  = self.tab.char_list.currentItem()
        type_item = self.tab.rel_type_list.currentItem()
        if not src_item or not type_item:
            QMessageBox.warning(self.view, "Внимание", "Выберите персонажа и тип связи")
            return

        source_id = src_item.data(Qt.UserRole)
        rt = RelationType.get_by_id(type_item.data(Qt.UserRole))

        form = RelationForm(
            parent=self.view,
            scenario_id=self._get_scenario().id,
            source_id=source_id,
            relation=rt
        )
        form.saved.connect(
            lambda new_name, targets: self._update_relation(source_id, rt, new_name, targets)
        )
        form.show()

    def _update_relation(self, source_id, old_rt, new_name, target_ids):
        """
        Слот: обновляем имя типа связи (если изменилось) и участников.
        Старые связи по old_rt удаляются.
        """
        scen = self._get_scenario()
        # Если имя изменилось — создаём/получаем новый RelationType
        if new_name != old_rt.name:
            rt, _ = RelationType.get_or_create(name=new_name, scenario=scen)
        else:
            rt = old_rt

        # Удаляем старые связи этого типа
        CharacterRelation.delete().where(
            (CharacterRelation.source == source_id) &
            (CharacterRelation.relation_type == old_rt)
        ).execute()

        # Добавляем обновлённые
        for tid in target_ids:
            CharacterRelation.create(source=source_id, target=tid, relation_type=rt)

        self.load_relations()

    def on_delete_relation(self):
        """Удаляет тип связи с подтверждением"""
        src_item = self.tab.char_list.currentItem()
        type_item = self.tab.rel_type_list.currentItem()
        
        if not src_item or not type_item:
            QMessageBox.warning(self.view, "Внимание", "Выберите персонажа и тип связи")
            return

        character = Character.get_by_id(src_item.data(Qt.UserRole))
        relation_type = RelationType.get_by_id(type_item.data(Qt.UserRole))

        # Создаем диалог с точным текстом по вашему требованию
        dialog = DeleteDialog(
            parent=self.view,
            message=f"Удалить связь {relation_type.name} у персонажа {character.name}",
            object_type=""  # Оставляем пустым, так как сообщение уже полное
        )
        
        # Показываем диалог и ждем результата
        dialog.exec_()
        
        # Проверяем, была ли нажата кнопка "Да"
        if dialog.clickedButton() == dialog.yes_button:
            try:
                with db.atomic():  # Используем транзакцию для безопасности
                    # Удаляем все связи этого типа
                    CharacterRelation.delete().where(
                        (CharacterRelation.source == character.id) &
                        (CharacterRelation.relation_type == relation_type)
                    ).execute()
                    
                    # Удаляем сам тип связи
                    relation_type.delete_instance()
                    
                    # Обновляем интерфейс
                    self.load_relations()
                    
            except Exception as e:
                QMessageBox.critical(
                    self.view,
                    "Ошибка",
                    f"Не удалось удалить связь: {str(e)}"
                )