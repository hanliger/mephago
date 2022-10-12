from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import ChessBoard, utils
import copy
#from BlurWindow.blurWindow import blur

import sys

class Window(QMainWindow):
    LocToPos = {12:(150,50), 11:(100, 100), 1:(200, 100),
            9:(50, 150), 0:(150, 150), 3:(250, 150),
            7:(100, 200), 5:(200, 200), 6:(150, 250)}
    size = 100
    offset = 40
    tileClicked = 0

    def __init__(self):
        super().__init__()
        self.myBoard = ChessBoard.ChessBoard("Hard")
        self.ym = 12
        self.bm = 3
        tmpBoard = copy.deepcopy(self.myBoard)
        self.pq = utils.placeMeteor(self.ym, 2, tmpBoard)
        self.initUI()

    def initUI(self):
        self.setFixedSize(300, 440)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        quitButton = QPushButton('X', self)
        quitButton.setGeometry(QRect(280,0,20,20))
        quitButton.clicked.connect(QCoreApplication.instance().quit)

        refreshButton = QPushButton('R', self)
        refreshButton.setGeometry(QRect(260, 0, 20, 20))
        refreshButton.clicked.connect(lambda : self.reset(diffCB))

        timerCheckBox = QCheckBox('타이머 ON', self)
        timerCheckBox.setGeometry(QRect(220, 30, 80, 20))
        timerCheckBox.setLayoutDirection(Qt.RightToLeft)
        timerCheckBox.setObjectName("timerCheckBox")
        lbl1 = QLabel("파메", self)
        lbl1.setGeometry(QRect(40, 375, 30, 20))

        self.bmLineEdit = QLineEdit(self)
        self.bmLineEdit.setGeometry(QRect(75, 375, 150, 20))
        self.bmLineEdit.setAlignment(Qt.AlignCenter)
        self.bmLineEdit.setText(str(self.pq))
        self.bmLineEdit.setReadOnly(True)

        nextButton = QPushButton("Next", self)
        nextButton.setGeometry(QRect(235, 375, 50, 20))
        nextButton.clicked.connect(lambda: self.nextButtonClicked())

        lbl2 = QLabel("노메", self)
        lbl2.setGeometry(QRect(40, 400, 40, 20))

        self.ymLineEdit = QLineEdit(self)
        self.ymLineEdit.setGeometry(QRect(75, 400, 150, 20))
        self.ymLineEdit.setAlignment(Qt.AlignCenter)
        self.ymLineEdit.setText(str(self.ym))
        self.ymLineEdit.setReadOnly(True)

        diffCB = QComboBox(self)
        diffCB.setGeometry(QRect(0, 0, 60, 20))
        diffCB.addItem('하드')
        diffCB.addItem('노말')
        diffCB.activated[str].connect(lambda : self.selectedComboItem(diffCB))

        # 3 x 3 tiles
        for loc in self.LocToPos :
            x, y = self.LocToPos[loc]
            button = QPushButton(self)
            button.setGeometry(QRect(x-25, y-25+self.offset, 50, 50))
            button.clicked.connect(lambda ch, loc = loc: self.tileButtonClicked(loc))
            button.setContextMenuPolicy(Qt.CustomContextMenu)
            button.customContextMenuRequested.connect(lambda ch, loc = loc: self.tileButtonRightClicked(loc))
            button.setFlat(True)

        nb6 = QPushButton("★",self)
        nb6.setGeometry(QRect(125, 340, 50, 20))
        nb6.clicked.connect(lambda : self.ym6Clicked())

        nb12 = QPushButton("★", self)
        nb12.setGeometry(QRect(125, 20, 50, 20))
        nb12.clicked.connect(lambda : self.ym12Clicked())

        mi_stay_on_top = QAction('Stay On Top', self)
        mi_stay_on_top.setShortcut('Ctrl+T')
        mi_stay_on_top.setCheckable(True)
        mi_stay_on_top.triggered.connect(self.toggle_stay_on_top)

        self.show()

    #reset
    def reset(self, str):
        if str.currentText() == '하드' :
            self.myBoard = ChessBoard.ChessBoard("Hard")
            self.ym = 12
        elif str.currentText() == '노말' :
            self.myBoard = ChessBoard.ChessBoard("Normal")
            self.ym = 6
        tmpBoard = copy.deepcopy(self.myBoard)
        self.pq = utils.placeMeteor(self.ym, 2, tmpBoard)
        # self.bmLineEdit.setText(str(self.pq))
        # self.ymLineEdit.setText(str(self.ym))
        self.update()

    def tileButtonClicked(self, id):
        # id = int(btn.objectName())
        loc, val = self.myBoard.get(id)
        self.myBoard.update(loc, max(0, val - 1))
        self.update()

    def tileButtonRightClicked(self, id):
        loc, val = self.myBoard.get(id)
        if val == 0 :
            self.myBoard.update(loc, 3)
        else :
            self.myBoard.update(loc, min(3, val + 1))
        self.update()

    def ym12Clicked(self):
        self.myBoard.update(12, 0)
        self.myBoard.update(11, 0)
        self.myBoard.update(1, 0)
        self.ym = 6
        self.ymLineEdit.setText(str(self.ym))
        self.update()

    def ym6Clicked(self):
        self.myBoard.update(6, 0)
        self.myBoard.update(7, 0)
        self.myBoard.update(5, 0)
        self.ym = 12
        self.ymLineEdit.setText(str(self.ym))
        self.update()

    def nextButtonClicked(self):
        print (self.bm)
        tmpBoard = copy.deepcopy(self.myBoard)
        self.pq = utils.placeMeteor(self.ym, self.bm, tmpBoard)
        self.bmLineEdit.setText(str(self.pq))
        self.bm = 3 + self.bm % 2 # 3 -> 4 -> 3 -> 4 -> ...
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

# ym = 12
# bm = 3
# myBoard = ChessBoard.ChessBoard("Hard")
# # myBoard = ChessBoard.ChessBoard([(11, 0), (1, 1), (12, 1), (3, 2), (9, 2), (0, 2), (5, 3), (7, 1), (6, 3)])
# newBoard, pq = utils.placeMeteor(ym, bm, myBoard)
# myBoard = newBoard
# print(myBoard.chessBoard)
# print(pq)

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    # window.setWindowOpacity(0.8)
    sys.exit(App.exec())