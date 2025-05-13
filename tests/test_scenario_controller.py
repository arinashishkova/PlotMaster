# tests/test_scenario_controller.py

import pytest
from PyQt5.QtWidgets import QListWidgetItem
from pytestqt.qtbot import QtBot

from models.scenario import Scenario
from views.main_window import MainWindow
from controllers.scenario_controller import ScenarioController

@pytest.mark.usefixtures("memory_db")
def test_load_and_display_scenarios(qtbot: QtBot):
    # 1) Подготовка: создаём пару сценариев
    Scenario.create(title="Alpha", description="Desc A", note="Note A")
    Scenario.create(title="Beta",  description="Desc B", note="Note B")

    # 2) Инициализируем окно и контроллер
    window = MainWindow()
    qtbot.addWidget(window)
    ctrl = ScenarioController(
        view=window,
        on_select_fn=window.show_detail,
        on_manage_genres_fn=lambda: None
    )

    # 3) Загружаем список сценариев
    ctrl.load_scenarios()
    # Ожидаем, что в списке ровно два элемента — в порядке по title
    items = [window.scenario.list.item(i).text() for i in range(window.scenario.list.count())]
    assert items == ["Alpha", "Beta"]

    # 4) Выбираем первый элемент и проверяем детали
    window.scenario.list.setCurrentRow(0)
    # При выборе контроллер должен заполнить desc_view и note_view
    assert window.scenario.desc_view.toPlainText() == "Desc A"
    assert window.scenario.note_view.toPlainText() == "Note A"
