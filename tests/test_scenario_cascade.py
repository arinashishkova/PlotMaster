# tests/test_scenario_cascade.py

import pytest
from models.scenario        import Scenario
from models.character       import Character
from models.genre           import Genre
from models.scenario_genre  import ScenarioGenre

@pytest.mark.usefixtures("memory_db")
def test_delete_scenario_cascades_characters():
    """При удалении сценария все его персонажи тоже удаляются."""
    scen = Scenario.create(title="BulkTest", description="", note="")
    Character.create(
        name="Hero", role="Protagonist",
        description="Desc", note=None,
        scenario=scen
    )
    assert Character.select().count() == 1

    scen.delete_instance(recursive=True)
    assert Character.select().count() == 0

@pytest.mark.usefixtures("memory_db")
def test_delete_scenario_cascades_scenario_genre():
    """При удалении сценария связи в ScenarioGenre должны удалиться."""
    scen = Scenario.create(title="X", description="", note="")
    g    = Genre.create(name="Action")
    ScenarioGenre.create(scenario=scen, genre=g)
    assert ScenarioGenre.select().count() == 1

    scen.delete_instance(recursive=True)
    assert ScenarioGenre.select().count() == 0
