# views/forms/scenario_form.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QSplitter, QMessageBox, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from widgets.highlight_text_edit import HighlightTextEdit
from utils.dotted_background import DottedBackgroundMixin

class ScenarioForm(QWidget, DottedBackgroundMixin):
    saved = pyqtSignal(dict)

    def __init__(self, parent=None, scenario=None):
        QWidget.__init__(self, parent, flags=Qt.Window)
        DottedBackgroundMixin.__init__(self)
        
        self.scenario = scenario
        self.setWindowTitle("Редактировать сценарий" if scenario else "Новый сценарий")
        self.resize(800, 900)
        self.setMinimumSize(600, 700)

        # Основной layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # --- Заголовок ---
        title_layout = QVBoxLayout()
        title_label = QLabel("Название:")
        self.title_input = QLineEdit()
        self.title_input.setMinimumHeight(30)
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_input)
        main_layout.addLayout(title_layout)

        # --- Сплиттер для описания и заметок ---
        content_splitter = QSplitter(Qt.Vertical)
        content_splitter.setChildrenCollapsible(False)
        
        # --- Описание ---
        desc_widget = QWidget()
        desc_layout = QVBoxLayout(desc_widget)
        desc_layout.setContentsMargins(0, 0, 0, 10)
        
        desc_label = QLabel("Основное описание:")
        self.desc_input = HighlightTextEdit()
        self.desc_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        desc_layout.addWidget(desc_label)
        desc_layout.addWidget(self.desc_input)
        content_splitter.addWidget(desc_widget)
        
        # --- Заметки ---
        note_widget = QWidget()
        note_layout = QVBoxLayout(note_widget)
        note_layout.setContentsMargins(0, 0, 0, 0)
        
        note_label = QLabel("Заметки:")
        self.note_input = HighlightTextEdit()
        self.note_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        note_layout.addWidget(note_label)
        note_layout.addWidget(self.note_input)
        content_splitter.addWidget(note_widget)
        
        # Настройки сплиттера
        content_splitter.setSizes([600, 300])
        content_splitter.setStyleSheet("QSplitter::handle { background-color: #8b7d6b; height: 1px; }")
        main_layout.addWidget(content_splitter, 1)

        # --- Кнопки ---
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.btn_save = QPushButton("Сохранить")
        self.btn_save.setFixedWidth(150)
        self.btn_save.setMinimumHeight(35)
        self.btn_save.clicked.connect(self._on_save)
        
        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.setFixedWidth(150)
        self.btn_cancel.setMinimumHeight(35)
        self.btn_cancel.clicked.connect(self.close)
        
        btn_layout.addWidget(self.btn_save)
        btn_layout.addSpacing(10)
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addStretch()
        
        main_layout.addLayout(btn_layout)

        # Заполняем данные, если передан сценарий
        if self.scenario:
            self.title_input.setText(self.scenario.title or "")
            self.desc_input.setPlainText(self.scenario.description or "")
            self.note_input.setPlainText(self.scenario.note or "")

    def _on_save(self):
        """Обработчик сохранения"""
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Ошибка", "Введите название сценария")
            return
            
        data = {
            'title': title,
            'description': self.desc_input.toPlainText().strip() or None,
            'note': self.note_input.toPlainText().strip() or None
        }
        
        self.saved.emit(data)
        self.close()