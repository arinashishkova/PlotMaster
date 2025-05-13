# models/event_character.py

from peewee import ForeignKeyField
from database import BaseModel
from models.event     import Event
from models.character import Character

class EventCharacter(BaseModel):
    event     = ForeignKeyField(Event,     backref='event_characters',     on_delete='CASCADE')
    character = ForeignKeyField(Character, backref='event_characters',     on_delete='CASCADE')
