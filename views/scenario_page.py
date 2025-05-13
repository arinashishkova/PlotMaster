# views/scenario_page.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QTextEdit,
    QSplitter, QLabel, QSizePolicy
)
from PyQt5.QtCore import Qt

class ScenarioPage(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)

        # ── Кнопки «Новый», «Продолжить» слева — «Сохранить…», «Загрузить…», «На главную» справа
        btn_layout = QHBoxLayout()
        self.btn_new      = QPushButton("Новый сценарий")
        self.btn_continue = QPushButton("Продолжить")
        self.btn_save     = QPushButton("Сохранить…")
        self.btn_load     = QPushButton("Загрузить…")
        self.btn_home     = QPushButton("← На главную")  # ← новая кнопка

        # Все кнопки одинаково растягиваются
        for btn in (
            self.btn_new,
            self.btn_continue,
            self.btn_save,
            self.btn_load,
            self.btn_home,
        ):
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Сначала «Новый» и «Продолжить»
        btn_layout.addWidget(self.btn_new,      1)
        btn_layout.addWidget(self.btn_continue, 1)

        btn_layout.addStretch(1)

        # Потом «Сохранить…» и «Загрузить…»
        btn_layout.addWidget(self.btn_save,     1)
        btn_layout.addWidget(self.btn_load,     1)

        # И в самом конце — «На главную»
        btn_layout.addWidget(self.btn_home,     1)

        main_layout.addLayout(btn_layout)

        # ── Далее всё без изменений ────────────────────────────────
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.setHandleWidth(1)
        main_splitter.setStyleSheet("QSplitter::handle { background-color: #8b7d6b; }")

        # —— Левая панель — список сценариев + кнопки редактирования/удаления
        left = QWidget()
        left_l = QVBoxLayout(left)
        left_l.addWidget(QLabel("Название:"))
        self.list = QListWidget()
        left_l.addWidget(self.list, stretch=1)

        btns = QHBoxLayout()
        self.btn_edit   = QPushButton("Редактировать сценарий")
        self.btn_delete = QPushButton("Удалить сценарий")
        self.btn_delete.setObjectName("btnDeleteScenario")
        for btn in (self.btn_edit, self.btn_delete):
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btns.addWidget(self.btn_edit,   1)
        btns.addWidget(self.btn_delete, 1)
        left_l.addLayout(btns)

        main_splitter.addWidget(left)

        # —— Правая панель — вложенный вертикальный сплиттер
        right_splitter = QSplitter(Qt.Vertical)
        right_splitter.setHandleWidth(1)
        right_splitter.setStyleSheet("QSplitter::handle { background-color: #8b7d6b; }")

        # 1) Описание сценария
        desc_panel = QWidget()
        desc_l = QVBoxLayout(desc_panel)
        desc_l.addWidget(QLabel("Основное описание:"))
        self.desc_view = QTextEdit()
        self.desc_view.setReadOnly(True)
        desc_l.addWidget(self.desc_view, stretch=1)
        right_splitter.addWidget(desc_panel)

        # 2) Заметки + Жанры
        aux_splitter = QSplitter(Qt.Vertical)
        aux_splitter.setHandleWidth(1)
        aux_splitter.setStyleSheet("QSplitter::handle { background-color: #8b7d6b; }")

        # 2a) Заметки
        note_panel = QWidget()
        note_l = QVBoxLayout(note_panel)
        note_l.addWidget(QLabel("Заметки:"))
        self.note_view = QTextEdit()
        self.note_view.setReadOnly(True)
        note_l.addWidget(self.note_view, stretch=1)
        aux_splitter.addWidget(note_panel)

        # 2b) Жанры + кнопки
        genre_panel = QWidget()
        genre_l = QVBoxLayout(genre_panel)
        genre_l.addWidget(QLabel("Добавленные жанры:"))
        self.genre_list = QListWidget()
        genre_l.addWidget(self.genre_list, stretch=1)
        genres_btns = QHBoxLayout()
        self.btn_new_genre    = QPushButton("Создать новый жанр")
        self.btn_add_genre    = QPushButton("Добавить жанр к сценарию")
        self.btn_remove_genre = QPushButton("Удалить жанр из сценария")
        self.btn_remove_genre.setStyleSheet("""
            QPushButton#btnRemoveGenre {
                color: red;
            }
            QPushButton#btnRemoveGenre:hover {
                background-color: #FFCCCC;
            }
        """)

        genres_btns.addWidget(self.btn_new_genre)
        genres_btns.addWidget(self.btn_add_genre)
        genres_btns.addWidget(self.btn_remove_genre)
        genre_l.addLayout(genres_btns)
        self.btn_manage_genres = QPushButton("Управление жанрами…")
        genre_l.addWidget(self.btn_manage_genres)
        aux_splitter.addWidget(genre_panel)

        aux_splitter.setStretchFactor(0, 1)
        aux_splitter.setStretchFactor(1, 1)
        right_splitter.addWidget(aux_splitter)

        right_splitter.setStretchFactor(0, 2)
        right_splitter.setStretchFactor(1, 1)
        main_splitter.addWidget(right_splitter)

        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 2)
        main_layout.addWidget(main_splitter)

        # Локальный CSS для кнопки «Удалить сценарий»
        self.btn_delete.setStyleSheet("""
            QPushButton#btnDeleteScenario {
                color: red;
            }
            QPushButton#btnDeleteScenario:hover {
                background-color: #FFCCCC;
            }
        """)
