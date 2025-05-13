# tests/test_bulk_insert.py

import pytest
from faker import Faker

from models.scenario  import Scenario
from models.character import Character

fake = Faker()

@pytest.mark.usefixtures("memory_db")
def test_bulk_insert_scenarios_and_characters():
    """
    Стресс-тест: создаём много сценариев и персонажей по батчам,
    убеждаемся, что вставка проходит без ошибок и даёт нужное количество строк.
    """
    scenarios_count     = 200
    chars_per_scenario  = 100
    batch_size          = 600  # строк за раз

    # 1) Массовая вставка сценариев (без проблем — 200×3=600 переменных)
    scen_data = [
        {
            'title':       fake.sentence(),
            'description': fake.paragraph(),
            'note':        fake.text()
        }
        for _ in range(scenarios_count)
    ]
    Scenario.insert_many(scen_data).execute()
    assert Scenario.select().count() == scenarios_count

    # 2) Подготовка всех персонажей
    char_data = []
    for scen in Scenario.select():
        for _ in range(chars_per_scenario):
            char_data.append({
                'name':        fake.name(),
                'role':        fake.job(),
                'description': fake.text(),
                'note':        None,
                'scenario':    scen.id
            })

    # 3) Вставляем пачками по batch_size
    for i in range(0, len(char_data), batch_size):
        batch = char_data[i:i + batch_size]
        Character.insert_many(batch).execute()

    expected = scenarios_count * chars_per_scenario
    assert Character.select().count() == expected
