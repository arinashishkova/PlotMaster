# models/event.py

from peewee import CharField, TextField, ForeignKeyField
from database import BaseModel
from models.scenario import Scenario
from models.location import Location
from models.chapter  import Chapter

class Event(BaseModel):
    title       = CharField(max_length=255)
    description = TextField(null=True)
    note        = TextField(null=True)  
    scenario    = ForeignKeyField(Scenario, backref='events', on_delete='CASCADE')
    chapter     = ForeignKeyField(Chapter,  backref='events',   null=True, on_delete='SET NULL')
    location    = ForeignKeyField(Location, backref='events',   null=True, on_delete='SET NULL')
