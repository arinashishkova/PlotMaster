from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt

class WelcomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addStretch()

        self.label = QLabel("<h1>PlotMaster</h1><p>Добро пожаловать!</p>")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        layout.addSpacing(20)

        btn_width = 200

        self.btn_start = QPushButton("Начать")
        self.btn_about = QPushButton("О программе")
        self.btn_exit = QPushButton("Выйти") 
        
        for btn in (self.btn_start, self.btn_about, self.btn_exit):
            btn.setFixedWidth(btn_width)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            layout.addWidget(btn, alignment=Qt.AlignCenter)
            layout.addSpacing(10)

        layout.addStretch()