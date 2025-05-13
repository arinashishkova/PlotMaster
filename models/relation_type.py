# models/relation_type.py

from peewee import CharField, ForeignKeyField
from database import BaseModel
from models.scenario import Scenario

class RelationType(BaseModel):
    name     = CharField(max_length=255)
    scenario = ForeignKeyField(Scenario, backref='relation_types', on_delete='CASCADE')
