# models/character_relation.py

from peewee import ForeignKeyField
from database import BaseModel
from models.character      import Character
from models.relation_type  import RelationType

class CharacterRelation(BaseModel):
    source        = ForeignKeyField(Character,     backref='relations_out', on_delete='CASCADE')
    target        = ForeignKeyField(Character,     backref='relations_in',  on_delete='CASCADE')
    relation_type = ForeignKeyField(RelationType, backref='relations',     on_delete='CASCADE')
