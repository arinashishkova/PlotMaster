# tests/conftest.py

import pytest
from peewee import SqliteDatabase

import database
from database import db
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

# List all your models here so we can create/drop their tables
ALL_MODELS = [
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
]

@pytest.fixture(scope="session")
def memory_db():
    """
    Provide an in-memory SQLite database for the duration of the test session.
    All tables are created once at the beginning and dropped at the end.
    """
    # 1) Создаём реальную in-memory базу
    test_db = SqliteDatabase(':memory:')

    # 2) Переназначаем глобальный db и базы моделей на эту in-memory БД
    database.db = test_db
    for model in ALL_MODELS:
        model._meta.database = test_db

    # 3) Подключаемся и создаём таблицы
    test_db.connect()
    test_db.create_tables(ALL_MODELS)
    yield test_db

    # 4) Удаляем тестовые таблицы и закрываем соединение
    test_db.drop_tables(ALL_MODELS)
    test_db.close()

@pytest.fixture(autouse=True)
def _clear_tables(memory_db):
    """
    Before each test, wipe all tables so tests don’t interfere with each other.
    """
    for model in ALL_MODELS:
        model.delete().execute()
    yield
