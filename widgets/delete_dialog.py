# widgets/delete_dialog.py
import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QMessageBox, QLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from utils.dotted_background import DottedBackgroundMixin


def resource_path(rel_path: str) -> str:
    """
    Возвращает абсолютный путь к ресурсу:
     - в режиме разработки: рядом с этим файлом
     - после сборки PyInstaller --onefile: внутри временной папки sys._MEIPASS
    """
    base = getattr(sys, '_MEIPASS', Path(__file__).parent)
    return str(Path(base) / rel_path)


class DeleteDialog(QMessageBox, DottedBackgroundMixin):
    def __init__(self, parent=None, title="Подтвердите удаление", message="", object_type=""):
        super().__init__(parent)
        DottedBackgroundMixin.__init__(self)
        
        self.setWindowTitle(title)
        self.setText(f"Удалить {object_type} «{message}»?")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        # Иконка удаления
        icon_path = resource_path("resources/icons/delete_icon.png")
        if os.path.exists(icon_path):
            self.setIconPixmap(QIcon(icon_path).pixmap(64, 64))
        else:
            self.setIcon(QMessageBox.Question)
    
        self._setup_appearance()
        self._setup_buttons()

    def _setup_appearance(self):
        # фиксированный размер
        self.setMinimumSize(500, 200)
        self.setMaximumSize(500, 200)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)
        # общий стиль
        self.setStyleSheet("""
            QMessageBox {
                background: #f8f5f2;
            }
            QPushButton {
                min-width: 100px;
                min-height: 30px;
            }
        """)
    
    def _setup_buttons(self):
        self.yes_button = self.addButton("Да",  QMessageBox.YesRole)
        self.no_button  = self.addButton("Нет", QMessageBox.NoRole)
        self.setDefaultButton(self.no_button)
        self.yes_button.setFixedSize(100, 35)
        self.no_button .setFixedSize(100, 35)
    
    def sizeHint(self):
        return QSize(500, 200)
