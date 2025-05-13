# views/forms/relation_form.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from utils.dotted_background import DottedBackgroundMixin

class RelationForm(QWidget, DottedBackgroundMixin):
    saved = pyqtSignal(str, list)  # Тип связи, список ID персонажей

    def __init__(self, parent=None, scenario_id=None, source_id=None, relation=None):
        QWidget.__init__(self, parent, flags=Qt.Window)
        DottedBackgroundMixin.__init__(self)
        
        self.scenario_id = scenario_id
        self.source_id = source_id
        self.relation = relation
        
        self.setWindowTitle("Редактировать связь" if relation else "Новая связь")
        self.resize(600, 700)
        self.setMinimumSize(500, 500)

        # Основной layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # --- Тип связи ---
        type_layout = QVBoxLayout()
        type_label = QLabel("Тип связи:")
        self.type_input = QLineEdit()
        self.type_input.setMinimumHeight(30)
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_input)
        main_layout.addLayout(type_layout)

        # --- Список персонажей ---
        chars_label = QLabel("Персонажи:")
        self.chars_list = QListWidget()
        self.chars_list.setSelectionMode(QListWidget.MultiSelection)
        main_layout.addWidget(chars_label)
        main_layout.addWidget(self.chars_list, 1)

        # --- Кнопки ---
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.btn_save = QPushButton("Сохранить")
        self.btn_save.setFixedWidth(200)
        self.btn_save.setMinimumHeight(35)
        self.btn_save.clicked.connect(self._on_save)
        
        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.setFixedWidth(200)
        self.btn_cancel.setMinimumHeight(35)
        self.btn_cancel.clicked.connect(self.close)
        
        btn_layout.addWidget(self.btn_save)
        btn_layout.addSpacing(10)
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addStretch()
        
        main_layout.addLayout(btn_layout)

        # Загрузка данных
        self._load_data()

    def _load_data(self):
        """Загружает данные в форму"""
        from models.character import Character
        from models.character_relation import CharacterRelation

        # Заполняем список персонажей (исключая source)
        for ch in Character.select().where(
            (Character.scenario == self.scenario_id) & 
            (Character.id != self.source_id)
        ):
            it = QListWidgetItem(ch.name)
            it.setData(Qt.UserRole, ch.id)
            self.chars_list.addItem(it)

        # Если редактируем существующую связь
        if self.relation:
            self.type_input.setText(self.relation.name or "")
            
            # Отмечаем связанных персонажей
            relations = CharacterRelation.select().where(
                (CharacterRelation.source == self.source_id) &
                (CharacterRelation.relation_type == self.relation)
            )
            
            target_ids = [rel.target.id for rel in relations]
            for i in range(self.chars_list.count()):
                if self.chars_list.item(i).data(Qt.UserRole) in target_ids:
                    self.chars_list.item(i).setSelected(True)

    def _on_save(self):
        """Обработчик сохранения"""
        relation_type = self.type_input.text().strip()
        if not relation_type:
            QMessageBox.warning(self, "Ошибка", "Введите тип связи")
            return
            
        target_ids = [
            self.chars_list.item(i).data(Qt.UserRole)
            for i in range(self.chars_list.count())
            if self.chars_list.item(i).isSelected()
        ]
        
        if not target_ids:
            QMessageBox.warning(self, "Ошибка", "Выберите хотя бы одного персонажа")
            return
            
        self.saved.emit(relation_type, target_ids)
        self.close()