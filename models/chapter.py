# models/chapter.py
from peewee import IntegerField, CharField, TextField, ForeignKeyField
from database import BaseModel
from models.scenario import Scenario

class Chapter(BaseModel):
    title       = CharField(max_length=255)
    description = TextField(null=True)
    note        = TextField(null=True)
    order       = IntegerField(default=0)   # новое поле для порядка
    scenario    = ForeignKeyField(
        Scenario,
        backref='chapters',
        on_delete='CASCADE'
    )
