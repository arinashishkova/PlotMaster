# seed_data.py

import random
from faker import Faker

from database import initialize_db, db
from models.scenario           import Scenario
from models.chapter            import Chapter
from models.character          import Character
from models.artifact           import Artifact
from models.location           import Location
from models.event              import Event
from models.event_character    import EventCharacter
from models.event_artifact     import EventArtifact
from models.genre              import Genre
from models.scenario_genre     import ScenarioGenre
from models.relation_type      import RelationType
from models.character_relation import CharacterRelation

fake = Faker()

def seed(
    n_scenarios=10,
    chapters_per=20,
    characters_per=20,
    artifacts_per=30,
    locations_per=20,
    events_per=10,
    genres_per=7,
    rel_types_per=5,
    char_relations_per=15
):
    """
    1) Удаляем все таблицы (safe=True — без ошибки, если их нет)
    2) Закрываем соединение
    3) Инициализируем заново через initialize_db()
    4) Сидируем «плотный» набор данных, задавая order глав явно
    """
    # --- Шаг 0: сброс предыдущей базы ---
    db.drop_tables([
        Scenario, Chapter, Character, Artifact, Location,
        Event, EventCharacter, EventArtifact,
        Genre, ScenarioGenre, RelationType, CharacterRelation
    ], safe=True)
    # После drop_tables Peewee открывает соединение — закрываем
    if not db.is_closed():
        db.close()

    # --- Шаг 1: заново создаём таблицы ---
    initialize_db([
        Scenario, Chapter, Character, Artifact, Location,
        Event, EventCharacter, EventArtifact,
        Genre, ScenarioGenre, RelationType, CharacterRelation
    ])

    # --- Шаг 2: пул уникальных жанров ---
    names = set()
    while len(names) < genres_per * 2:
        names.add(fake.word().capitalize())
    global_genres = [Genre.create(name=name) for name in names]

    # --- Шаг 3: сидирование сценариев и связанных данных ---
    for _ in range(n_scenarios):
        scen = Scenario.create(
            title=fake.sentence(nb_words=6),
            description=fake.paragraph(nb_sentences=5),
            note=fake.text(max_nb_chars=200)
        )

        # жанры
        for g in random.sample(global_genres, k=min(genres_per, len(global_genres))):
            ScenarioGenre.create(scenario=scen, genre=g)

        # типы связей для этого сценария
        local_rt = [
            RelationType.create(name=fake.word(), scenario=scen)
            for _ in range(rel_types_per)
        ]

        # главы с порядковым номером
        chapters = []
        for idx in range(chapters_per):
            chap = Chapter.create(
                title=f"Глава {idx+1}: {fake.sentence(nb_words=4)}",
                description=fake.paragraph(nb_sentences=70),
                note=None,
                scenario=scen,
                order=idx + 1
            )
            chapters.append(chap)

        # локации
        locs = []
        for _ in range(locations_per):
            locs.append(
                Location.create(
                    name=fake.city(),
                    description=fake.paragraph(nb_sentences=5),
                    note=None,
                    scenario=scen,
                    chapter=random.choice(chapters)
                )
            )

        # артефакты
        arts = []
        for _ in range(artifacts_per):
            arts.append(
                Artifact.create(
                    name=fake.word().capitalize(),
                    description=fake.paragraph(nb_sentences=5),
                    note=None,
                    scenario=scen,
                    chapter=random.choice(chapters)
                )
            )

        # персонажи
        chars = []
        for _ in range(characters_per):
            chars.append(
                Character.create(
                    name=fake.name(),
                    role=fake.job(),
                    description=fake.paragraph(nb_sentences=5),
                    note=None,
                    scenario=scen
                )
            )

        # связи между персонажами
        for _ in range(char_relations_per):
            a, b = random.sample(chars, 2)
            CharacterRelation.create(
                source=a,
                target=b,
                relation_type=random.choice(local_rt)
            )

        # события и их связи
        for _ in range(events_per):
            ev = Event.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=5),
                note=fake.text(max_nb_chars=200),
                scenario=scen,
                chapter=random.choice(chapters),
                location=random.choice(locs)
            )
            for ch in random.sample(chars, min(5, len(chars))):
                EventCharacter.create(event=ev, character=ch)
            for art in random.sample(arts, min(5, len(arts))):
                EventArtifact.create(event=ev, artifact=art)

    # --- Шаг 4: закрываем соединение ещё раз на всякий случай ---
    if not db.is_closed():
        db.close()

    print(f"Seeded {n_scenarios} scenarios with full data!")

if __name__ == "__main__":
    seed()
