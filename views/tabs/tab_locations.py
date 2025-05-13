# views/tab_locations.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLabel,
    QSplitter, QTextEdit, QSizePolicy, QFrame
)
from PyQt5.QtCore import Qt

class TabLocations(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # ── Кнопки CRUD ──────────────────────────
        btn_layout = QHBoxLayout()
        self.btn_new_loc = QPushButton("Новая локация")
        self.btn_edit_loc = QPushButton("Редактировать локацию")
        self.btn_delete_loc = QPushButton("Удалить локацию")
        for btn in (self.btn_new_loc, self.btn_edit_loc, self.btn_delete_loc):
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        # ── Основной сплиттер: слева — список, справа — детали ────
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.setHandleWidth(1)
        main_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #8b7d6b;
                width: 1px;
                margin-left: 10px;
            }
        """)

        # • Список локаций (слева)
        self.loc_list = QListWidget()
        main_splitter.addWidget(self.loc_list)

        # • Панель деталей (справа) с вертикальным сплиттером
        detail_splitter = QSplitter(Qt.Vertical)
        detail_splitter.setHandleWidth(1)
        detail_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #8b7d6b;
                height: 1px;
            }
        """)

        # — Верхняя часть: заголовок и описание
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        
        # Заголовок (название локации)
        self.loc_title = QLabel("")
        self.loc_title.setStyleSheet("font-weight: bold; font-size: 18px;")
        top_layout.addWidget(self.loc_title, stretch=0)

        # Горизонтальная линия
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Plain)                  
        sep.setStyleSheet("""
            QFrame {
                border-top: 1px solid #8b7d6b;
                color: brown;
            }
        """)
        top_layout.addWidget(sep, stretch=0)

        # Описание
        top_layout.addWidget(QLabel("Описание:"))
        self.loc_desc = QTextEdit()
        self.loc_desc.setReadOnly(True)
        top_layout.addWidget(self.loc_desc, stretch=1)

        detail_splitter.addWidget(top_widget)

        # — Нижняя часть: заметки
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        
        bottom_layout.addWidget(QLabel("Заметки:"))
        self.loc_note = QTextEdit()
        self.loc_note.setReadOnly(True)
        self.loc_note.setPlaceholderText("Заметка (если есть)...")
        bottom_layout.addWidget(self.loc_note, stretch=1)

        detail_splitter.addWidget(bottom_widget)

        # Пропорции между описанием и заметками (3:1)
        detail_splitter.setStretchFactor(0, 3)
        detail_splitter.setStretchFactor(1, 1)

        main_splitter.addWidget(detail_splitter)

        # Настроим соотношение ширин: список 1, детали 2
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 2)

        layout.addWidget(main_splitter)