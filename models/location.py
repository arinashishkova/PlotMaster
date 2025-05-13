# models/location.py

from peewee import CharField, TextField, ForeignKeyField
from database import BaseModel
from models.scenario import Scenario
from models.chapter  import Chapter

class Location(BaseModel):
    name        = CharField(max_length=255)
    description = TextField(null=True)
    note        = TextField(null=True)      # ← новое поле
    scenario    = ForeignKeyField(Scenario, backref='locations', on_delete='CASCADE')
    chapter     = ForeignKeyField(Chapter,  backref='locations',   null=True, on_delete='SET NULL')
