from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import ChessBoard, utils
import copy
#from BlurWindow.blurWindow import blur

import sys

class tileButton(QPushButton):
    def __init__(self):
        super().__init__()
        timer = QTimer(self, interval=1000)

class Window(QMainWindow):
    LocToPos = {12:(150,50), 11:(100, 100), 1:(200, 100),
            9:(50, 150), 0:(150, 150), 3:(250, 150),
            7:(100, 200), 5:(200, 200), 6:(150, 250)}
    size = 100
    offset = 40
    tileClicked = 0

    def __init__(self):
        super().__init__()
        self.initMode("Hard")
        self.initUI()

    def initMode(self, mode):
        if mode == "Hard":
            self.mode = mode
            self.myBoard = ChessBoard.ChessBoard("Hard")
            self.ym = 12
            self.bm = 3
            self.ymBroken = [5, 6, 7]
        elif mode == "Normal":
            self.mode = mode
            self.myBoard = ChessBoard.ChessBoard("Normal")
            self.ym = 6
            self.bm = 3
            self.ymBroken = [11, 12, 1]
        tmpBoard = copy.deepcopy(self.myBoard)
        self.pq = utils.placeMeteor(self.ym, 2, tmpBoard, mode)

    def initUI(self):
        self.setFixedSize(300, 440)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color:#252740;color:white")

        self.quitButton = QPushButton('X', self)
        self.quitButton.setGeometry(QRect(280,0,20,20))
        self.quitButton.clicked.connect(QCoreApplication.instance().quit)

        self.refreshButton = QPushButton('R', self)
        self.refreshButton.setGeometry(QRect(260, 0, 20, 20))
        self.refreshButton.clicked.connect(self.refresh)

        self.timerCheckBox = QCheckBox('타이머 ON', self)
        self.timerCheckBox.setGeometry(QRect(220, 30, 80, 20))
        self.timerCheckBox.setLayoutDirection(Qt.RightToLeft)
        self.timerCheckBox.setObjectName("timerCheckBox")

        self.tileCheckBox = QCheckBox('타일파괴방지', self)
        self.tileCheckBox.setGeometry(QRect(0, 30, 100, 20))
        # self.tileCheckBox.setLayoutDirection(Qt.RightToLeft)
        #self.tileCheckBox.toggle()
        self.tileCheckBox.stateChanged.connect(self.refresh)

        self.lbl1 = QLabel("파메", self)
        self.lbl1.setGeometry(QRect(40, 375, 30, 20))

        self.bmLineEdit = QLineEdit(self)
        self.bmLineEdit.setGeometry(QRect(75, 375, 150, 20))
        self.bmLineEdit.setAlignment(Qt.AlignCenter)
        self.bmLineEdit.setText(str(self.pq))
        self.bmLineEdit.setReadOnly(True)

        self.nextButton = QPushButton("Next", self)
        self.nextButton.setGeometry(QRect(235, 375, 50, 20))
        self.nextButton.clicked.connect(self.nextButtonClicked)

        self.lbl2 = QLabel("노메", self)
        self.lbl2.setGeometry(QRect(40, 400, 40, 20))

        self.ymLineEdit = QLineEdit(self)
        self.ymLineEdit.setGeometry(QRect(75, 400, 150, 20))
        self.ymLineEdit.setAlignment(Qt.AlignCenter)
        self.ymLineEdit.setText(str(self.ym))
        self.ymLineEdit.setReadOnly(True)

        self.diffCB = QComboBox(self)
        self.diffCB.setGeometry(QRect(0, 0, 70, 20))
        self.diffCB.addItem("Hard")
        self.diffCB.addItem("Normal")
        self.diffCB.activated[str].connect(self.reset)

        # self.lbl = QLabel('1:40', self)
        # self.lbl.setGeometry((QRect(125,25+self.offset, 50, 50)))
        # self.lbl.setAlignment(Qt.AlignCenter)
        # self.lbl.setStyleSheet("background-color:rgba(0,0,0,0)")

        # 3 x 3 tiles
        for loc in self.LocToPos :
            x, y = self.LocToPos[loc]
            self.button = QPushButton(self)
            self.button.setGeometry(QRect(x-25, y-25+self.offset, 50, 50))
            self.button.clicked.connect(lambda ch, loc = loc: self.tileButtonClicked(loc))
            self.button.setContextMenuPolicy(Qt.CustomContextMenu)
            self.button.customContextMenuRequested.connect(lambda ch, loc = loc: self.tileButtonRightClicked(loc))
            self.button.setFlat(True)



        self.nb6 = QPushButton("★",self)
        self.nb6.setGeometry(QRect(125, 340, 50, 20))
        self.nb6.clicked.connect(lambda : self.ymClicked(6))
        self.nb6.setContextMenuPolicy(Qt.CustomContextMenu)
        self.nb6.customContextMenuRequested.connect(lambda : self.ymRightClicked())

        self.nb12 = QPushButton("★", self)
        self.nb12.setGeometry(QRect(125, 20, 50, 20))
        self.nb12.clicked.connect(lambda : self.ymClicked(12))
        self.nb12.setContextMenuPolicy(Qt.CustomContextMenu)
        self.nb12.customContextMenuRequested.connect(lambda : self.ymRightClicked())
        self.show()

    #reset
    def reset(self, cb):
        self.mode = cb
        self.initMode(cb)
        self.bmLineEdit.setText(str(self.pq))
        self.ymLineEdit.setText(str(self.ym))
        self.update()

    def refresh(self):
        self.bm = 3 + self.bm % 2
        tmpBoard = copy.deepcopy(self.myBoard)
        if self.tileCheckBox.isChecked() :
            self.pq = utils.placeMeteor(self.ym, self.bm, tmpBoard, "Safe")
        else :
            self.pq = utils.placeMeteor(self.ym, self.bm, tmpBoard, self.mode)
        self.bmLineEdit.setText(str(self.pq))
        self.ymLineEdit.setText(str(self.ym))
        self.bm = 3 + self.bm % 2
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
        self.refresh()
        # self.update()

    def ymClicked(self, loc):
        if loc == 12 :
            index = [12, 11, 1]
            self.ym = 6
        elif loc == 6 :
            index = [6, 7, 5]
            self.ym = 12
        self.ymBroken = []
        for i in index :
            _, val = self.myBoard.get(i)
            if val > 0 :
                self.myBoard.update(i, 0)
                self.ymBroken += [i]
        self.refresh()

    def ymRightClicked(self):
        if self.ymBroken :
            for loc in self.ymBroken :
                self.myBoard.update(loc, 3)
            self.ymBroken = []
            self.refresh()

    def nextButtonClicked(self):
        tmpBoard = copy.deepcopy(self.myBoard)
        if self.tileCheckBox.isChecked() :
            self.pq = utils.placeMeteor(self.ym, self.bm, tmpBoard, "Safe")
        else :
            self.pq = utils.placeMeteor(self.ym, self.bm, tmpBoard, self.mode)
        self.bmLineEdit.setText(str(self.pq))
        self.bm = 3 + self.bm % 2 # 3 -> 4 -> 3 -> 4 -> ...
        self.update()

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
        painter.setPen(QPen(Qt.white, 2.5, Qt.SolidLine))
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
    window.setWindowOpacity(0.8)
    sys.exit(App.exec())