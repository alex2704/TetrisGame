import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow,  QPushButton, QComboBox, QSpinBox, QMessageBox, QLabel
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QFont, QBrush, QPen
from PyQt5.QtCore import Qt, QBasicTimer
from Game import GameTetris
from UI import Interface as MainWindowUI


class Window(QMainWindow, MainWindowUI):
    def __init__(self):
        super().__init__()
        self.startTetrisGame()
        self.setupUI(self)

        self.title = "TetrisGame"
        self.top = 100
        self.left = 100
        self.width = 830
        self.height = 800

        self.timer = QBasicTimer()
        self.timer.start(self.game.GetSpeed(), self)
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

    #Начало игры для Новой игры
    def startTetrisGame(self):
        self.game = GameTetris()

        self.setFocus()
        self.update()

    # Проигрыш
    def LoseGame(self, painter):
        painter.setFont(QFont('Decorative', 30))
        painter.drawText(150, 370, 'Проигрыш!')

    #таймер
    def timerEvent(self, e):
        self.game.Low()
        self.update()

    # события для клавиатуры
    def keyPressEvent(self, e):
        map = {
            QtCore.Qt.Key_Down: self.game.Low,
            QtCore.Qt.Key_Left: self.game.Left,
            QtCore.Qt.Key_Right: self.game.Right,
            QtCore.Qt.Key_Up: self.game.Rotate
        }
        if e.key() in map:
            map[e.key()]()
        self.update()

    #в случае проигрыша
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        painter.begin(self)

        self.lb_count.setNum(self.game.GetScore())
        for k in range(self.game.GetLenMatrixRows()):
            for l in range(self.game.GetLenMatrixCols()):
                painter.drawRect(self.game.GetCoordinateX(k, l)*50, self.game.GetCoordinateY(k, l)*50, 50, 50)
                if self.game.CheckOnSquare(k, l):
                    painter.fillRect(self.game.GetCoordinateX(k, l) * 50, self.game.GetCoordinateY(k, l) * 50, 50, 50,
                                     Qt.red)
                elif self.game.CheckOnStick(k, l):
                    painter.fillRect(self.game.GetCoordinateX(k, l) * 50, self.game.GetCoordinateY(k, l) * 50, 50, 50,
                                     Qt.yellow)
                elif self.game.CheckOnT(k, l):
                    painter.fillRect(self.game.GetCoordinateX(k, l) * 50, self.game.GetCoordinateY(k, l) * 50, 50, 50,
                                     Qt.blue)
                elif self.game.CheckOnZipper(k, l):
                    painter.fillRect(self.game.GetCoordinateX(k, l) * 50, self.game.GetCoordinateY(k, l) * 50, 50, 50,
                                     Qt.green)
                elif self.game.CheckOnRake(k, l):
                    painter.fillRect(self.game.GetCoordinateX(k, l) * 50, self.game.GetCoordinateY(k, l) * 50, 50, 50,
                                     Qt.darkYellow)
        if self.game.CheckTetrisLose():
           self.LoseGame(painter)
        painter.end()



App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
