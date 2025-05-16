# controllers/event_controller.py

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem
from peewee import fn

from models.event            import Event
from models.event_character  import EventCharacter
from models.event_artifact   import EventArtifact
from views.forms.event_form  import EventForm
from widgets.delete_dialog   import DeleteDialog
from widgets.message_dialog  import WarningDialog

class EventController:
    def __init__(self, view, get_current_scenario_fn):
        self.view = view
        self._get_scenario = get_current_scenario_fn
        self.tab = self.view.detail.events_tab

        # Привязка сигналов
        self.tab.btn_new_ev.clicked.connect(self.on_new_event)
        self.tab.btn_edit_ev.clicked.connect(self.on_edit_event)
        self.tab.btn_delete_ev.clicked.connect(self.on_delete_event)
        self.tab.ev_list.currentItemChanged.connect(self.on_event_selected)

    # загрузка событий в сценраий 
    def load(self):
        scen = self._get_scenario()
        lw = self.tab.ev_list
        lw.clear()
        # Получаем события, отсортированные по названию без учета регистра
        events = (
            Event.select()
            .where(Event.scenario == scen)
            .order_by(fn.LOWER(Event.title))
        )
        for ev in events:
            it = QListWidgetItem(ev.title or "")
            it.setData(Qt.UserRole, ev.id)
            lw.addItem(it)
        self._clear_details()

    # очищает поля с деталями события
    def _clear_details(self):
        self.tab.ev_title.clear()
        self.tab.ev_loc.clear()
        self.tab.ev_chars_lbl.clear()
        self.tab.ev_arts_lbl.clear()
        self.tab.ev_desc.clear()
        self.tab.ev_note.clear()

    # заполняет событие при выборе деталями
    def on_event_selected(self, current, previous):
        if not current:
            self._clear_details()
            return

        ev = Event.get_by_id(current.data(Qt.UserRole))
        self.tab.ev_title.setText(ev.title or "")
        self.tab.ev_loc.setText(ev.location.name if ev.location else "")

        # Персонажи
        chars = ", ".join(
            ec.character.name
            for ec in EventCharacter.select().where(EventCharacter.event == ev)
        )
        self.tab.ev_chars_lbl.setText(chars)

        # Артефакты
        arts = ", ".join(
            ea.artifact.name
            for ea in EventArtifact.select().where(EventArtifact.event == ev)
        )
        self.tab.ev_arts_lbl.setText(arts)

        # Описание и заметки
        self.tab.ev_desc.setPlainText(ev.description or "")
        self.tab.ev_note.setPlainText(ev.note or "")

    # открытие формы создания нового события
    def on_new_event(self):
        scen = self._get_scenario()
        form = EventForm(parent=self.view, scenario_id=scen.id)
        form.saved.connect(lambda data, f=form: self._create_event(data, f))
        form.show()

    
    def _create_event(self, data, form):
        """Слот: создаёт событие и связи по выбору в форме."""
        ev = Event.create(**data)

        # Собираем выбранные ID персонажей и артефактов
        char_ids = [
            form.char_list.item(i).data(Qt.UserRole)
            for i in range(form.char_list.count())
            if form.char_list.item(i).isSelected()
        ]
        art_ids = [
            form.art_list.item(i).data(Qt.UserRole)
            for i in range(form.art_list.count())
            if form.art_list.item(i).isSelected()
        ]

        # Создаём связи
        for cid in char_ids:
            EventCharacter.create(event=ev, character=cid)
        for aid in art_ids:
            EventArtifact.create(event=ev, artifact=aid)

        self.load()

    # форма редактирования выбранного соытия
    def on_edit_event(self):
        sel = self.tab.ev_list.currentItem()
        if not sel:
            dlg = WarningDialog(parent=self.view, title="Внимание", message="Выберите событие для редактирования")
            dlg.exec_()
            return

        ev = Event.get_by_id(sel.data(Qt.UserRole))
        form = EventForm(parent=self.view, scenario_id=self._get_scenario().id, event=ev)
        form.saved.connect(lambda data, ev=ev, f=form: self._update_event(ev, data, f))
        form.show()

    # обновление формы редактирования
    def _update_event(self, ev, data, form):
        for key, val in data.items():
            setattr(ev, key, val)
        ev.save()

        # Пересоздаём связи
        EventCharacter.delete().where(EventCharacter.event == ev).execute()
        EventArtifact.delete().where(EventArtifact.event == ev).execute()

        char_ids = [
            form.char_list.item(i).data(Qt.UserRole)
            for i in range(form.char_list.count())
            if form.char_list.item(i).isSelected()
        ]
        art_ids = [
            form.art_list.item(i).data(Qt.UserRole)
            for i in range(form.art_list.count())
            if form.art_list.item(i).isSelected()
        ]

        for cid in char_ids:
            EventCharacter.create(event=ev, character=cid)
        for aid in art_ids:
            EventArtifact.create(event=ev, artifact=aid)

        self.load()

    # удаление события с подтверждением
    def on_delete_event(self):
        sel = self.tab.ev_list.currentItem()
        if not sel:
            dlg = WarningDialog(parent=self.view, title="Внимание", message="Выберите событие для удаления")
            dlg.exec_()
            return

        ev = Event.get_by_id(sel.data(Qt.UserRole))

        dialog = DeleteDialog(
            parent=self.view,
            message=ev.title,
            object_type="событие"
        )
        dialog.exec_()
        if dialog.clickedButton() == dialog.yes_button:
            ev.delete_instance(recursive=True)
            self.load()
