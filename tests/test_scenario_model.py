import pytest
from models.scenario import Scenario

def test_create_and_read_scenario(memory_db):
    # 1) Создаём сценарий
    s = Scenario.create(
        title="Тестовый сценарий",
        description="Описание",
        note="Заметка"
    )
    # 2) Он получил ID
    assert s.id is not None

    # 3) Считаем из базы
    s2 = Scenario.get_by_id(s.id)
    assert s2.title == "Тестовый сценарий"
    assert s2.description == "Описание"
    assert s2.note        == "Заметка"

def test_update_scenario(memory_db):
    s = Scenario.create(title="A")
    # редактируем
    s.title = "B"
    s.save()

    reloaded = Scenario.get_by_id(s.id)
    assert reloaded.title == "B"

def test_delete_scenario(memory_db):
    s = Scenario.create(title="ToDelete")
    sid = s.id
    # удаляем
    s.delete_instance()
    # теперь при попытке получить — будет DoesNotExist
    with pytest.raises(Scenario.DoesNotExist):
        Scenario.get_by_id(sid)
