# controllers/chapter_controller.py

from PyQt5.QtCore    import Qt
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem
from PyQt5.QtWidgets import QListWidget  # Для scrollToItem

from models.chapter     import Chapter
from views.forms.chapter_form import ChapterForm
from widgets.delete_dialog import DeleteDialog
from database import db  # Для транзакций

class ChapterController:
    def __init__(self, view, get_current_scenario_fn):
        self.view          = view
        self._get_scenario = get_current_scenario_fn
        self.tab = self.view.detail.chapters_tab

        # кнопки и список
        self.tab.btn_create_chapter.clicked.connect(self.on_create_chapter)
        self.tab.btn_edit_chapter  .clicked.connect(self.on_edit_chapter)
        self.tab.btn_delete_chapter.clicked.connect(self.on_delete_chapter)
        self.tab.btn_move_up       .clicked.connect(self.on_move_chapter_up)
        self.tab.btn_move_down     .clicked.connect(self.on_move_chapter_down)
        self.tab.chapter_list.currentItemChanged.connect(self.on_chapter_selected)

    def load_chapters(self):
        """Загружает списком все главы, упорядоченные по полю order."""
        scen = self._get_scenario()
        lw   = self.tab.chapter_list
        lw.clear()
        # упорядочиваем по order, а при равных — по id для стабильности
        for chap in (Chapter
                     .select()
                     .where(Chapter.scenario == scen)
                     .order_by(Chapter.order, Chapter.id)):
            it = QListWidgetItem(chap.title)
            it.setData(Qt.UserRole, chap.id)
            lw.addItem(it)
        # очищаем детали
        self.tab.chapter_content.clear()
        self.tab.chapter_note.clear()

    def on_chapter_selected(self, current, previous):
        """При выборе главы показывает её содержимое."""
        if current:
            chap = Chapter.get_by_id(current.data(Qt.UserRole))
            self.tab.chapter_title.setText(chap.title)
            self.tab.chapter_content.setPlainText(chap.description or "")
            self.tab.chapter_note.setPlainText(chap.note or "")
        else:
            self.tab.chapter_title.clear()
            self.tab.chapter_content.clear()
            self.tab.chapter_note.clear()

    def on_create_chapter(self):
        scen = self._get_scenario()
        form = ChapterForm(parent=self.view, scenario_id=scen.id)
        form.saved.connect(self._create_chapter)
        form.show()

    def _create_chapter(self, data):
        scen = self._get_scenario()
        last = (Chapter
                .select()
                .where(Chapter.scenario == scen)
                .order_by(Chapter.order.desc())
                .first())
        data['order'] = (last.order + 1) if last else 1
        Chapter.create(**data)
        self.load_chapters()

    def on_edit_chapter(self):
        sel = self.tab.chapter_list.currentItem()
        if not sel:
            QMessageBox.warning(self.view, "Внимание", "Выберите главу для редактирования")
            return
        chap = Chapter.get_by_id(sel.data(Qt.UserRole))
        form = ChapterForm(parent=self.view,
                           scenario_id=chap.scenario.id,
                           chapter=chap)
        form.saved.connect(lambda data, chap=chap: self._update_chapter(chap, data))
        form.show()

    def _update_chapter(self, chap, data):
        chap.title       = data["title"]
        chap.description = data.get("description")
        chap.note        = data.get("note")
        chap.save()
        self.load_chapters()

    def on_delete_chapter(self):
        sel = self.tab.chapter_list.currentItem()
        if not sel:
            QMessageBox.warning(self.view, "Внимание", "Выберите главу для удаления")
            return
        chapter = Chapter.get_by_id(sel.data(Qt.UserRole))
        dialog = DeleteDialog(parent=self.view,
                              message=chapter.title,
                              object_type="главу")
        dialog.exec_()
        if dialog.clickedButton() == dialog.yes_button:
            try:
                with db.atomic():
                    chapter.delete_instance(recursive=True)
                self.load_chapters()
            except Exception as e:
                QMessageBox.critical(self.view, "Ошибка",
                                     f"Не удалось удалить главу: {e}")

    def on_move_chapter_up(self):
        """Перемещает выбранную главу на одну позицию выше."""
        sel = self.tab.chapter_list.currentItem()
        if not sel: 
            return
        chap       = Chapter.get_by_id(sel.data(Qt.UserRole))
        # ищем предыдущую по order
        prev = (Chapter
                .select()
                .where((Chapter.scenario == chap.scenario) &
                       (Chapter.order < chap.order))
                .order_by(Chapter.order.desc())
                .first())
        if not prev:
            return
        with db.atomic():
            # меняем местами порядковые номера
            chap.order, prev.order = prev.order, chap.order
            chap.save()
            prev.save()
            # нормализуем все order — подряд от 1 до N
            self._normalize_orders(chap.scenario)
        self.load_chapters()
        self._restore_selection(chap.id)

    def on_move_chapter_down(self):
        """Перемещает выбранную главу на одну позицию ниже."""
        sel = self.tab.chapter_list.currentItem()
        if not sel:
            return
        chap = Chapter.get_by_id(sel.data(Qt.UserRole))
        nxt  = (Chapter
                .select()
                .where((Chapter.scenario == chap.scenario) &
                       (Chapter.order > chap.order))
                .order_by(Chapter.order.asc())
                .first())
        if not nxt:
            return
        with db.atomic():
            chap.order, nxt.order = nxt.order, chap.order
            chap.save()
            nxt.save()
            self._normalize_orders(chap.scenario)
        self.load_chapters()
        self._restore_selection(chap.id)

    def _normalize_orders(self, scenario):
        """Переупорядочивает все главы сценария, чтобы order шёл подряд от 1."""
        for idx, chap in enumerate(
                Chapter
                .select()
                .where(Chapter.scenario == scenario)
                .order_by(Chapter.order, Chapter.id),
                start=1
        ):
            if chap.order != idx:
                chap.order = idx
                chap.save()

    def _restore_selection(self, chapter_id):
        """После перезагрузки списка восстанавливаем выбор и скроллим к нему."""
        lw = self.tab.chapter_list  # type: QListWidget
        for i in range(lw.count()):
            it = lw.item(i)
            if it.data(Qt.UserRole) == chapter_id:
                lw.setCurrentRow(i)
                lw.scrollToItem(it)
                break
