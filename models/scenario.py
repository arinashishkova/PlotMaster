# models/scenario.py

from peewee import Model, CharField, TextField
from database import BaseModel

class Scenario(BaseModel):
    title = CharField(max_length=255)
    description = TextField(null=True)
    note        = TextField(null=True)