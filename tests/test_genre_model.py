# tests/test_genre_model.py

import pytest
from peewee import IntegrityError
from faker import Faker

from models.genre import Genre

fake = Faker()

@pytest.mark.usefixtures("memory_db")
def test_genre_unique_constraint():
    """Жанр с одинаковым именем не должен дважды сохраняться."""
    Genre.create(name="Fantasy")
    with pytest.raises(IntegrityError):
        Genre.create(name="Fantasy")
