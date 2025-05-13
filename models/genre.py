# models/genre.py
from peewee import CharField
from database   import BaseModel

class Genre(BaseModel):
    name = CharField(max_length=100, unique=True)
