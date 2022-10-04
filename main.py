# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import ChessBoard
from PyQt5.QtWidgets import QApplication, QWidget

def sort(list):
    return sorted(list, key = lambda x : (x[1]), reverse=True)

def distribute(bm, ls):
    pq = list()
    for loc, val in sort(ls):
        if val == 3:
            if bm >= 2:
                bm -= 2
                pq += 2 * [loc]
            elif bm == 1:
                bm -= 1
                pq.append(loc)
        elif val == 2 and bm >= 1:
            bm -= 1
            pq.append(loc)
    return pq

def updateBoard(pq, chessBoard: ChessBoard):
    newBoard = chessBoard
    for loc in pq:
        x, y = newBoard.get(loc)
        new_y = max(0, y - 1)
        newBoard.update(x, new_y)
    return newBoard


def placeMeteor(ym, bm, myBoard):
    myBoard.divide(ym)
    print(myBoard.top)
    print(myBoard.spr)
    print(myBoard.bot)
    print("ym = " + str(ym) + " bm = " + str(bm))
    pq = distribute(bm, myBoard.top)
    bm -= len(pq)
    myBoard = updateBoard(pq, myBoard)
    myBoard.divide(ym)

    if myBoard.zeros() == 3:
        if bm > myBoard.sum():
            return 0

    else:
        if bm > 0 and myBoard.zeros() < 3:
            if ym == 12:
                a = 11;
                b = 1
            elif ym == 6:
                a = 7;
                b = 5
            sv_a = (2 - sum(x == a for x in pq)) * [a]
            sv_b = (2 - sum(x == b for x in pq)) * [b]

            if myBoard.get(a)[1] == 0 or myBoard.get(b)[1] == 0:
                sv_a = []
                sv_b = []

            if bm >= 2:
                if len(sv_a) >= len(sv_b):
                    bm -= len(sv_a)
                    myBoard.update(a, 0)
                    pq += sv_a
                else:
                    bm -= len(sv_b)
                    myBoard.update(b, 0)
                    pq += sv_b
            else:
                if a in pq and len(sv_a) > 0:
                    bm -= 1
                    myBoard.update(a, 0)
                    pq += [a]
                elif b in pq and len(sv_b) > 0:
                    bm -= 1
                    myBoard.update(b, 0)
                    pq += [b]
                else:
                    availability = min(1, len(sv_a))
                    bm -= availability
                    myBoard.update(a, 1 - availability)
                    pq += availability * [a]

    myBoard.divide(ym)
    if bm > 0 and bm > myBoard.sum("bot") + myBoard.sum("spr"):
        return 0

    pq_tmp = distribute(bm, myBoard.bot)
    bm -= len(pq_tmp)
    myBoard = updateBoard(pq_tmp, myBoard)
    pq += pq_tmp
    myBoard.divide(ym)

    pq_tmp = distribute(bm, myBoard.spr)
    bm -= len(pq_tmp)
    myBoard = updateBoard(pq_tmp, myBoard)
    pq += pq_tmp
    myBoard.divide(ym)

    return myBoard, pq


ym = 6
bm = 4
# myBoard = ChessBoard("Hard")
myBoard = ChessBoard.ChessBoard([(11, 1), (1, 1), (12, 1), (3, 3), (9, 2), (0, 2), (5, 3), (7, 3), (6, 2)])
newBoard, pq = placeMeteor(ym, bm, myBoard)
myBoard = newBoard
print(myBoard.chessBoard)
print(pq)


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('My First Application')
        self.move(300, 300)
        self.resize(400, 200)
        self.show()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

