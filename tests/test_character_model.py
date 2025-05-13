# tests/test_character_model.py

import pytest
from faker import Faker
from models.character import Character
from models.scenario  import Scenario

fake = Faker()

@pytest.mark.usefixtures("memory_db")
def test_create_and_read_character():
    scen = Scenario.create(
        title=fake.sentence(),
        description=fake.text(),
        note=fake.text()
    )

    ch = Character.create(
        name        = fake.name(),
        role        = fake.job(),
        description = fake.text(),
        note        = fake.text(),
        scenario    = scen
    )

    read = Character.get_by_id(ch.id)
    assert read.name == ch.name   
    assert read.scenario.id == scen.id                   
