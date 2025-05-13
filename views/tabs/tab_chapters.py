# views/tabs/tab_chapters.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QSplitter,
    QLabel, QSizePolicy
)
from PyQt5.QtCore import Qt
from widgets.highlight_text_edit import HighlightTextEdit

class TabChapters(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # ── кнопки Create/Edit/Delete ─────────────────────────
        btn_layout = QHBoxLayout()
        self.btn_create_chapter = QPushButton("Создать часть")
        self.btn_edit_chapter   = QPushButton("Редактировать часть")
        self.btn_delete_chapter = QPushButton("Удалить часть")
        for btn in (
            self.btn_create_chapter,
            self.btn_edit_chapter,
            self.btn_delete_chapter
        ):
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        # ── Главный сплиттер: слева — список + up/down, справа — детали ──
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.setHandleWidth(1)
        main_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #8b7d6b;
                width: 1px;
            }
        """)

        # — Левая панель: список глав и кнопки перемещения
        left = QWidget()
        left_l = QVBoxLayout(left)
        self.chapter_list = QListWidget()
        left_l.addWidget(self.chapter_list)
        move_l = QHBoxLayout()
        self.btn_move_up   = QPushButton("Вверх")
        self.btn_move_down = QPushButton("Вниз")
        move_l.addWidget(self.btn_move_up)
        move_l.addWidget(self.btn_move_down)
        left_l.addLayout(move_l)
        main_splitter.addWidget(left)

        # — Правая панель: вложенный vertical splitter для содержимого и заметки
        right = QWidget()
        right_l = QVBoxLayout(right)
        # Устанавливаем одинаковые отступы для всей правой панели
        right_l.setContentsMargins(10, 10, 10, 10)
        right_l.setSpacing(10)

        # Название главы
        self.chapter_title = QLabel("")
        self.chapter_title.setStyleSheet("""
            font-weight: bold;
            font-size: 18px;
        """)
        right_l.addWidget(self.chapter_title)

        # Заголовок для содержимого
        content_label = QLabel("Содержание главы:")
        right_l.addWidget(content_label)

        # Сплиттер по вертикали: верх — содержимое, низ — заметка
        vert_split = QSplitter(Qt.Vertical)
        vert_split.setHandleWidth(1)
        vert_split.setStyleSheet("""
            QSplitter::handle {
                background-color: #8b7d6b;
                height: 1px;
            }
        """)

        # • Верхняя часть: содержимое
        content_w = QWidget()
        content_l = QVBoxLayout(content_w)
        # Устанавливаем отступы внутри контейнера содержимого
        content_l.setContentsMargins(0, 0, 0, 10)  # Добавляем нижний отступ 5px
        self.chapter_content = HighlightTextEdit()
        self.chapter_content.setReadOnly(True)
        content_l.addWidget(self.chapter_content)
        vert_split.addWidget(content_w)

        # • Нижняя часть: заметка
        note_w = QWidget()
        note_l = QVBoxLayout(note_w)
        # Устанавливаем отступы внутри контейнера заметки
        note_l.setContentsMargins(0, 5, 0, 0)  # Добавляем верхний отступ 5px
        note_label = QLabel("Заметка к главе:")
        note_l.addWidget(note_label)
        self.chapter_note = HighlightTextEdit()
        self.chapter_note.setReadOnly(True)
        self.chapter_note.setPlaceholderText("Заметки о части сюжета (если есть)…")
        self.chapter_note.setStyleSheet("font-style: italic; color: gray;")
        note_l.addWidget(self.chapter_note)
        vert_split.addWidget(note_w)

        # Задаём стартовые пропорции: содержимое 3, заметка 1
        vert_split.setStretchFactor(0, 3)
        vert_split.setStretchFactor(1, 1)

        right_l.addWidget(vert_split)
        main_splitter.addWidget(right)

        # Итоговые пропорции: список 1, детали 2
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 2)

        layout.addWidget(main_splitter)