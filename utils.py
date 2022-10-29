import ChessBoard
from collections import Counter
from itertools import repeat, chain
import copy

def sort(dic: dict):
    return sorted(dic.items(), key=lambda item: item[1], reverse=True)

def secs_to_minsec(secs: int):
    mins = secs // 60
    secs = secs % 60
    minsec = f'{mins:02}:{secs:02}'
    return minsec

def sortpq(ls: list):
    order = [11, 12, 1, 3, 5, 6, 7, 9, 0]
    return list(chain.from_iterable(repeat(i, c) for i, c in Counter(sorted(ls, key=order.index)).most_common()))

def pqToString(pq):
    if type(pq) is str:
        return pq
    output = ""
    for item in pq:
        output = output + str(item) + ", "
    return output[:-2]


def dispenseBM(i):
    if i == 0:
        return 2
    else:
        return 3 + (i + 1) % 2


def distribute(bm, dic):
    pq = list()
    for loc, val in sort(dic):
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


def distributeUniform(bm, dic):
    pq = list()
    for loc, val in dic.items():
        if val > 1 and bm > 0:
            bm -= 1
            pq += [loc]
            dic[loc] -= 1
    if bm > 0:
        for loc, val in dic.items():
            if bm == 0:
                break
            elif val > 1:
                bm -= 1
                pq += [loc]
    return pq


def updateBoard(pq, chessBoard: ChessBoard):
    for loc in pq:
        chessBoard.update(loc, max(0, chessBoard.get(loc) - 1))
    chessBoard.split()


def placeMeteor(myBoard, difficulty):
    board = copy.deepcopy(myBoard)
    if difficulty == "Hard":
        return placeMeteorHard(board)
    elif difficulty == "Normal":
        return placeMeteorNormal(board)
    elif difficulty == "Safe":
        return placeMeteorSafe(board)


def placeMeteorSafe(myBoard):
    # check availability a priori
    myBoard.split()
    if myBoard.zeros() > 3:
        return "실패"

    if myBoard.bm > myBoard.sum():
        if myBoard.zeros() == 3:
            return "타일복구까지 딜컷"
        else:
            return "노메까지 빡딜"
    else:
        # uniform distribute on top side
        pq = distributeUniform(myBoard.bm, myBoard.top)
        myBoard.bm -= len(pq)
        updateBoard(pq, myBoard)

        # uniform distribute on bot side
        pq_tmp = distributeUniform(myBoard.bm, myBoard.bot)
        myBoard.bm -= len(pq_tmp)
        updateBoard(pq_tmp, myBoard)
        pq += pq_tmp

        # distribute on spr side
        myBoard.adjustSpr(pq)
        pq_tmp = distribute(myBoard.bm, myBoard.spr)
        myBoard.bm -= len(pq_tmp)
        updateBoard(pq_tmp, myBoard)
        pq += pq_tmp
        return pq


def placeMeteorNormal(myBoard):
    # check availability a priori
    myBoard.split()
    if myBoard.zeros() > 3:
        return "실패"
    if myBoard.bm > myBoard.sum():
        if myBoard.zeros() == 3:
            return "타일복구까지 딜컷"
        else:
            return "노메까지 빡딜"
    pq = []
    # best case scenario : 가능하다면 top에 균등배치
    if myBoard.sum("top") >= myBoard.bm:
        pq = distributeUniform(myBoard.bm, myBoard.top)
    # top에 배치 후 잉여 1개일 시
    # top에 1개씩 배치 후 + 1개 spr > bot 배치
    elif myBoard.bm - myBoard.sum("top") == 1:
        if myBoard.sum("spr") >= 1:
            pq = distributeUniform(myBoard.bm - 1, myBoard.top)
            # preferably 가까운 spare로...
            myBoard.adjustSpr(pq)
            pq += distribute(1, myBoard.spr)
        elif myBoard.sum("bot") >= 1:
            pq = distributeUniform(myBoard.bm - 1, myBoard.top) + distributeUniform(1, myBoard.bot)
    # top에 배치 후 2개 이상 잉여분이 생기는 경우
    else:
        # top에 깨진 타일이 없으면 몰아서 깬다
        if myBoard.zeros(myBoard.top) == 0 and myBoard.zeros() < 3:
            if myBoard.ym == 12:
                if myBoard.get(11) == 1:
                    pq = myBoard.bm * [11]
                elif myBoard.get(1) == 1:
                    pq = myBoard.bm * [1]
            elif myBoard.ym == 6:
                if myBoard.get(7) == 1:
                    pq = myBoard.bm * [7]
                elif myBoard.get(5) == 1:
                    pq = myBoard.bm * [5]
        # top에 깨진 타일이 있으면 top -> bot -> spr 나눠서 배치
        else:
            pq = distributeUniform(myBoard.bm, myBoard.top)
            myBoard.bm -= len(pq)
            pq_tmp = distributeUniform(myBoard.bm, myBoard.bot)
            myBoard.bm -= len(pq_tmp)
            pq += pq_tmp
            if myBoard.bm > 0:
                myBoard.adjustSpr(pq)
                pq_tmp += distribute(myBoard.bm, myBoard.spr)
                myBoard.bm -= len(pq_tmp)
                pq += pq_tmp
    updateBoard(pq, myBoard)
    return pq


def placeMeteorHard(myBoard):
    # check availability a priori
    if myBoard.zeros() > 3:
        return "실패"

    myBoard.split()
    pq = distribute(myBoard.bm, myBoard.top) if myBoard.bm == 4 \
        else distributeUniform(myBoard.bm, myBoard.top)

    myBoard.bm -= len(pq)
    updateBoard(pq, myBoard)

    if myBoard.zeros() == 3:
        if myBoard.bm > myBoard.sum():
            return "타일복구까지 딜컷"
    else:
        # top 타일 하나 깨기
        if myBoard.bm > 0 and myBoard.zeros() < 3:
            if myBoard.ym == 12:
                a = 11
                b = 1
            elif myBoard.ym == 6:
                a = 7
                b = 5
            sv_a = (2 - sum(x == a for x in pq)) * [a]
            sv_b = (2 - sum(x == b for x in pq)) * [b]
            if myBoard.get(a) == 0 or myBoard.get(b) == 0:
                sv_a = []
                sv_b = []
            if myBoard.bm >= 2:
                if len(sv_a) >= len(sv_b):
                    myBoard.bm -= len(sv_a)
                    myBoard.update(a, 0)
                    pq += sv_a
                else:
                    myBoard.bm -= len(sv_b)
                    myBoard.update(b, 0)
                    pq += sv_b
            else:
                if a in pq and len(sv_a) > 0:
                    myBoard.bm -= 1
                    myBoard.update(a, 0)
                    pq += [a]
                elif b in pq and len(sv_b) > 0:
                    myBoard.bm -= 1
                    myBoard.update(b, 0)
                    pq += [b]
                else:
                    availability = min(1, len(sv_a))
                    myBoard.bm -= availability
                    myBoard.update(a, 1 - availability)
                    pq += availability * [a]

    if myBoard.bm > 0 and myBoard.bm > myBoard.sum("bot") + myBoard.sum("spr"):
        return "노메까지 빡딜"

    pq_tmp = distribute(myBoard.bm, myBoard.bot) if myBoard.bm == 4 \
        else distributeUniform(myBoard.bm, myBoard.bot)
    myBoard.bm -= len(pq_tmp)
    updateBoard(pq_tmp, myBoard)
    pq += pq_tmp

    myBoard.adjustSpr(pq)
    pq_tmp = distribute(myBoard.bm, myBoard.spr)
    myBoard.bm -= len(pq_tmp)
    updateBoard(pq_tmp, myBoard)
    pq += pq_tmp

    return pq