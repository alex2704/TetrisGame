from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow,  QPushButton, QComboBox, QSpinBox, QMessageBox, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QFont, QBrush, QPen
from PyQt5.QtCore import Qt

class Interface(object):
    def setupUI(self, Window):
        self.btn_restart = QPushButton('Начать заново', Window)
        self.lb_count_name = QLabel(Window)
        self.lb_count = QLabel(Window)

        Window.title = "TetrisGame"
        Window.top = 100
        Window.left = 100
        Window.width = 830
        Window.height = 800
        self.btn_restart.setFont(QFont('Decorative', 12))
        self.btn_restart.setGeometry(550, 13, 170, 55)
        self.btn_restart.clicked.connect(Window.startTetrisGame)

        self.lb_count_name.setText('Ряды')
        self.lb_count_name.setAlignment(Qt.AlignCenter)
        self.lb_count_name.setFont(QFont('Decoraive', 20))
        self.lb_count_name.setGeometry(550, 100, 170, 55)

        self.lb_count.setAlignment(Qt.AlignCenter)
        self.lb_count.setFont(QFont('Decorative', 20))
        self.lb_count.setGeometry(550, 170, 170, 55)
        self.lb_count.setNum(Window.game.GetScore())
        Window.show()