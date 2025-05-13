# controllers/save_load_controller.py

import json
from PyQt5.QtCore    import Qt
from PyQt5.QtWidgets import QFileDialog

from models.scenario           import Scenario
from models.genre              import Genre
from models.scenario_genre     import ScenarioGenre
from models.character          import Character
from models.chapter            import Chapter
from models.artifact           import Artifact
from models.location           import Location
from models.event              import Event
from models.event_character    import EventCharacter
from models.event_artifact     import EventArtifact
from models.relation_type      import RelationType
from models.character_relation import CharacterRelation

from widgets.message_dialog import WarningDialog 

class SaveLoadController:
    def __init__(self, view, scenario_controller):
        """
        view                 — экземпляр MainWindow
        scenario_controller  — ваш ScenarioController, чтобы после загрузки
                               перезагрузить список сценариев
        """
        self.view                = view
        self.scenario_controller = scenario_controller

        sp = view.scenario
        sp.btn_save.clicked.connect(self.on_save)
        sp.btn_load.clicked.connect(self.on_load)

    def on_save(self):
        current = self.view.scenario.list.currentItem()
        if not current:
            dlg = WarningDialog(
                parent=self.view,
                title="Ошибка",
                message="Нет выбранного сценария для сохранения"
            )
            dlg.exec_()
            return

        sid  = current.data(Qt.UserRole)
        scen = Scenario.get_by_id(sid)

        path, _ = QFileDialog.getSaveFileName(
            self.view,
            "Сохранить сценарий как…",
            "",
            "JSON-файл (*.json)"
        )
        if not path:
            return

        try:
            data = self._gather(scen)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            dlg = WarningDialog(
                parent=self.view,
                title="Ошибка",
                message=f"Не удалось сохранить файл:\n{e}"
            )
            dlg.exec_()
        else:
            dlg = WarningDialog(
                parent=self.view,
                title="Готово",
                message=f'Сценарий "{scen.title}" успешно сохранён в:\n{path}'
            )
            dlg.exec_()

    def on_load(self):
        path, _ = QFileDialog.getOpenFileName(
            self.view,
            "Загрузить сценарий…",
            "",
            "JSON-файл (*.json)"
        )
        if not path:
            return

        # 1) читаем JSON
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            dlg = WarningDialog(
                parent=self.view,
                title="Ошибка",
                message=f"Не удалось открыть файл:\n{e}"
            )
            dlg.exec_()
            return

        # 2) импортируем в БД
        try:
            new_scenario = self._import(data)
        except Exception as e:
            dlg = WarningDialog(
                parent=self.view,
                title="Ошибка",
                message=f"Не удалось импортировать сценарий:\n{e}"
            )
            dlg.exec_()
            return

        # 3) перезагружаем список и выбираем только что добавленный
        self.scenario_controller.load_scenarios()
        lw = self.view.scenario.list
        for i in range(lw.count()):
            if lw.item(i).text() == new_scenario.title:
                lw.setCurrentRow(i)
                break

        # 4) показываем сообщение об успехе
        dlg = WarningDialog(
            parent=self.view,
            title="Готово",
            message=f'Сценарий "{new_scenario.title}" успешно загружен!'
        )
        dlg.exec_()

    def _gather(self, scen):
        """Собирает всё содержимое сценария в dict для JSON."""
        return {
            "title":       scen.title,
            "description": scen.description,
            "note":        scen.note,
            "genres":      [sg.genre.name for sg in scen.scenario_genres],
            "characters":  [
                {
                  "name":        c.name,
                  "role":        c.role,
                  "description": c.description,
                  "note":        c.note
                }
                for c in scen.characters
            ],
            "chapters":    [
                {
                  "title":       ch.title,
                  "description": ch.description,
                  "note":        ch.note,
                  "order":       ch.order
                }
                for ch in scen.chapters.order_by(Chapter.order)
            ],
            "artifacts":   [
                {
                  "name":        a.name,
                  "description": a.description,
                  "note":        a.note
                }
                for a in scen.artifacts
            ],
            "locations":   [
                {
                  "name":        l.name,
                  "description": l.description,
                  "note":        l.note
                }
                for l in scen.locations
            ],
            "events":      [
                {
                  "title":       e.title,
                  "description": e.description,
                  "note":        e.note,
                  "chapter":     (e.chapter.title if e.chapter else None),
                  "location":    (e.location.name if e.location else None),
                  "characters":  [rel.character.name for rel in EventCharacter.select().where(EventCharacter.event == e)],
                  "artifacts":   [rel.artifact.name  for rel in EventArtifact.select().where(EventArtifact.event == e)]
                }
                for e in scen.events
            ],
            "relations":   [
                {
                  "source": src.name,
                  "type":   rt.name,
                  "targets":[t.target.name for t in CharacterRelation.select().where(
                                (CharacterRelation.source == src) &
                                (CharacterRelation.relation_type == rt)
                            )]
                }
                for src in scen.characters
                for rt in RelationType.select()
                                      .join(CharacterRelation)
                                      .where(CharacterRelation.source == src)
            ]
        }

    def _import(self, data):
        """Импортирует сценарий из dict, возвращает новый Scenario."""
        scen = Scenario.create(
            title       = data["title"],
            description = data.get("description"),
            note        = data.get("note"),
        )
        # жанры
        for name in data.get("genres", []):
            g, _ = Genre.get_or_create(name=name)
            ScenarioGenre.create(scenario=scen, genre=g)
        # персонажи
        char_map = {}
        for c in data.get("characters", []):
            ch = Character.create(
                name        = c["name"],
                role        = c.get("role"),
                description = c.get("description"),
                note        = c.get("note"),
                scenario    = scen
            )
            char_map[ch.name] = ch
        # главы
        for ch in data.get("chapters", []):
            Chapter.create(
                title       = ch["title"],
                description = ch.get("description"),
                note        = ch.get("note"),
                order       = ch["order"],
                scenario    = scen
            )
        # артефакты
        for a in data.get("artifacts", []):
            Artifact.create(
                name        = a["name"],
                description = a.get("description"),
                note        = a.get("note"),
                scenario    = scen
            )
        # локации
        for l in data.get("locations", []):
            Location.create(
                name        = l["name"],
                description = l.get("description"),
                note        = l.get("note"),
                scenario    = scen
            )
        # события
        for e in data.get("events", []):
            ev = Event.create(
                title       = e["title"],
                description = e.get("description"),
                note        = e.get("note"),
                scenario    = scen,
                chapter     = Chapter.get_or_none(Chapter.title == e.get("chapter"), Scenario == scen),
                location    = Location.get_or_none(Location.name  == e.get("location"), Scenario == scen),
            )
            for cname in e.get("characters", []):
                if cname in char_map:
                    EventCharacter.create(event=ev, character=char_map[cname])
            for aname in e.get("artifacts", []):
                art = Artifact.get_or_none(Artifact.name == aname, Scenario == scen)
                if art:
                    EventArtifact.create(event=ev, artifact=art)
        # отношения
        for rel in data.get("relations", []):
            src = char_map.get(rel["source"])
            if not src:
                continue
            rt, _ = RelationType.get_or_create(name=rel["type"], scenario=scen)
            for tname in rel.get("targets", []):
                tgt = char_map.get(tname)
                if tgt:
                    CharacterRelation.create(source=src, target=tgt, relation_type=rt)
        return scen
