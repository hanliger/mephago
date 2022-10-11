from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import ChessBoard, utils
#from BlurWindow.blurWindow import blur

import sys

class Window(QMainWindow):
    LocToPos = {12:(150,50), 11:(100, 100), 1:(200, 100),
            9:(50, 150), 0:(150, 150), 3:(250, 150),
            7:(100, 200), 5:(200, 200), 6:(150, 250)}
    size = 100
    offset = 60
    myBoard = ChessBoard.ChessBoard("Hard")

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(300, 450)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        quitButton = QPushButton('X', self)
        quitButton.setGeometry(QRect(280,0,20,20))
        quitButton.clicked.connect(QCoreApplication.instance().quit)

        refreshButton = QPushButton('R', self)
        refreshButton.setGeometry(QRect(260, 0, 20, 20))
        # refreshButton.clicked.connect(lambda : self.selectedComboItem(diffCB))

        timerCheckBox = QCheckBox('타이머 ON', self)
        timerCheckBox.setGeometry(QRect(220, 30, 80, 20))
        timerCheckBox.setLayoutDirection(Qt.RightToLeft)
        timerCheckBox.setObjectName("timerCheckBox")

        diffCB = QComboBox(self)
        diffCB.setGeometry(QRect(0, 0, 60, 20))
        diffCB.addItem('하드',)
        diffCB.addItem('노말')
        diffCB.activated[str].connect(lambda : self.selectedComboItem(diffCB))

        pb12 = QPushButton(self)
        pb12.setGeometry(QRect(125,25+self.offset, 50, 50))
        pb12.setObjectName('12')
        pb12.clicked.connect(lambda : self.tileButtonClicked(pb12))
        pb12.setFlat(True)

        pb11 = QPushButton(self)
        pb11.setGeometry(QRect(75, 75 + self.offset, 50, 50))
        pb11.setObjectName('11')
        pb11.clicked.connect(lambda : self.tileButtonClicked(pb11))
        pb11.setFlat(True)

        pb1 = QPushButton(self)
        pb1.setGeometry(QRect(175, 75 + self.offset, 50, 50))
        pb1.setObjectName('1')
        pb1.clicked.connect(lambda : self.tileButtonClicked(pb1))
        pb1.setFlat(True)

        pb9 = QPushButton(self)
        pb9.setGeometry(QRect(25, 125 + self.offset, 50, 50))
        pb9.setObjectName('9')
        pb9.clicked.connect(lambda : self.tileButtonClicked(pb9))
        pb9.setFlat(True)

        pb0 = QPushButton(self)
        pb0.setGeometry(QRect(125, 125 + self.offset, 50, 50))
        pb0.setObjectName('0')
        pb0.clicked.connect(lambda : self.tileButtonClicked(pb0))
        pb0.setFlat(True)

        pb3 = QPushButton(self)
        pb3.setGeometry(QRect(225, 125 + self.offset, 50, 50))
        pb3.setObjectName('3')
        pb3.clicked.connect(lambda : self.tileButtonClicked(pb3))
        pb3.setFlat(True)

        pb7 = QPushButton(self)
        pb7.setGeometry(QRect(75, 175 + self.offset, 50, 50))
        pb7.setObjectName('7')
        pb7.clicked.connect(lambda : self.tileButtonClicked(pb7))
        pb7.setFlat(True)

        pb5 = QPushButton(self)
        pb5.setGeometry(QRect(175, 175 + self.offset, 50, 50))
        pb5.setObjectName('5')
        pb5.clicked.connect(lambda : self.tileButtonClicked(pb5))
        pb5.setFlat(True)

        pb6 = QPushButton(self)
        pb6.setGeometry(QRect(125, 225 + self.offset, 50, 50))
        pb6.setObjectName('6')
        pb6.clicked.connect(lambda : self.tileButtonClicked(pb6))
        pb6.setFlat(True)

        lbl1 = QLabel("파메", self)
        lbl1.setGeometry(QRect(50, 370, 30, 20))

        bmLineEdit = QLineEdit(self)
        bmLineEdit.setGeometry(QRect(75,370,150, 20))

        nextButton = QPushButton("Next", self)
        nextButton.setGeometry(QRect(225, 370, 40, 20))

        lbl2 = QLabel("노메", self)
        lbl2.setGeometry(QRect(50, 400, 40, 20))

        ymLineEdit = QLineEdit(self)
        ymLineEdit.setGeometry(QRect(75,400,150, 20))


        mi_stay_on_top = QAction('Stay On Top', self)
        mi_stay_on_top.setShortcut('Ctrl+T')
        mi_stay_on_top.setCheckable(True)
        mi_stay_on_top.triggered.connect(self.toggle_stay_on_top)

        self.show()

    def selectedComboItem(self, str):
        if str.currentText() == '하드' :
            self.myBoard = ChessBoard.ChessBoard("Hard")
        elif str.currentText() == '노말' :
            self.myBoard = ChessBoard.ChessBoard("Normal")
        self.update()

    def tileButtonClicked(self, btn):
        id = int(btn.objectName())
        loc, val = self.myBoard.get(id)
        self.myBoard.update(loc, max(0, val - 1))
        self.update()

    def toggle_stay_on_top(self):
        if self.mi_stay_on_top.isChecked():
            # enabled
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            # disable
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        # re-show the window after changing flags
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        # self.drawTile(12, 1)  # 12
        # self.drawTile(11, 1)  # 11
        # self.drawTile(1, 1)  # 1
        #
        # self.drawTile(9, 2)  # 9
        # self.drawTile(0, 2)  # 0
        # self.drawTile(3, 2)  # 3
        #
        # self.drawTile(7, 3)  # 7
        # self.drawTile(5, 0)  # 5
        # self.drawTile(6, 0)  # 6
        self.drawTiles(self.myBoard)

    def drawTiles(self, myBoard):
        for x, y in myBoard.chessBoard :
            self.drawTile(x, y)

    def drawTile(self, loc, val, size=100):
        painter = QPainter(self)
        radius = round(size / 2)
        x, y = self.LocToPos[loc]
        if val == 3:
            color = Qt.white
        elif val == 2:
            color = Qt.lightGray
        elif val == 1:
            color = Qt.darkGray
        else:
            color = Qt.black

        painter.setPen(QPen(Qt.black, 2.5, Qt.SolidLine))
        painter.setBrush(QBrush(color, Qt.SolidPattern))

        points = [
            QPoint(x, y - radius + self.offset),
            QPoint(x + radius, y + self.offset),
            QPoint(x, y + radius + self.offset),
            QPoint(x - radius, y + self.offset)
        ]
        poly = QPolygon(points)
        painter.drawPolygon(poly)

    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()

ym = 12
bm = 3
myBoard = ChessBoard.ChessBoard("Hard")
# myBoard = ChessBoard.ChessBoard([(11, 0), (1, 1), (12, 1), (3, 2), (9, 2), (0, 2), (5, 3), (7, 1), (6, 3)])
newBoard, pq = utils.placeMeteor(ym, bm, myBoard)
myBoard = newBoard
print(myBoard.chessBoard)
print(pq)

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    window.setWindowOpacity(0.8)
    sys.exit(App.exec())