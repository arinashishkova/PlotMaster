# views/forms/genre_form.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, 
    QPushButton, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from utils.dotted_background import DottedBackgroundMixin

class GenreForm(QWidget, DottedBackgroundMixin):
    saved = pyqtSignal(dict)

    def __init__(self, parent=None, genre=None):
        QWidget.__init__(self, parent, flags=Qt.Window)
        DottedBackgroundMixin.__init__(self)
        
        self.genre = genre

        self.setWindowTitle("Редактировать жанр" if genre else "Новый жанр")
        self.resize(500, 200)
        self.setMinimumSize(400, 150)

        # Основной вертикальный layout
        main = QVBoxLayout(self)
        main.setSpacing(15)

        # --- Блок имени ---
        name_layout = QVBoxLayout()
        name_label = QLabel("Название жанра:")
        name_layout.addWidget(name_label)
        
        self.le_name = QLineEdit()
        self.le_name.setMinimumHeight(30)
        name_layout.addWidget(self.le_name)
        
        main.addLayout(name_layout)
        
        # Добавляем растягивающееся пространство
        main.addStretch(1)
        
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
        
        # Заполняем поля, если передан жанр для редактирования
        if genre:
            self.le_name.setText(genre.name)

    def _on_save(self):
        data = {
            'name': self.le_name.text().strip()
        }
        self.saved.emit(data)
        self.close()