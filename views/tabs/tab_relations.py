# views/tabs/tab_relations.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLabel,
    QSplitter, QSizePolicy
)
from PyQt5.QtCore import Qt

class TabRelations(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Новая связь")
        self.btn_edit = QPushButton("Редактировать связь")
        self.btn_delete = QPushButton("Удалить связь")
        for btn in (self.btn_add, self.btn_edit, self.btn_delete):
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.setHandleWidth(1)
        main_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #8b7d6b;
                width: 1px;
            }
        """)

        left_panel = QWidget()
        left_l = QVBoxLayout(left_panel)
        left_l.addWidget(QLabel("Персонажи:"))
        self.char_list = QListWidget()
        left_l.addWidget(self.char_list)
        main_splitter.addWidget(left_panel)

        right_splitter = QSplitter(Qt.Vertical)
        right_splitter.setHandleWidth(1)
        right_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #8b7d6b;
                height: 1px;
            }
        """)

        top_panel = QWidget()
        top_l = QVBoxLayout(top_panel)
        top_l.addWidget(QLabel("Типы связей:"))
        self.rel_type_list = QListWidget()
        top_l.addWidget(self.rel_type_list)
        right_splitter.addWidget(top_panel)

        bottom_panel = QWidget()
        bottom_l = QVBoxLayout(bottom_panel)
        bottom_l.addWidget(QLabel("Участники:"))
        self.participants_list = QListWidget()
        bottom_l.addWidget(self.participants_list)
        right_splitter.addWidget(bottom_panel)

        main_splitter.addWidget(right_splitter)
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 2)

        layout.addWidget(main_splitter)