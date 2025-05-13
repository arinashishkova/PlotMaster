# views/forms/chapter_form.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, 
    QPushButton, QSplitter, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal

from widgets.highlight_text_edit import HighlightTextEdit
from utils.dotted_background import DottedBackgroundMixin

class ChapterForm(QWidget, DottedBackgroundMixin):
    # Добавляем сигналы как в CharacterForm
    saved = pyqtSignal(dict)
    accepted = pyqtSignal()
    rejected = pyqtSignal()

    def __init__(self, parent=None, scenario_id=None, chapter=None):
        QWidget.__init__(self, parent, flags=Qt.Window)
        DottedBackgroundMixin.__init__(self)
        
        self.scenario_id = scenario_id
        self.chapter = chapter
        self.setWindowTitle("Редактировать главу" if chapter else "Новая глава")
        self.resize(720, 1280)
        self.setMinimumSize(500, 400)

        # Основной вертикальный layout
        main = QVBoxLayout(self)
        main.setSpacing(15)

        # --- Блок заголовка ---
        title_layout = QVBoxLayout()
        title_label = QLabel("Заголовок:")
        title_layout.addWidget(title_label)
        
        self.title_input = QLineEdit()
        self.title_input.setMinimumHeight(30)
        title_layout.addWidget(self.title_input)
        
        main.addLayout(title_layout)
        
        # --- Сплиттер для содержания и заметки ---
        content_splitter = QSplitter(Qt.Vertical)
        content_splitter.setChildrenCollapsible(False)
        
        # --- Блок содержания ---
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 10)
        
        content_label = QLabel("Содержание:")
        content_layout.addWidget(content_label)
        
        self.desc_input = HighlightTextEdit()
        self.desc_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_layout.addWidget(self.desc_input)
        
        content_splitter.addWidget(content_widget)
        
        # --- Блок заметки ---
        note_widget = QWidget()
        note_layout = QVBoxLayout(note_widget)
        note_layout.setContentsMargins(0, 0, 0, 0)
        
        note_label = QLabel("Заметка:")
        note_layout.addWidget(note_label)
        
        self.note_input = HighlightTextEdit()
        self.note_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        note_layout.addWidget(self.note_input)
        
        content_splitter.addWidget(note_widget)
        
        # Устанавливаем начальные размеры (содержание - больше, заметка - меньше)
        content_splitter.setSizes([800, 200])
        content_splitter.setStyleSheet("QSplitter::handle { background-color: #8b7d6b; width: 1px; }")
        
        main.addWidget(content_splitter, 1)  # 1 - это stretch factor, даём больше места для сплиттера
        
        # --- Блок кнопок ---
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()  # Растягивание слева для центрирования
        
        btn_ok = QPushButton("Сохранить")
        btn_cancel = QPushButton("Отмена")
        
        # Устанавливаем фиксированную ширину для кнопок
        btn_ok.setFixedWidth(200)
        btn_cancel.setFixedWidth(200)
        
        # Устанавливаем минимальную высоту для кнопок
        btn_ok.setMinimumHeight(35)
        btn_cancel.setMinimumHeight(35)
        
        btn_ok.clicked.connect(self._on_save)
        btn_cancel.clicked.connect(self.reject)
        
        btn_layout.addWidget(btn_ok)
        btn_layout.addSpacing(5)  # Расстояние между кнопками
        btn_layout.addWidget(btn_cancel)
        btn_layout.addStretch()  # Растягивание справа для центрирования
        
        main.addLayout(btn_layout)
        
        # Заполняем поля, если передана глава для редактирования
        if chapter:
            self.title_input.setText(chapter.title or "")
            self.desc_input.setPlainText(chapter.description or "")
            self.note_input.setPlainText(chapter.note or "")

    def _on_save(self):
        """Обработчик кнопки сохранения"""
        data = self.get_data()
        self.saved.emit(data)
        self.accepted.emit()
        self.close()

    def accept(self):
        """Метод для совместимости с QDialog"""
        self._on_save()
        return True

    def reject(self):
        """Метод для совместимости с QDialog"""
        self.rejected.emit()
        self.close()
        return False

    def exec_(self):
        """Метод для обратной совместимости с предыдущей версией, 
        возвращает всегда True для упрощения перехода"""
        self.show()
        return True

    def get_data(self):
        """Получение данных из формы"""
        return {
            "title": self.title_input.text().strip(),
            "description": self.desc_input.toPlainText().strip() or None,
            "note": self.note_input.toPlainText().strip() or None,
            "scenario": self.scenario_id
        }