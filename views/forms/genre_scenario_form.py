# views/forms/genre_scenario_form.py

from PyQt5.QtWidgets import (
    QWidget, QLabel, QComboBox, QListView,
    QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from utils.dotted_background import DottedBackgroundMixin
from models.genre import Genre
from database import db

class GenreScenarioForm(QWidget, DottedBackgroundMixin):
    saved = pyqtSignal(object)

    def __init__(self, parent=None, scenario=None, exclude_ids=None):
        QWidget.__init__(self, parent, flags=Qt.Window)
        DottedBackgroundMixin.__init__(self)

        self.scenario = scenario
        self.exclude_ids = exclude_ids or []

        # Заголовок и размеры
        self.setWindowTitle("Добавить жанр")
        self.resize(500, 150)
        self.setMinimumSize(400, 250)

        # Основной layout
        main = QVBoxLayout(self)
        main.setSpacing(15)

        # Метка
        lbl = QLabel("Выберите жанр:")
        main.addWidget(lbl)

        # Выпадающий список
        self.combo = QComboBox()
        # Назначаем QListView, чтобы QSS для QAbstractItemView применялся к popup
        self.combo.setView(QListView(self.combo))
        self.combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        main.addWidget(self.combo)

        # Загрузка жанров из базы (исключая уже добавленные)
        with db.atomic():
            genres = (
                Genre
                .select()
                .where(~Genre.id.in_(self.exclude_ids))
                .order_by(Genre.name.collate('NOCASE'))
            )
        for g in genres:
            self.combo.addItem(g.name, g.id)

        # Отступ до кнопок
        main.addStretch(1)

        # Кнопки
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_add = QPushButton("Добавить")
        btn_cancel = QPushButton("Отмена")
        # Размеры кнопок
        btn_add.setFixedWidth(200)
        btn_cancel.setFixedWidth(200)
        btn_add.setMinimumHeight(35)
        btn_cancel.setMinimumHeight(35)

        btn_add.clicked.connect(self._on_add)
        btn_cancel.clicked.connect(self.close)

        btn_layout.addWidget(btn_add)
        btn_layout.addSpacing(5)
        btn_layout.addWidget(btn_cancel)
        btn_layout.addStretch(1)
        main.addLayout(btn_layout)

    def _on_add(self):
        idx = self.combo.currentIndex()
        if idx < 0:
            return
        genre_id = self.combo.itemData(idx)
        genre = Genre.get_by_id(genre_id)
        self.saved.emit(genre)
        self.close()
