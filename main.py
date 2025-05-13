# main.py

import sys
import os
from pathlib import Path

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui     import QIcon

from database import initialize_db

# Импорт моделей
from models.scenario            import Scenario
from models.character           import Character
from models.chapter             import Chapter
from models.artifact            import Artifact
from models.location            import Location
from models.event               import Event
from models.event_character     import EventCharacter
from models.event_artifact      import EventArtifact
from models.genre               import Genre
from models.scenario_genre      import ScenarioGenre
from models.relation_type       import RelationType
from models.character_relation  import CharacterRelation

# Импорт главного окна и контроллера
from views.main_window          import MainWindow
from controllers.main_controller import MainController

def resource_path(rel_path: str) -> str:
    """
    Возвращает абсолютный путь к ресурсу:
    - в режиме разработки: рядом с main.py
    - после сборки PyInstaller --onefile: внутри временной папки sys._MEIPASS
    """
    base = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base, rel_path)

if __name__ == '__main__':
    # 1) Инициализируем базу данных
    initialize_db([
        Scenario,
        Character,
        Chapter,
        Artifact,
        Location,
        Event,
        EventCharacter,
        EventArtifact,
        Genre,
        ScenarioGenre,
        RelationType,
        CharacterRelation,
    ])

    # 2) Создаём приложение
    app = QApplication(sys.argv)

    # 3) Подгружаем стиль из style.qss
    try:
        qss_file = resource_path("style.qss")
        with open(qss_file, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        # Если не получилось, используем минимальный запасной стиль
        print("Не удалось загрузить style.qss:", e)
        app.setStyleSheet("""
            QWidget {
                font-family: Consolas, monospace;
                font-size: 16px;
            }
        """)

    # 4) Устанавливаем иконку (тоже через resource_path, если её добавлял)
    icon_path = resource_path("resources/favicon.png")
    app.setWindowIcon(QIcon(icon_path))

    # 5) Запускаем главный цикл
    window = MainWindow()
    controller = MainController(window)
    window.show()
    sys.exit(app.exec_())
