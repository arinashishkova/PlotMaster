# models/event_artifact.py

from peewee import ForeignKeyField
from database import BaseModel
from models.event    import Event
from models.artifact import Artifact

class EventArtifact(BaseModel):
    event    = ForeignKeyField(Event,    backref='event_artifacts',    on_delete='CASCADE')
    artifact = ForeignKeyField(Artifact, backref='event_artifacts',    on_delete='CASCADE')
