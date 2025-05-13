from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class AboutPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Информация о приложении и краткий гайд
        info_text = """
        <h2>PlotMaster</h2>
        <p>Приложение для создания и управления вашими сценариями.</p>
        <h3>Возможности</h3>
        <ul>
          <li><b>Сценарии</b>: создавайте новые или открывайте существующие, задавайте 
              название, краткое описание и подробные заметки.</li>
          <li><b>Жанры</b>: добавляйте жанры к сценарию для удобной классификации.</li>
          <li><b>Персонажи</b>: заводите героя, антагониста и всех участников, 
              указывайте их роль, описание и заметки.</li>
          <li><b>Главы (Сюжет)</b>: структурируйте историю на части и главы, 
              упорядочивайте их и добавляйте содержание.</li>
          <li><b>Артефакты и Локации</b>: храните ключевые предметы и места действия.</li>
          <li><b>События</b>: связывайте события с локациями, 
              персонажами и артефактами.</li>
          <li><b>Отношения</b>: моделируйте родственные или социальные связи 
              между персонажами.</li>
          <li><b>Сохранение/Загрузка</b>: экспортируйте сценарий в JSON-файл и 
              импортируйте его обратно.</li>
          <li><b>Просмотр</b>: соберите весь сценарий в единый текстовый документ 
              для печати или обзора.</li>
        </ul>
        <p style="color:gray; font-size:smaller;">
          © 2025 Arina Šiškova & Daria Strigun
        </p>
        """
        self.info = QLabel(info_text)
        self.info.setWordWrap(True)
        layout.addWidget(self.info)

        layout.addStretch()

        # Кнопка возврата (измененная)
        self.btn_back = QPushButton("Назад")
        self.btn_back.setFixedWidth(200)  # Фиксированная ширина
        layout.addWidget(self.btn_back, alignment=Qt.AlignCenter)  # По центру