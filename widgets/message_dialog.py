# widgets/message_dialog.py
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


class WarningDialog(QMessageBox, DottedBackgroundMixin):
    """Стилизованный диалог предупреждения."""
    def __init__(self, parent=None, title="Внимание", message=""):
        super().__init__(parent)
        DottedBackgroundMixin.__init__(self)

        self.setWindowTitle(title)
        self.setText(message)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # Иконка предупреждения
        icon_path = resource_path("resources/icons/warning_icon.png")
        if os.path.exists(icon_path):
            self.setIconPixmap(QIcon(icon_path).pixmap(64, 64))
        else:
            self.setIcon(QMessageBox.Warning)

        self._setup_appearance()
        self._setup_buttons()

    def _setup_appearance(self):
        # фиксированный размер
        self.setMinimumSize(400, 180)
        self.setMaximumSize(400, 180)
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
        self.ok_button = self.addButton("ОК", QMessageBox.AcceptRole)
        self.setDefaultButton(self.ok_button)
        self.ok_button.setFixedSize(100, 35)

    def sizeHint(self):
        return QSize(400, 180)
