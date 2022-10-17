import ChessBoard

def sort(ls:list):
    return sorted(ls, key = lambda x : (x[1]), reverse=True)

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

def distributeNormal(bm, ls) :
    pq = list()
    for loc, val in ls :
        if val > 1 and bm > 0:
            bm -= 1
            pq += [loc]
            i = ls.index((loc,val))
            ls[i] = (loc, val - 1)
    if bm > 0 :
        for loc, val in ls :
            if bm == 0 :
                break
            elif val > 1 :
                bm -= 1
                if loc in pq :
                    i = pq.index(loc)
                    pq = pq[0:i] + [loc] + pq[i:len(pq)]
                else :
                    pq += [loc]
    return pq

def updateBoard(pq, chessBoard: ChessBoard):
    for loc in pq:
        x, y = chessBoard.get(loc)
        chessBoard.update(x, max(0, y - 1))

def placeMeteor (ym, bm, myBoard, difficulty) :
    if difficulty == "Hard" :
        return placeMeteorHard(ym, bm, myBoard)
    elif difficulty == "Normal" :
        return placeMeteorNormal(ym, bm, myBoard)
    elif difficulty == "Safe" :
        return placeMeteorSafe (ym, bm, myBoard)

def placeMeteorSafe (ym, bm, myBoard) :
    # check availability a priori
    if myBoard.zeros() > 3 :
        print("failed")
        return 0
    if bm > myBoard.sum():
        print("dps gogo")
        return 0
    else :
        # uniform distribute on top side
        myBoard.split(ym)
        pq = distributeNormal(bm, myBoard.top)
        bm -= len(pq)
        updateBoard(pq, myBoard)

        # uniform distribute on bot side
        myBoard.split(ym)
        pq_tmp = distributeNormal(bm, myBoard.bot)
        bm -= len(pq_tmp)
        updateBoard(pq_tmp, myBoard)
        pq += pq_tmp

        # distribute on spr side
        myBoard.split(ym)
        myBoard.adjustSpr(pq)
        pq_tmp = distribute(bm, myBoard.spr)
        bm -= len(pq_tmp)
        updateBoard(pq_tmp, myBoard)
        pq += pq_tmp
        myBoard.split(ym)

        return pq

def placeMeteorNormal(ym, bm, myBoard) :
    # check availability a priori
    myBoard.split(ym)
    if myBoard.zeros() > 3 :
        print("failed")
        return 0
    if myBoard.zeros() == 3 and bm > myBoard.sum():
        print("dpscut")
        return 0
    pq = []
    # best case scenario : 가능하다면 top에 균등배치
    if myBoard.sum("top") >= bm :
        pq = distributeNormal(bm, myBoard.top)
    # top에 배치 후 잉여 1개일 시
    # top에 1개씩 배치 후 + 1개 spr > bot 배치
    elif bm - myBoard.sum("top") == 1 :
        if myBoard.sum("spr") >= 1 :
            pq = distributeNormal(bm - 1, myBoard.top)
            # preferably 가까운 spare로...
            myBoard.adjustSpr(pq)
            pq += distribute(1, myBoard.spr)
        elif myBoard.sum("bot") >= 1 :
            pq = distributeNormal(bm - 1, myBoard.top) + distributeNormal(1, myBoard.bot)
    # top에 배치 후 2개 이상 잉여분이 생기는 경우
    else :
        #top에 깨진 타일이 없으면 몰아서 깬다
        if myBoard.zeros() < 3 and myBoard.zeros(myBoard.top) == 0 :
            if ym == 12 :
                if myBoard.get(11)[1] == 1 :
                    pq = bm*[11]
                elif myBoard.get(1)[1] == 1 :
                    pq = bm*[1]
            elif ym == 6 :
                if myBoard.get(7)[1] == 1 :
                    pq = bm*[7]
                elif myBoard.get(5)[1] == 1 :
                    pq = bm*[5]
        #top에 깨진 타일이 있으면 top -> bot -> spr 나눠서 배치
        else :
            pq = distributeNormal(bm, myBoard.top)
            bm -= len(pq)
            pq_tmp = distributeNormal(bm, myBoard.bot)
            bm -= len(pq_tmp)
            pq += pq_tmp
            if bm > 0 :
                myBoard.adjustSpr(pq)
                pq_tmp += distribute(bm, myBoard.spr)
                bm -= len(pq_tmp)
                pq += pq_tmp
    updateBoard(pq, myBoard)
    myBoard.split(ym)
    return pq

def placeMeteorHard(ym, bm, myBoard):
    # check availability a priori
    if myBoard.zeros() > 3 :
        print("failed")
        return 0

    myBoard.split(ym)
    pq = distribute(bm, myBoard.top)
    bm -= len(pq)
    updateBoard(pq, myBoard)

    myBoard.split(ym)
    if myBoard.zeros() == 3:
        if bm > myBoard.sum():
            print("dpscut")
            return 0
    else:
        if bm > 0 and myBoard.zeros() < 3:
            if ym == 12:
                a = 11
                b = 1
            elif ym == 6:
                a = 7
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

    myBoard.split(ym)

    if bm > 0 and bm > myBoard.sum("bot") + myBoard.sum("spr"):
        print("dpscut")
        return 0

    pq_tmp = distribute(bm, myBoard.bot)
    bm -= len(pq_tmp)
    updateBoard(pq_tmp, myBoard)
    pq += pq_tmp
    myBoard.split(ym)

    myBoard.adjustSpr(pq)
    pq_tmp = distribute(bm, myBoard.spr)
    bm -= len(pq_tmp)
    updateBoard(pq_tmp, myBoard)
    pq += pq_tmp
    myBoard.split(ym)

    return pq