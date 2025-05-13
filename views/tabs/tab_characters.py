# views/tabs/tab_characters.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLabel,
    QSplitter
)
from PyQt5.QtCore import Qt
from widgets.highlight_text_edit import HighlightTextEdit

class TabCharacters(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # ── Сплиттер: слева — детали, справа — список и кнопки ──
        splitter = QSplitter(Qt.Horizontal)

        # — Левая панель: вертикальный сплиттер для описания и заметок
        left_splitter = QSplitter(Qt.Vertical)
        left_splitter.setHandleWidth(1)
        left_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #8b7d6b;
                height: 1px;
            }
        """)

        # • Верхняя часть: имя, роль, описание
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        # Имя
        top_layout.addWidget(QLabel("Имя:"))
        self.lbl_char_name = QLabel("")
        self.lbl_char_name.setStyleSheet("font-weight: bold; font-size: 18px;")
        top_layout.addWidget(self.lbl_char_name)
        # Роль
        top_layout.addWidget(QLabel("Роль:"))
        self.lbl_char_role = QLabel("")
        self.lbl_char_role.setStyleSheet("font-style: italic; font-size: 18px;")
        top_layout.addWidget(self.lbl_char_role)
        # Описание
        top_layout.addWidget(QLabel("Описание:"))
        self.char_desc = HighlightTextEdit()
        self.char_desc.setReadOnly(True)
        self.char_desc.setStyleSheet("font-family: 'Consolas';")
        top_layout.addWidget(self.char_desc)

        left_splitter.addWidget(top_widget)

        # • Нижняя часть: заметки
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.addWidget(QLabel("Заметки:"))
        self.char_note = HighlightTextEdit()
        self.char_note.setReadOnly(True)
        self.char_note.setPlaceholderText("Заметки о персонаже (если есть)…")
        self.char_note.setStyleSheet("font-style: italic; color: gray;")
        bottom_layout.addWidget(self.char_note)

        left_splitter.addWidget(bottom_widget)

        # Пропорции между описанием и заметками
        left_splitter.setStretchFactor(0, 3)
        left_splitter.setStretchFactor(1, 1)

        splitter.addWidget(left_splitter)

        # — Правая панель: кнопка + список + ред/удл
        right = QWidget()
        right_l = QVBoxLayout(right)
        self.btn_new_char    = QPushButton("Новый персонаж")
        self.char_list       = QListWidget()
        right_l.addWidget(self.btn_new_char, stretch=0)
        right_l.addWidget(self.char_list,    stretch=1)

        btns = QHBoxLayout()
        self.btn_edit_char   = QPushButton("Редактировать")
        self.btn_delete_char = QPushButton("Удалить")
        btns.addWidget(self.btn_edit_char)
        btns.addWidget(self.btn_delete_char)
        right_l.addLayout(btns, stretch=0)

        splitter.addWidget(right)

        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter)