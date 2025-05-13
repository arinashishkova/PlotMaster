# controllers/location_controller.py

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox
from peewee import fn

from models.location import Location
from views.forms.location_form import LocationForm  # Изменённый импорт
from widgets.delete_dialog import DeleteDialog
from widgets.message_dialog import WarningDialog
from database import db  # Для транзакций

class LocationController:
    def __init__(self, view, get_current_scenario_fn):
        """
        view                  — экземпляр MainWindow
        get_current_scenario_fn — функция, возвращающая текущий Scenario
        """
        self.view = view
        self._get_scenario = get_current_scenario_fn

        # Работаем с виджетами на вкладке «Локации»
        self.tab = self.view.detail.locations_tab

        # Привязываем сигналы кнопок и списка
        self.tab.btn_new_loc.clicked.connect(self.on_new_location)
        self.tab.btn_edit_loc.clicked.connect(self.on_edit_location)
        self.tab.btn_delete_loc.clicked.connect(self.on_delete_location)
        self.tab.loc_list.currentItemChanged.connect(self.on_loc_selected)

    def load_locations(self):
        """Загружает локации текущего сценария во вкладке «Локации»."""
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

    def on_loc_selected(self, current, previous):
        """При выборе локации показывает её название, описание и заметку."""
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

    def on_new_location(self):
        """Открывает немодальное окно создания локации."""
        scen = self._get_scenario()
        form = LocationForm(parent=self.view, scenario_id=scen.id)
        # подписываемся на сигнал saved
        form.saved.connect(self._create_location)
        form.show()

    def _create_location(self, data):
        """Слот: создавать новую локацию и обновлять список."""
        Location.create(**data)
        self.load_locations()

    def on_edit_location(self):
        """Открывает немодальное окно редактирования выбранной локации."""
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

    def _update_location(self, loc, data):
        """Слот: сохраняем изменения локации и обновляем список."""
        for key, val in data.items():
            setattr(loc, key, val)
        loc.save()
        self.load_locations()

    def on_delete_location(self):
        """Удаляет локацию с подтверждением"""
        sel = self.tab.loc_list.currentItem()
        if not sel:
            dlg = WarningDialog(parent=self.view, title="Внимание", message="Выберите локацию для удаления")
            dlg.exec_()
            return

        location = Location.get_by_id(sel.data(Qt.UserRole))
        
        # Создаем кастомный диалог подтверждения
        dialog = DeleteDialog(
            parent=self.view,
            message=location.name,
            object_type="локацию"
        )
        
        # Показываем диалог и ждем результата
        dialog.exec_()
        
        # Проверяем, была ли нажата кнопка "Да"
        if dialog.clickedButton() == dialog.yes_button:
            try:
                with db.atomic():  # Используем транзакцию для безопасности
                    # Удаляем локацию и все связанные данные
                    location.delete_instance(recursive=True)
                    
                    # Обновляем список локаций
                    self.load_locations()
                    
            except Exception as e:
                QMessageBox.critical(
                    self.view,
                    "Ошибка",
                    f"Не удалось удалить локацию: {str(e)}"
                )
