# controllers/manage_genre_controller.py
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox
from peewee import IntegrityError

from models.genre import Genre
from views.forms.genre_form import GenreForm
from widgets.delete_dialog import DeleteDialog
from database import db

class ManageGenreController:
    def __init__(self, parent, form):
        self.parent = parent
        self.form = form
        
        self.load_genres()
        
        f = self.form
        f.btn_new.clicked.connect(self.on_new)
        f.btn_edit.clicked.connect(self.on_edit)
        f.btn_delete.clicked.connect(self.on_delete)

    # загрузка всех жанров
    def load_genres(self):
        lw = self.form.list
        lw.clear()
        for g in Genre.select().order_by(Genre.name):
            it = QListWidgetItem(g.name)
            it.setData(Qt.UserRole, g.id)
            lw.addItem(it)

    # открытие окна создания жанра
    def on_new(self):
        form = GenreForm(parent=self.parent)
        form.saved.connect(self._create_genre)
        form.show()

    # создание жанра и обновления списка
    def _create_genre(self, data):
        name = data.get('name', '').strip()
        if not name:
            return
            
        try:
            Genre.create(name=name)
            self.load_genres()
        except IntegrityError:
            QMessageBox.warning(
                self.parent,
                "Жанр уже существует",
                f"Жанр «{name}» уже есть в списке."
            )

    # открытия окна немодального жанра
    def on_edit(self):
        sel = self.form.list.currentItem()
        if not sel:
            QMessageBox.warning(self.form, "Внимание", "Выберите жанр для редактирования")
            return

        gid = sel.data(Qt.UserRole)
        g = Genre.get_by_id(gid)
        form = GenreForm(parent=self.parent, genre=g)
        form.saved.connect(lambda data, g=g: self._update_genre(g, data))
        form.show()

    # сохранение жанра и обновление списков
    def _update_genre(self, genre, data):
        name = data.get('name', '').strip()
        if not name:
            return
            
        try:
            genre.name = name
            genre.save()
            self.load_genres()
        except IntegrityError:
            QMessageBox.warning(
                self.parent,
                "Жанр уже существует",
                f"Жанр «{name}» уже есть в списке."
            )

    # удаление жанра с подтверждением
    def on_delete(self):
        sel = self.form.list.currentItem()
        if not sel:
            QMessageBox.warning(self.form, "Внимание", "Выберите жанр для удаления")
            return
            
        gid = sel.data(Qt.UserRole)
        genre = Genre.get_by_id(gid)
        
        dialog = DeleteDialog(
            parent=self.parent,
            message=genre.name,
            object_type="жанра"
        )
        
        dialog.exec_()
        
        if dialog.clickedButton() == dialog.yes_button:
            try:
                with db.atomic():
                    genre.delete_instance()
                    self.load_genres()
            except Exception as e:
                QMessageBox.critical(
                    self.parent,
                    "Ошибка",
                    f"Не удалось удалить жанр: {str(e)}"
                )
