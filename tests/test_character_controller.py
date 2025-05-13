# tests/test_character_controller.py

import pytest
from pytestqt.qtbot import QtBot
from models.scenario  import Scenario
from models.character import Character
from views.main_window import MainWindow
from controllers.character_controller import CharacterController

@pytest.mark.usefixtures("memory_db")
def test_create_and_update_character(qtbot: QtBot):
    # 1) Подготовка: создаём один сценарий
    scen = Scenario.create(title="MyStory", description="", note="")

    # 2) Открываем окно, переключаемся на вкладку детализации
    window = MainWindow()
    qtbot.addWidget(window)
    # Имитируем переход в detail (как будто user нажал «Продолжить»)
    window.show_detail()
    # Устанавливаем контроллер текущего сценария
    main_ctrl = window.controller if hasattr(window, "controller") else None
    # Но проще: создаём CharacterController вручную
    char_ctrl = CharacterController(
        view=window,
        get_current_scenario_fn=lambda: scen
    )

    # 3) Создаём персонажа через приватный метод контроллера
    data = {
        "name":        "Alice",
        "role":        "Heroine",
        "description": "Brave and bold",
        "note":        None,
        "scenario":    scen
    }
    char_ctrl._create_character(data)

    # Убедимся, что запись появилась в БД
    chars = list(Character.select())
    assert len(chars) == 1
    assert chars[0].name == "Alice"

    # 4) Редактируем только имя и роль
    ch = chars[0]
    update_data = {"name": "Alice X", "role": "Protagonist"}
    char_ctrl._update_character(ch, update_data)

    # Проверяем, что данные в базе изменились
    updated = Character.get_by_id(ch.id)
    assert updated.name == "Alice X"
    assert updated.role == "Protagonist"
