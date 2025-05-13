# models/character.py


from peewee import Model, CharField, TextField, ForeignKeyField
from database import BaseModel
from models.scenario import Scenario

class Character(BaseModel):
    name = CharField(max_length=255)
    description = TextField(null=True)
    role = CharField(max_length=255, null=True)
    note = TextField(null=True)
    scenario = ForeignKeyField(Scenario, backref='characters', on_delete='CASCADE')
