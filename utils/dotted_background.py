# utils/dotted_background.py
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QBrush

class DottedBackgroundMixin:
    """
    Миксин для добавления точечного фона к окнам и виджетам.
    Для использования нужно наследовать этот класс вместе с QWidget или его потомками.
    """
    def __init__(self, *args, **kwargs):
        # Настройки фона по умолчанию
        self.dot_color = QColor("#8b7d6b")
        self.dot_size = 1
        self.dot_spacing = 15
        self.bg_color = QColor("#f8f5f2")
        
    def setup_background(self, dot_color=None, dot_size=None, dot_spacing=None, bg_color=None):
        """Позволяет настроить параметры фона при необходимости"""
        if dot_color:
            self.dot_color = QColor(dot_color)
        if dot_size is not None:
            self.dot_size = dot_size
        if dot_spacing is not None:
            self.dot_spacing = dot_spacing
        if bg_color:
            self.bg_color = QColor(bg_color)
            
    def paintEvent(self, event):
        """Рисуем фон с точечным паттерном."""
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.bg_color)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.dot_color))

        r = self.rect()
        for x in range(r.x(), r.x() + r.width(), self.dot_spacing):
            for y in range(r.y(), r.y() + r.height(), self.dot_spacing):
                painter.drawEllipse(x, y, self.dot_size, self.dot_size)
        
        # Вызов метода paintEvent родительского класса, если он существует
        parent_paint = getattr(super(), "paintEvent", None)
        if parent_paint is not None:
            parent_paint(event)