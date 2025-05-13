# views/scenario_detail_page.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTabWidget,
    QSplitter, QSizePolicy, QFrame
)
from PyQt5.QtCore import Qt

# Импорт вкладок
from views.tabs.tab_chapters   import TabChapters
from views.tabs.tab_characters import TabCharacters
from views.tabs.tab_artifacts  import TabArtifacts
from views.tabs.tab_locations  import TabLocations
from views.tabs.tab_events     import TabEvents
from views.tabs.tab_relations  import TabRelations


class ScenarioDetailPage(QWidget):
    def __init__(self):
        super().__init__()

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(5, 5, 5, 5)

        # Создаем главный вертикальный сплиттер, который будет содержать 
        # верхнюю часть с информацией и нижнюю часть с вкладками
        main_splitter = QSplitter(Qt.Vertical)
        main_splitter.setHandleWidth(1)
        main_splitter.setStyleSheet("""
            QSplitter::handle:vertical { 
                background-color: #8b7d6b;
                height: 1px;
            }
        """)

        # Контейнер для верхней части (заголовок, жанры, описание)
        top_container = QWidget()
        top_layout = QVBoxLayout(top_container)
        top_layout.setContentsMargins(5, 5, 5, 5)
        
        # Строка 1: заголовок и кнопка "Назад"
        title_layout = QHBoxLayout()
        self.lbl_title = QLabel("")
        self.lbl_title.setStyleSheet("font-weight: bold; font-size: 24px;")
        title_layout.addWidget(self.lbl_title, stretch=1)
        self.btn_back = QPushButton("← Назад")
        self.btn_back.setFixedWidth(200)
        title_layout.addWidget(self.btn_back, alignment=Qt.AlignRight)
        top_layout.addLayout(title_layout)

        # Строка 2: жанры под заголовком
        genres_layout = QHBoxLayout()
        self.lbl_genres = QLabel("") 
        self.lbl_genres.setStyleSheet("color: gray; font-style: italic;")
        genres_layout.addWidget(self.lbl_genres, stretch=1)
        top_layout.addLayout(genres_layout)

        # Строка 3: описание и заметки разделенные сплиттером
        desc_notes_splitter = QSplitter(Qt.Horizontal)
        desc_notes_splitter.setHandleWidth(1)
        desc_notes_splitter.setStyleSheet("""
            QSplitter::handle:horizontal { 
                background-color: #8b7d6b;
                width: 1px;
            }
        """)
        
        # Контейнер для описания
        desc_container = QWidget()
        desc_layout = QVBoxLayout(desc_container)
        desc_layout.setContentsMargins(0, 0, 5, 0)
        
        lbl_desc_title = QLabel("Краткое описание:")
        lbl_desc_title.setStyleSheet("text-decoration: underline;")
        desc_layout.addWidget(lbl_desc_title)

        self.lbl_description = QLabel("")
        self.lbl_description.setWordWrap(True)
        # Выравнивание текста по верхнему левому углу
        self.lbl_description.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.lbl_description.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        desc_layout.addWidget(self.lbl_description, stretch=1)
        
        # Контейнер для заметок
        notes_container = QWidget()
        notes_layout = QVBoxLayout(notes_container)
        notes_layout.setContentsMargins(5, 0, 0, 0)
        
        lbl_notes_title = QLabel("Заметки:")
        lbl_notes_title.setStyleSheet("text-decoration: underline;")
        notes_layout.addWidget(lbl_notes_title)

        self.lbl_notes = QLabel("")
        self.lbl_notes.setWordWrap(True)
        # Выравнивание текста по верхнему левому углу
        self.lbl_notes.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.lbl_notes.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        notes_layout.addWidget(self.lbl_notes, stretch=1)
        
        # Добавляем контейнеры в сплиттер
        desc_notes_splitter.addWidget(desc_container)
        desc_notes_splitter.addWidget(notes_container)
        
        # Установка начальных размеров для сплиттера (описание : заметки = 3 : 1)
        desc_notes_splitter.setStretchFactor(0, 3)  # Для описания
        desc_notes_splitter.setStretchFactor(1, 1)  # Для заметок
        
        # Добавляем сплиттер в верхний контейнер
        top_layout.addWidget(desc_notes_splitter, stretch=1)
        
        top_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        # Добавляем верхний контейнер в сплиттер
        main_splitter.addWidget(top_container)
        
        # Контейнер для вкладок
        tab_container = QWidget()
        tab_layout = QVBoxLayout(tab_container)
        tab_layout.setContentsMargins(5, 10, 5, 0)
        
        # Вкладки
        self.tabs = QTabWidget()
        self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        tab_layout.addWidget(self.tabs)
        
        # Добавляем контейнер с вкладками в сплиттер
        main_splitter.addWidget(tab_container)
        
        # Установка начальных размеров для сплиттера (относительные пропорции)
        main_splitter.setStretchFactor(0, 1)  # Для верхней части
        main_splitter.setStretchFactor(1, 3)  # Для нижней части с вкладками
        
        # Добавляем сплиттер в основной макет
        root_layout.addWidget(main_splitter, stretch=1)

        # Инициализация вкладок
        self.chapters_tab   = TabChapters()
        self.characters_tab = TabCharacters()
        self.artifacts_tab  = TabArtifacts()
        self.locations_tab  = TabLocations()
        self.events_tab     = TabEvents()
        self.relations_tab  = TabRelations()

        # Добавление вкладок
        self.tabs.addTab(self.chapters_tab,   "Сюжет")
        self.tabs.addTab(self.characters_tab, "Персонажи")
        self.tabs.addTab(self.artifacts_tab,  "Артефакты")
        self.tabs.addTab(self.locations_tab,  "Локации")
        self.tabs.addTab(self.events_tab,     "События")
        self.tabs.addTab(self.relations_tab,  "Связи")

        # Кнопка "Просмотр сценария" внизу справа
        btn_row = QHBoxLayout()
        btn_row.addStretch(1)
        self.btn_overview = QPushButton("Просмотр сценария")
        self.btn_overview.setFixedWidth(200)
        btn_row.addWidget(self.btn_overview, alignment=Qt.AlignRight)
        btn_row.setContentsMargins(0, 0, 5, 0)  # Отступ 5px справа
        root_layout.addLayout(btn_row)