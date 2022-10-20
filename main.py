from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import ChessBoard, utils
import copy
# from BlurWindow.blurWindow import blur

import sys


def secs_to_minsec(secs: int):
    mins = secs // 60
    secs = secs % 60
    minsec = f'{mins:02}:{secs:02}'
    return minsec


class Window(QMainWindow):
    LocToPos = {12: (150, 50), 11: (100, 100), 1: (200, 100),
                9: (50, 150), 0: (150, 150), 3: (250, 150),
                7: (100, 200), 5: (200, 200), 6: (150, 250)}

    DURATION = 100
    order = [11, 12, 1, 3, 5, 6, 7, 9, 0]
    LocToTime = dict()
    turn = 0
    size = 100
    offset = 40
    locked = False

    def __init__(self):
        super().__init__()
        self.initMode("Hard")
        self.initUI()
        self.showBM()

    def initMode(self, mode):
        for item in self.order:
            self.LocToTime[item] = self.DURATION
        self.mode = mode
        self.myBoard = ChessBoard.ChessBoard(mode)
        self.turn = 0
        self.bm = utils.dispenseBM(self.turn)
        if mode == "Hard":
            self.ym = 12
            self.ymBroken = [5, 6, 7]
        elif mode == "Normal":
            self.ym = 6
            self.bm = utils.dispenseBM(self.turn)
            self.ymBroken = [11, 12, 1]
        tmpBoard = copy.deepcopy(self.myBoard)
        self.pq = utils.placeMeteor(self.ym, self.bm, tmpBoard, mode)

    def initUI(self):
        self.setFixedSize(300, 430)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color:#252740;color:white; font-family:맑은 고딕; font-size:15px")

        self.quitButton = QPushButton('X', self)
        self.quitButton.setGeometry(QRect(280, 0, 20, 20))
        self.quitButton.clicked.connect(QCoreApplication.instance().quit)

        # self.refreshButton = QPushButton('R', self)
        # self.refreshButton.setGeometry(QRect(260, 0, 20, 20))
        # self.refreshButton.clicked.connect(self.refresh)

        self.lockCheckBox = QCheckBox(self)
        self.lockCheckBox.setGeometry(QRect(265, 0, 20, 20))

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setGeometry(QRect(185, 0, 70, 20))
        self.slider.setRange(10, 100)
        self.slider.setValue(80)
        self.slider.valueChanged[int].connect(self.sliderChanged)

        self.timerCheckBox = QCheckBox('타이머 ON', self)
        self.timerCheckBox.setGeometry(QRect(200, 30, 100, 20))
        self.timerCheckBox.setLayoutDirection(Qt.RightToLeft)
        self.timerCheckBox.setObjectName("timerCheckBox")

        self.tileCheckBox = QCheckBox('찬미하라', self)
        self.tileCheckBox.setGeometry(QRect(0, 30, 100, 20))
        # self.tileCheckBox.setLayoutDirection(Qt.RightToLeft)
        # self.tileCheckBox.toggle()
        self.tileCheckBox.stateChanged.connect(self.refresh)

        self.bmLabel = QLabel(self)
        self.bmLabel.setGeometry(QRect(73, 387, 150, 35))
        self.bmLabel.setAlignment(Qt.AlignCenter)
        self.bmLabel.setStyleSheet("font-size:18px; font-weight:bold; color:cyan")
        self.bmLabel.setText(utils.pqToString(self.pq))

        self.applyButton = QPushButton(self)
        self.applyButton.setGeometry(QRect(73, 387, 150, 35))
        self.applyButton.clicked.connect(self.applyButtonClicked)
        self.applyButton.setFlat(True)

        self.nextButton = QPushButton("다음", self)
        self.nextButton.setStyleSheet("font-size:20px; font-weight:bold")
        self.nextButton.setGeometry(QRect(238, 387, 55, 35))
        self.nextButton.clicked.connect(self.nextButtonClicked)
        self.nextButton.setFlat(True)

        self.ymLabel = QLabel(self)
        self.ymLabel.setGeometry(QRect(8, 387, 55, 35))
        self.ymLabel.setAlignment(Qt.AlignCenter)
        self.ymLabel.setStyleSheet("font-size:20px; font-weight:bold; color:yellow")
        self.ymLabel.setText(str(self.ym))

        self.applyYMButton = QPushButton(self)
        self.applyYMButton.setGeometry(QRect(8, 387, 55, 35))
        self.applyYMButton.clicked.connect(lambda: self.ymClicked(self.ym))
        self.applyYMButton.setFlat(True)

        self.diffCB = QComboBox(self)
        self.diffCB.setGeometry(QRect(0, 0, 80, 20))
        self.diffCB.addItem("Hard")
        self.diffCB.addItem("Normal")
        self.diffCB.activated[str].connect(self.reset)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timerTimeout)
        self.timer.start(1000)

        # 3 x 3 timer & labels & tiles
        for loc in self.LocToPos:
            x, y = self.LocToPos[loc]

            self.lbl = QLabel(self)
            self.lbl.setObjectName("lbl{}".format(loc))
            self.lbl.setGeometry((QRect(x - 25, y - 25 + self.offset, 50, 50)))
            self.lbl.setAlignment(Qt.AlignCenter)
            self.lbl.setStyleSheet("background-color:rgba(0,0,0,0)")
            self.lbl.setText(str(secs_to_minsec(self.LocToTime[loc])))
            self.lbl.hide()

            self.bmlbl = QLabel(self)
            self.bmlbl.setObjectName("bmlbl{}".format(loc))
            self.bmlbl.setGeometry((QRect(x - 25, y - 25 + self.offset, 50, 50)))
            self.bmlbl.setAlignment(Qt.AlignCenter)
            self.bmlbl.setStyleSheet("background-color:rgba(0,0,0,0);color:blue;font-size:20px;")
            self.bmlbl.hide()

            self.button = QPushButton(self)
            self.button.setObjectName("btn{}".format(loc))
            self.button.setGeometry(QRect(x - 25, y - 25 + self.offset, 50, 50))
            self.button.clicked.connect(lambda ch, loc=loc: self.tileButtonClicked(loc))
            self.button.setContextMenuPolicy(Qt.CustomContextMenu)
            self.button.customContextMenuRequested.connect(lambda ch, loc=loc: self.tileButtonRightClicked(loc))
            self.button.setFlat(True)

        self.nb12 = QPushButton(self)
        self.nb12.setGeometry(QRect(130, 0, 40, 40))
        self.nb12.clicked.connect(lambda: self.ymClicked(12))
        self.nb12.setContextMenuPolicy(Qt.CustomContextMenu)
        self.nb12.customContextMenuRequested.connect(self.ymRightClicked)
        self.nb12.setFlat(True)

        self.nb6 = QPushButton(self)
        self.nb6.setGeometry(QRect(130, 340, 40, 40))
        self.nb6.clicked.connect(lambda: self.ymClicked(6))
        self.nb6.setContextMenuPolicy(Qt.CustomContextMenu)
        self.nb6.customContextMenuRequested.connect(self.ymRightClicked)
        self.nb6.setFlat(True)

        self.switchYM()

        self.show()

    def printhi(self):
        print("clicked")

    # reset
    def reset(self, cb):
        self.hideBM()
        self.mode = cb
        self.initMode(cb)
        self.bmLabel.setText(utils.pqToString(self.pq))
        self.ymLabel.setText(str(self.ym))
        self.switchYM()
        self.showBM()
        self.update()

    def switchYM(self):
        if self.ym == 12:
            self.nb12.setText("★")
            self.nb12.setStyleSheet("color:yellow;font-size:33px")
            self.nb6.setText("☆")
            self.nb6.setStyleSheet("color:Gray;font-size:33px")
        elif self.ym == 6:
            self.nb6.setText("★")
            self.nb6.setStyleSheet("color:yellow;font-size:33px")
            self.nb12.setText("☆")
            self.nb12.setStyleSheet("color:Gray;font-size:33px")

    def showBM(self):
        if type(self.pq) is list:
            self.pq = utils.cycleSort(self.pq)
            for loc in self.pq:
                bmlbl = self.findChild(QLabel, "bmlbl{}".format(loc))
                if self.pq.count(loc) == 4:
                    bmlbl.setText("★★\n★★")
                elif self.pq.count(loc) == 3:
                    bmlbl.setText("★\n★★")
                elif self.pq.count(loc) == 2:
                    bmlbl.setText("★★")
                elif self.pq.count(loc) == 1:
                    bmlbl.setText("★")
                bmlbl.show()

    def hideBM(self):
        if type(self.pq) is list:
            self.pq = utils.cycleSort(self.pq)
            for loc in self.pq:
                bmlbl = self.findChild(QLabel, "bmlbl{}".format(loc))
                bmlbl.hide()

    def refresh(self):
        self.hideBM()
        tmpBoard = copy.deepcopy(self.myBoard)
        if self.tileCheckBox.isChecked():
            self.pq = utils.placeMeteor(self.ym, self.bm, tmpBoard, "Safe")
        else:
            self.pq = utils.placeMeteor(self.ym, self.bm, tmpBoard, self.mode)
        if type(self.pq) is list:
            self.pq = utils.cycleSort(self.pq)
            self.showBM()
        self.switchYM()
        self.bmLabel.setText(utils.pqToString(self.pq))
        self.ymLabel.setText(str(self.ym))
        self.update()

    def timerTimeout(self):
        for loc, val in self.myBoard.chessBoard:
            time = self.LocToTime[loc]
            lbl = self.findChild(QLabel, "lbl{}".format(loc))
            if self.timerCheckBox.isChecked() and val == 0:
                self.LocToTime[loc] -= 1  # countdown 1 sec
                lbl.setText(secs_to_minsec(time))
                lbl.show()
                if self.LocToTime[loc] == 0:
                    self.myBoard.update(loc, 3)
                    self.LocToTime[loc] = self.DURATION
                    self.refresh()
            else:
                lbl.hide()
        self.update()

    def sliderChanged(self, value):
        opacity = value / 100
        super().setWindowOpacity(opacity)

    def tileButtonClicked(self, id):
        loc, val = self.myBoard.get(id)
        if val > 1:
            self.myBoard.update(loc, val - 1)
        elif val == 1:
            self.myBoard.update(loc, 0)
        self.refresh()

    def tileButtonRightClicked(self, id):
        loc, val = self.myBoard.get(id)
        if val == 0:
            self.myBoard.update(loc, 3)
            self.LocToTime[loc] = self.DURATION
        else:
            self.myBoard.update(loc, min(3, val + 1))
        self.refresh()

    def ymClicked(self, loc):
        if loc == 12:
            index = [12, 11, 1]
            self.ym = 6
        elif loc == 6:
            index = [6, 7, 5]
            self.ym = 12
        self.ymBroken = []
        for i in index:
            _, val = self.myBoard.get(i)
            if val > 0:
                self.myBoard.update(i, 0)
                self.ymBroken += [i]
        self.refresh()

    def ymRightClicked(self):
        if self.ymBroken:
            for loc in self.ymBroken:
                self.myBoard.update(loc, 3)
                self.LocToTime[loc] = self.DURATION
            self.ymBroken = []
            self.refresh()

    def nextButtonClicked(self):
        # utils.updateBoard(self.pq, self.myBoard)
        self.turn += 1
        self.bm = utils.dispenseBM(self.turn)
        self.refresh()

    def applyButtonClicked(self):
        if type(self.pq) is list :
            utils.updateBoard(self.pq, self.myBoard)
            self.nextButtonClicked()

    def paintEvent(self, event):
        self.drawTiles()
        self.drawRect()

    def drawRect(self):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.yellow, 3, Qt.SolidLine))
        painter.drawRect(5, 385, 60, 40)
        painter.setPen(QPen(Qt.cyan, 3, Qt.SolidLine))
        painter.drawRect(70, 385, 160, 40)
        painter.setPen(QPen(Qt.white, 3, Qt.SolidLine))
        painter.drawRect(235, 385, 60, 40)

    def drawTiles(self):
        for x, y in self.myBoard.chessBoard:
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
        painter.setPen(QPen(QColor('#ECECEC'), 2.5, Qt.SolidLine))
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
        if not self.lockCheckBox.isChecked():
            self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        if not self.lockCheckBox.isChecked():
            delta = QPoint(event.globalPos() - self.oldPosition)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPosition = event.globalPos()


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    window.setWindowOpacity(0.8)
    sys.exit(App.exec())
