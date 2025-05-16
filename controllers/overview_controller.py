# controllers/overview_controller.py

from peewee import fn
from models.chapter import Chapter
from models.event import Event
from models.event_character import EventCharacter
from models.artifact import Artifact
from models.location import Location

class OverviewController:
    # контроллер генерации содержимого
    def __init__(self, scenario):
        self.scenario = scenario

    def generate_html(self) -> str:
        s = self.scenario
        parts = []

        # Заголовок
        parts.append(f"<h1>{s.title}</h1>")

        # Жанры
        genres = ", ".join(g.genre.name for g in s.scenario_genres)
        parts.append(f"<p><i>Жанры: {genres or '—'}</i></p>")

        # Описание
        if s.description:
            parts.append(f"<p>{s.description}</p>")

        # Краткий список персонажей
        char_names = [c.name for c in s.characters]
        if char_names:
            parts.append(f"<p><b>Действующие лица:</b> {', '.join(char_names)}.</p><br>")

        # Сюжет (главы)
        parts.append("<h1>СЮЖЕТ</h1>")
        for chap in Chapter.select().where(Chapter.scenario == s).order_by(Chapter.order):
            parts.append(f"<p><b>{chap.title}</b><br>{chap.description or ''}</p>")

        # Персонажи с описаниями
        parts.append("<br><h2>Персонажи</h2><ol>")
        for c in s.characters:
            role = f" — {c.role}" if c.role else ""
            desc = f": {c.description}" if c.description else ""
            parts.append(f"<li><b>{c.name}</b><i>{role}</i>{desc}</li>")
        parts.append("</ol>")

        # События
        parts.append("<br><h2>События</h2><ol>")
        for ev in Event.select().where(Event.scenario == s).order_by(fn.LOWER(Event.title)):
            loc = ev.location.name if ev.location else None
            chars = [rel.character.name for rel in EventCharacter.select().where(EventCharacter.event == ev)]
            extras = []
            if loc:
                extras.append(f"место: {loc}")
            if chars:
                extras.append(f"персонажи: {', '.join(chars)}")
            suffix = f" ({'; '.join(extras)})" if extras else ""
            parts.append(f"<li><b>{ev.title}</b>{suffix}: {ev.description or ''}</li>")
        parts.append("</ol>")

        # Артефакты
        parts.append("<br><h2>Артефакты</h2><ol>")
        for a in Artifact.select().where(Artifact.scenario == s):
            parts.append(f"<li><b>{a.name}</b>: {a.description or ''}</li>")
        parts.append("</ol>")

        # Локации
        parts.append("<br><h2>Локации</h2><ol>")
        for l in Location.select().where(Location.scenario == s):
            parts.append(f"<li><b>{l.name}</b>: {l.description or ''}</li>")
        parts.append("</ol>")

        # Окончательный шаблон HTML
        html = f"""
        <html>
         <head>
          <style>
            @page {{ margin: 2cm 2.5cm; }}
            body {{ padding: 20px 40px; font-family: Consolas, serif; font-size: 12pt; line-height: 1.5; }}
            h1 {{ font-size: 20pt; text-align: center; margin-bottom: 0.8cm; text-transform: uppercase; }}
            h2 {{ font-size: 14pt; margin-top: 1.2cm; margin-bottom: 0.5cm; border-bottom: 1px solid #999; padding-bottom: 3px; }}
            p, li {{ margin-bottom: 0.3cm; text-align: justify; text-justify: inter-word; text-indent: 1em; }}
            ol {{ margin-left: 1.2em; margin-bottom: 1cm; }}
          </style>
         </head>
         <body>
           {''.join(parts)}
         </body>
        </html>
        """
        return html
