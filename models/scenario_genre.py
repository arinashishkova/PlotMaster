# models/scenario_genre.py
from peewee import ForeignKeyField
from database   import BaseModel
from models.scenario import Scenario
from models.genre    import Genre

class ScenarioGenre(BaseModel):
    scenario = ForeignKeyField(Scenario, backref='scenario_genres', on_delete='CASCADE')
    genre    = ForeignKeyField(Genre,    backref='scenario_genres', on_delete='CASCADE')
