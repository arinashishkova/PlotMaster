# views/forms/location_form.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, 
    QPushButton, QSplitter, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from widgets.highlight_text_edit import HighlightTextEdit
from utils.dotted_background import DottedBackgroundMixin

class LocationForm(QWidget, DottedBackgroundMixin):
    saved = pyqtSignal(dict)

    def __init__(self, parent=None, scenario_id=None, location=None):
        QWidget.__init__(self, parent, flags=Qt.Window)
        DottedBackgroundMixin.__init__(self)
        
        self.scenario_id = scenario_id
        self.location = location

        self.setWindowTitle("Редактировать локацию" if location else "Новая локация")
        self.resize(720, 1280)
        self.setMinimumSize(500, 400)

        # Основной вертикальный layout
        main = QVBoxLayout(self)
        main.setSpacing(15)

        # --- Блок названия ---
        name_layout = QVBoxLayout()
        name_label = QLabel("Название:")
        name_layout.addWidget(name_label)
        
        self.le_name = QLineEdit()
        self.le_name.setMinimumHeight(30)
        name_layout.addWidget(self.le_name)
        
        main.addLayout(name_layout)
        
        # --- Сплиттер для описания и заметки ---
        content_splitter = QSplitter(Qt.Vertical)
        content_splitter.setChildrenCollapsible(False)
        
        # --- Блок описания ---
        desc_widget = QWidget()
        desc_layout = QVBoxLayout(desc_widget)
        desc_layout.setContentsMargins(0, 0, 0, 10)
        
        desc_label = QLabel("Описание:")
        desc_layout.addWidget(desc_label)
        
        self.txt_desc = HighlightTextEdit()
        self.txt_desc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        desc_layout.addWidget(self.txt_desc)
        
        content_splitter.addWidget(desc_widget)
        
        # --- Блок заметки ---
        note_widget = QWidget()
        note_layout = QVBoxLayout(note_widget)
        note_layout.setContentsMargins(0, 0, 0, 0)
        
        note_label = QLabel("Заметка:")
        note_layout.addWidget(note_label)
        
        self.txt_note = HighlightTextEdit()
        self.txt_note.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        note_layout.addWidget(self.txt_note)
        
        content_splitter.addWidget(note_widget)
        
        # Устанавливаем начальные размеры (описание - больше, заметка - меньше)
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
        btn_cancel.clicked.connect(self.close)
        
        btn_layout.addWidget(btn_ok)
        btn_layout.addSpacing(5)  # Расстояние между кнопками
        btn_layout.addWidget(btn_cancel)
        btn_layout.addStretch()  # Растягивание справа для центрирования
        
        main.addLayout(btn_layout)
        
        # Заполняем поля, если передана локация для редактирования
        if self.location:
            self.le_name.setText(self.location.name)
            self.txt_desc.setPlainText(self.location.description or "")
            self.txt_note.setPlainText(self.location.note or "")

    def _on_save(self):
        data = {
            'name': self.le_name.text().strip(),
            'description': self.txt_desc.toPlainText().strip() or None,
            'note': self.txt_note.toPlainText().strip() or None,
            'scenario': self.scenario_id
        }
        self.saved.emit(data)
        self.close()