#database.py
from peewee import SqliteDatabase, Model

db = SqliteDatabase('plotmaster.db', pragmas={'foreign_keys': 1})

class BaseModel(Model):
    class Meta:
        database = db

def initialize_db(models: list):
    db.connect()
    db.create_tables(models)
    db.close()

