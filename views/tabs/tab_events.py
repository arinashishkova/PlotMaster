# views/tabs/tab_events.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLabel,
    QSplitter, QSizePolicy, QFrame
)
from PyQt5.QtCore import Qt
from widgets.highlight_text_edit import HighlightTextEdit

class TabEvents(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Кнопки CRUD 
        btn_layout = QHBoxLayout()
        self.btn_new_ev = QPushButton("Новое событие")
        self.btn_edit_ev = QPushButton("Редактировать событие")
        self.btn_delete_ev = QPushButton("Удалить событие")
        for btn in (self.btn_new_ev, self.btn_edit_ev, self.btn_delete_ev):
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        # Главное разделение: список событий | детали 
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.setHandleWidth(1)
        main_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #8b7d6b;
                width: 1px;
                margin-left: 10px;
            }
        """)

        # Список событий
        self.ev_list = QListWidget()
        main_splitter.addWidget(self.ev_list)

        # ПРАВАЯ панель — детали
        detail = QWidget()
        detail_l = QVBoxLayout(detail)
        detail_l.setContentsMargins(10, 10, 10, 10)  # Устанавливаем единый отступ 10px

        # Название события
        self.ev_title = QLabel("")
        self.ev_title.setStyleSheet("font-weight: bold; font-size: 18px; text-decoration: underline;")
        detail_l.addWidget(self.ev_title, stretch=0)

        # Место события
        hl_loc = QHBoxLayout()
        hl_loc.addWidget(QLabel("Место события:"))
        self.ev_loc = QLabel("")
        self.ev_loc.setStyleSheet("font-style: italic; font-weight: bold;")
        hl_loc.addWidget(self.ev_loc, stretch=1)
        detail_l.addLayout(hl_loc)

        # Ряд: персонажи / предметы (по 50%)
        hl_row = QHBoxLayout()
        # Персонажи
        vl_chars = QVBoxLayout()
        vl_chars.addWidget(QLabel("Задействованные персонажи:"))
        self.ev_chars_lbl = QLabel("")
        self.ev_chars_lbl.setStyleSheet("font-style: italic; font-weight: bold;")
        self.ev_chars_lbl.setWordWrap(True)
        vl_chars.addWidget(self.ev_chars_lbl)
        hl_row.addLayout(vl_chars, 1)
        # Предметы
        vl_arts = QVBoxLayout()
        vl_arts.addWidget(QLabel("Ключевые предметы:"))
        self.ev_arts_lbl = QLabel("")
        self.ev_arts_lbl.setStyleSheet("font-style: italic; font-weight: bold;")
        self.ev_arts_lbl.setWordWrap(True)
        vl_arts.addWidget(self.ev_arts_lbl)
        hl_row.addLayout(vl_arts, 1)
        detail_l.addLayout(hl_row)

        # Разделитель
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        detail_l.addWidget(sep)
        sep.setStyleSheet("""
            QFrame {
                border-top: 1px solid #8b7d6b;
                color: brown;
            }
        """)

        # Вертикальный сплиттер для описания и заметок
        desc_note_splitter = QSplitter(Qt.Vertical)
        desc_note_splitter.setHandleWidth(1)
        desc_note_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #8b7d6b;
                height: 1px;
                margin-left: -10px;                         
            }
        """)

        # Верхняя часть: описание
        desc_widget = QWidget()
        desc_layout = QVBoxLayout(desc_widget)
        desc_layout.setContentsMargins(0, 10, 0, 10)  
        desc_layout.addWidget(QLabel("Описание события:"))
        self.ev_desc = HighlightTextEdit()
        self.ev_desc.setReadOnly(True)
        desc_layout.addWidget(self.ev_desc, stretch=1)
        desc_note_splitter.addWidget(desc_widget)

        # Нижняя часть: заметки
        note_widget = QWidget()
        note_layout = QVBoxLayout(note_widget)
        note_layout.setContentsMargins(0, 10, 0, 0)  
        note_layout.addWidget(QLabel("Заметки:"))
        self.ev_note = HighlightTextEdit()
        self.ev_note.setReadOnly(True)
        self.ev_note.setPlaceholderText("Заметка (если есть)...")
        self.ev_note.setStyleSheet("font-style: italic; color: gray;")
        note_layout.addWidget(self.ev_note, stretch=1)
        desc_note_splitter.addWidget(note_widget)

        desc_note_splitter.setStretchFactor(0, 3)
        desc_note_splitter.setStretchFactor(1, 1)

        detail_l.addWidget(desc_note_splitter, stretch=1)

        main_splitter.addWidget(detail)
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 2)

        layout.addWidget(main_splitter)