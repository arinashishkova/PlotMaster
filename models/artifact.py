# models/artifact.py

from peewee import CharField, TextField, ForeignKeyField
from database import BaseModel
from models.scenario import Scenario
from models.chapter  import Chapter

class Artifact(BaseModel):
    name        = CharField(max_length=255)
    description = TextField(null=True)
    note        = TextField(null=True)   # ← добавили поле заметок
    scenario    = ForeignKeyField(Scenario, backref='artifacts', on_delete='CASCADE')
    chapter     = ForeignKeyField(Chapter,  backref='artifacts',   null=True, on_delete='SET NULL')
