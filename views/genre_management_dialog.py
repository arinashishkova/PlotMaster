# forms/genre_management_form.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem,
    QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from utils.dotted_background import DottedBackgroundMixin
from controllers.manage_genre_controller import ManageGenreController

class GenreManagementForm(QWidget, DottedBackgroundMixin):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent, flags=Qt.Window)
        DottedBackgroundMixin.__init__(self)
        
        self.setWindowTitle("Управление жанрами")
        self.resize(500, 400)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # список всех жанров
        self.list = QListWidget()
        self.list.setSelectionMode(QListWidget.SingleSelection)
        layout.addWidget(self.list)
        
        # кнопки CRUD
        btns = QHBoxLayout()
        btns.setSpacing(10)
        
        self.btn_new = QPushButton("Новый")
        self.btn_edit = QPushButton("Редактировать")  
        self.btn_delete = QPushButton("Удалить")

        self.btn_new.setMinimumHeight(35)
        self.btn_edit.setMinimumHeight(35)
        self.btn_delete.setMinimumHeight(35)
        
        btns.addWidget(self.btn_new)
        btns.addWidget(self.btn_edit)
        btns.addWidget(self.btn_delete)
        layout.addLayout(btns)
        
        # Инициализируем контроллер и сохраняем его
        self.controller = ManageGenreController(parent=parent, form=self)