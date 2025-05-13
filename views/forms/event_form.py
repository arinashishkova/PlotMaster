# views/forms/event_form.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QSplitter, QListWidget, QListWidgetItem,
    QComboBox, QListView
)
from PyQt5.QtCore import Qt, pyqtSignal
from widgets.highlight_text_edit import HighlightTextEdit
from utils.dotted_background import DottedBackgroundMixin

class EventForm(QWidget, DottedBackgroundMixin):
    saved = pyqtSignal(dict)
    selections_changed = pyqtSignal(list, list)

    def __init__(self, parent=None, scenario_id=None, event=None):
        super().__init__(parent, flags=Qt.Window)
        DottedBackgroundMixin.__init__(self)

        self.scenario_id = scenario_id
        self.event = event

        self.setWindowTitle("Редактировать событие" if event else "Новое событие")
        self.resize(1280, 720)
        self.setMinimumSize(700, 600)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # --- Заголовок ---
        title_layout = QVBoxLayout()
        title_label = QLabel("Заголовок:")
        self.title_input = QLineEdit()
        self.title_input.setMinimumHeight(30)
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_input)
        main_layout.addLayout(title_layout)

        # --- Основной сплиттер ---
        main_splitter = QSplitter(Qt.Horizontal)

        # ---- Левая панель ----
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        # полностью без внешних отступов, чтобы вложенный chars_arts_splitter влево упёрся
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        # -- персонажи/артефакты --
        chars_arts_splitter = QSplitter(Qt.Vertical)

        # Персонажи
        chars_widget = QWidget()
        chars_layout = QVBoxLayout(chars_widget)
        # чуть отступ снизу и справа, если нужно
        chars_layout.setContentsMargins(0, 0, 10, 10)
        chars_label = QLabel("Персонажи:")
        self.char_list = QListWidget()
        self.char_list.setSelectionMode(QListWidget.MultiSelection)
        chars_layout.addWidget(chars_label)
        chars_layout.addWidget(self.char_list)
        chars_arts_splitter.addWidget(chars_widget)

        # Артефакты
        arts_widget = QWidget()
        arts_layout = QVBoxLayout(arts_widget)
        arts_layout.setContentsMargins(0, 0, 10, 10)
        arts_label = QLabel("Ключевые предметы:")
        self.art_list = QListWidget()
        self.art_list.setSelectionMode(QListWidget.MultiSelection)
        arts_layout.addWidget(arts_label)
        arts_layout.addWidget(self.art_list)
        chars_arts_splitter.addWidget(arts_widget)

        left_layout.addWidget(chars_arts_splitter)

        # -- локация --
        loc_label = QLabel("Локация:")
        self.loc_combo = QComboBox()
        self.loc_combo.setObjectName("locationComboBox")
        self.loc_combo.setMinimumHeight(30)
        # чтобы QSS точно применялось к popup
        self.loc_combo.setView(QListView(self.loc_combo))

        # контейнер для комбобокса с правым отступом 10px
        from PyQt5.QtWidgets import QVBoxLayout as _QVBox, QWidget as _W
        loc_container = _W()
        loc_layout = _QVBox(loc_container)
        # Добавляем отступ снизу для выравнивания с полем заметок 
        loc_layout.setContentsMargins(0, 0, 10, 10)
        loc_layout.setSpacing(5)
        loc_layout.addWidget(loc_label)
        loc_layout.addWidget(self.loc_combo)
        left_layout.addWidget(loc_container)

        main_splitter.addWidget(left_panel)

        # ---- Правая панель ----
        right_splitter = QSplitter(Qt.Vertical)

        # Описание
        desc_widget = QWidget()
        desc_layout = QVBoxLayout(desc_widget)
        # Устанавливаем нулевой отступ сверху для выравнивания с "Персонажи:"
        desc_layout.setContentsMargins(10, 0, 0, 10)
        desc_label = QLabel("Описание:")
        self.desc_input = HighlightTextEdit()
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_input)
        right_splitter.addWidget(desc_widget)

        # Заметки
        note_widget = QWidget()
        note_layout = QVBoxLayout(note_widget)
        # Добавляем отступ сверху, чтобы метка "Заметки:" была ниже
        note_layout.setContentsMargins(10, 10, 0, 0)
        note_label = QLabel("Заметки:")
        self.note_input = HighlightTextEdit()
        note_layout.addWidget(note_label)
        note_layout.addWidget(self.note_input)
        right_splitter.addWidget(note_widget)

        # задаём стартовые размеры: больше пространства для описания, меньше для заметок
        right_splitter.setSizes([700, 200])

        main_splitter.addWidget(right_splitter)
        # левая панель 1 часть, правая – 2 части
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 2)

        main_layout.addWidget(main_splitter, 1)

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

        # --- Загрузка данных ---
        self._load_data()

    def _load_data(self):
        from models.character import Character
        from models.artifact import Artifact
        from models.location import Location
        from models.event_character import EventCharacter
        from models.event_artifact import EventArtifact

        for ch in Character.select().where(Character.scenario == self.scenario_id):
            it = QListWidgetItem(ch.name)
            it.setData(Qt.UserRole, ch.id)
            self.char_list.addItem(it)

        for art in Artifact.select().where(Artifact.scenario == self.scenario_id):
            it = QListWidgetItem(art.name)
            it.setData(Qt.UserRole, art.id)
            self.art_list.addItem(it)

        self.loc_combo.addItem("- Не выбрано -", None)
        for loc in Location.select().where(Location.scenario == self.scenario_id):
            self.loc_combo.addItem(loc.name, loc.id)

        if self.event:
            self.title_input.setText(self.event.title or "")
            self.desc_input.setPlainText(self.event.description or "")
            self.note_input.setPlainText(self.event.note or "")

            if self.event.location:
                idx = self.loc_combo.findData(self.event.location.id)
                if idx >= 0:
                    self.loc_combo.setCurrentIndex(idx)

            char_ids = [ec.character.id for ec in
                        EventCharacter.select().where(EventCharacter.event == self.event)]
            for i in range(self.char_list.count()):
                if self.char_list.item(i).data(Qt.UserRole) in char_ids:
                    self.char_list.item(i).setSelected(True)

            art_ids = [ea.artifact.id for ea in
                       EventArtifact.select().where(EventArtifact.event == self.event)]
            for i in range(self.art_list.count()):
                if self.art_list.item(i).data(Qt.UserRole) in art_ids:
                    self.art_list.item(i).setSelected(True)

    def _on_save(self):
        data = {
            'title': self.title_input.text().strip(),
            'description': self.desc_input.toPlainText().strip() or None,
            'note': self.note_input.toPlainText().strip() or None,
            'scenario': self.scenario_id,
            'location': self.loc_combo.currentData()
        }

        char_ids = [
            self.char_list.item(i).data(Qt.UserRole)
            for i in range(self.char_list.count())
            if self.char_list.item(i).isSelected()
        ]
        art_ids = [
            self.art_list.item(i).data(Qt.UserRole)
            for i in range(self.art_list.count())
            if self.art_list.item(i).isSelected()
        ]

        self.saved.emit(data)
        self.selections_changed.emit(char_ids, art_ids)
        self.close()