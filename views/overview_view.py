# views/overview_view.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtCore import Qt
from controllers.overview_controller import OverviewController

class ScenarioOverview(QDialog):
    def __init__(self, parent=None, scenario=None):
        super().__init__(parent)
        self.setWindowTitle("Просмотр сценария")
        self.scenario = scenario

        # соотношение сторон A4
        self.resize(1240, 1754)

        # Текстовый виджет
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        # Устанавливаем белый фон и чёрный текст, чтобы окно было чисто-белым
        self.text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                color: black;
            }
        """ )

        # Кнопки
        self.btn_print = QPushButton("Печать")
        self.btn_save_txt = QPushButton("Сохранить в TXT")
        self.btn_close = QPushButton("Закрыть")
        for btn in (self.btn_print, self.btn_save_txt, self.btn_close):
            btn.setFixedWidth(200)

        # Центрирование кнопок
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_print)
        btn_layout.addWidget(self.btn_save_txt)
        btn_layout.addWidget(self.btn_close)
        btn_layout.addStretch()

        # Стили для QPushButton и QDialog
        self.setStyleSheet("""
            QPushButton { background-color: #f0f0f0; border: 1px solid #ccc; border-radius: 4px; padding: 6px 0; }
            QPushButton:hover { background-color: #e0e0e0; }
            QPushButton:pressed { background-color: #d0d0d0; }
            QDialog { background-color: white; }
        """
        )

        # Основной layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.text)
        layout.addLayout(btn_layout)

        # Наполнение HTML из контроллера
        controller = OverviewController(self.scenario)
        html = controller.generate_html()
        self.text.setHtml(html)

        # Обеспечиваем выравнивание текста по ширине
        option = self.text.document().defaultTextOption()
        option.setAlignment(Qt.AlignJustify)
        self.text.document().setDefaultTextOption(option)

        # Сигналы кнопок
        self.btn_print.clicked.connect(self._print)
        self.btn_save_txt.clicked.connect(self._save_to_txt)
        self.btn_close.clicked.connect(self.reject)

    def _print(self):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPrinter.A4)
        printer.setOrientation(QPrinter.Portrait)
        dlg = QPrintDialog(printer, self)
        dlg.setWindowTitle("Печать сценария")
        if dlg.exec_() == QPrintDialog.Accepted:
            self.text.print_(printer)

    def _save_to_txt(self):
        from PyQt5.QtWidgets import QFileDialog, QMessageBox
        options = QFileDialog.Options()
        default_name = f"{self.scenario.title}.txt" if self.scenario.title else "сценарий.txt"
        fname, _ = QFileDialog.getSaveFileName(self, "Сохранить как", default_name, "*.txt", options=options)
        if fname:
            if not fname.lower().endswith('.txt'):
                fname += '.txt'
            try:
                with open(fname, 'w', encoding='utf-8') as f:
                    f.write(self.text.toPlainText())
                QMessageBox.information(self, "Сохранено", f"Сценарий сохранён:\n{fname}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
