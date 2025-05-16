# controllers/location_controller.py

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox
from peewee import fn

from models.location import Location
from views.forms.location_form import LocationForm 
from widgets.delete_dialog import DeleteDialog
from widgets.message_dialog import WarningDialog
from database import db

class LocationController:
    def __init__(self, view, get_current_scenario_fn):
        self.view = view
        self._get_scenario = get_current_scenario_fn

        self.tab = self.view.detail.locations_tab

        # Привязываем сигналы кнопок и списка
        self.tab.btn_new_loc.clicked.connect(self.on_new_location)
        self.tab.btn_edit_loc.clicked.connect(self.on_edit_location)
        self.tab.btn_delete_loc.clicked.connect(self.on_delete_location)
        self.tab.loc_list.currentItemChanged.connect(self.on_loc_selected)

    # загрузка локация к привязаному сценарию
    def load_locations(self):
        scen = self._get_scenario()

        # Обновляем список локаций
        lw = self.tab.loc_list
        lw.clear()
        # Получаем список локаций, отсортированных по имени без учета регистра
        locations = (
            Location.select()
            .where(Location.scenario == scen)
            .order_by(fn.LOWER(Location.name))
        )
        for loc in locations:
            it = QListWidgetItem(loc.name)
            it.setData(Qt.UserRole, loc.id)
            lw.addItem(it)

        # Сбрасываем детали
        self.tab.loc_title.clear()
        self.tab.loc_desc.clear()
        self.tab.loc_note.clear()

    # при выборе локация отображает её данные
    def on_loc_selected(self, current, previous):
        if not current:
            self.tab.loc_title.clear()
            self.tab.loc_desc.clear()
            self.tab.loc_note.clear()
            return

        loc_id = current.data(Qt.UserRole)
        loc = Location.get_by_id(loc_id)
        self.tab.loc_title.setText(loc.name)
        self.tab.loc_desc.setPlainText(loc.description or "")
        self.tab.loc_note.setPlainText(loc.note or "")

    # открытие окна создания локации
    def on_new_location(self):
        scen = self._get_scenario()
        form = LocationForm(parent=self.view, scenario_id=scen.id)
        form.saved.connect(self._create_location)
        form.show()

    # создание новой локации и обновления списка
    def _create_location(self, data):
        Location.create(**data)
        self.load_locations()

    # открытие окноредактирования выбраной локации
    def on_edit_location(self):
        sel = self.tab.loc_list.currentItem()
        if not sel:
            dlg = WarningDialog(parent=self.view, title="Внимание", message="Выберите локацию для редактирования")
            dlg.exec_()
            return

        loc_id = sel.data(Qt.UserRole)
        loc = Location.get_by_id(loc_id)
        form = LocationForm(
            parent=self.view,
            scenario_id=self._get_scenario().id,
            location=loc
        )
        # передаём сам объект loc в замыкание
        form.saved.connect(lambda data, loc=loc: self._update_location(loc, data))
        form.show()

    #  сохранение изменений локации и обновляет список
    def _update_location(self, loc, data):
        for key, val in data.items():
            setattr(loc, key, val)
        loc.save()
        self.load_locations()

    # удаление локации с подтверждением
    def on_delete_location(self):
        sel = self.tab.loc_list.currentItem()
        if not sel:
            dlg = WarningDialog(parent=self.view, title="Внимание", message="Выберите локацию для удаления")
            dlg.exec_()
            return

        location = Location.get_by_id(sel.data(Qt.UserRole))
        
        dialog = DeleteDialog(
            parent=self.view,
            message=location.name,
            object_type="локацию"
        )
        
        dialog.exec_()
        
        if dialog.clickedButton() == dialog.yes_button:
            try:
                with db.atomic(): 
                    location.delete_instance(recursive=True)
                    
                    self.load_locations()
                    
            except Exception as e:
                QMessageBox.critical(
                    self.view,
                    "Ошибка",
                    f"Не удалось удалить локацию: {str(e)}"
                )
