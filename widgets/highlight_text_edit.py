# widgets/highlight_text_edit.py

from PyQt5.QtWidgets import QTextEdit, QAction
from PyQt5.QtGui import QTextCharFormat, QColor
from PyQt5.QtCore import Qt

class HighlightTextEdit(QTextEdit):
    def contextMenuEvent(self, event):
        # Берём стандартное меню
        menu = self.createStandardContextMenu()

        # Добавляем подменю «Акцент»
        accent_menu = menu.addMenu("Акцент")

        # Словарь доступных цветов
        colors = {
            "Красный":   QColor("#FFADAD"),
            "Оранжевый": QColor("#FFD6A5"),
            "Жёлтый":    QColor("#FDFFB6"),
            "Зелёный":   QColor("#CAFFBF"),
            "Голубой":   QColor("#9BF6FF"),
            "Синий":     QColor("#A0C4FF"),
            "Фиолетовый":QColor("#BDB2FF"),
            "Розовый":   QColor("#FFC6FF"),
            "Серый":     QColor("#E5E5E5"),
        }

        # Для каждого цвета создаём пункт меню
        for name, col in colors.items():
            act = QAction(name, accent_menu)
            # при срабатывании передаём конкретный цвет
            act.triggered.connect(lambda checked, c=col: self._apply_highlight(c))
            accent_menu.addAction(act)

        # И пункт для сброса
        reset = QAction("Сбросить акцент", accent_menu)
        reset.triggered.connect(self._clear_highlight)
        accent_menu.addAction(reset)

        # Показываем меню
        menu.exec_(event.globalPos())

    def _apply_highlight(self, color: QColor):
        """
        Окрашиваем фон выделенного текста в заданный цвет.
        """
        cursor = self.textCursor()
        if not cursor.hasSelection():
            return
        fmt = QTextCharFormat()
        fmt.setBackground(color)
        cursor.mergeCharFormat(fmt)

    def _clear_highlight(self):
        """
        Убираем фон у выделенного текста (делаем прозрачным).
        """
        cursor = self.textCursor()
        if not cursor.hasSelection():
            return
        fmt = QTextCharFormat()
        fmt.setBackground(Qt.transparent)
        cursor.mergeCharFormat(fmt)
