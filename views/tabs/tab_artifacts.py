# views/tabs/tab_artifacts.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLabel,
    QSplitter, QTextEdit, QSizePolicy, QFrame
)
from PyQt5.QtCore import Qt

class TabArtifacts(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # ── Кнопки CRUD ──────────────────────────
        btn_layout = QHBoxLayout()
        self.btn_new_art    = QPushButton("Новый артефакт")
        self.btn_edit_art   = QPushButton("Редактировать артефакт")
        self.btn_delete_art = QPushButton("Удалить артефакт")
        for btn in (self.btn_new_art, self.btn_edit_art, self.btn_delete_art):
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

        # • Список артефактов (слева)
        self.art_list = QListWidget()
        main_splitter.addWidget(self.art_list)

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
        
        # Заголовок (имя артефакта)
        self.art_title = QLabel("")
        self.art_title.setStyleSheet("font-weight: bold; font-size: 18px;")
        top_layout.addWidget(self.art_title, stretch=0)

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
        self.art_desc = QTextEdit()
        self.art_desc.setReadOnly(True)
        top_layout.addWidget(self.art_desc, stretch=1)

        detail_splitter.addWidget(top_widget)

        # — Нижняя часть: заметки
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        
        bottom_layout.addWidget(QLabel("Заметки:"))
        
        self.art_note = QTextEdit()
        self.art_note.setReadOnly(True)
        bottom_layout.addWidget(self.art_note, stretch=1)

        detail_splitter.addWidget(bottom_widget)

        # Пропорции между описанием и заметками
        detail_splitter.setStretchFactor(0, 3)
        detail_splitter.setStretchFactor(1, 1)

        main_splitter.addWidget(detail_splitter)

        # Настроим соотношение ширин: список 1, детали 2
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 2)

        layout.addWidget(main_splitter)