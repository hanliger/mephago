class ChessBoard:

    def __init__(self, difficulty):
        self.chessBoard = list()
        self.difficulty = difficulty
        if self.difficulty == "Hard":
            self.chessBoard = [(11, 2), (1, 1), (12, 2), (3, 3), (9, 2), (0, 2), (5, 0), (7, 0), (6, 0)]
        elif self.difficulty == "Normal":
            self.chessBoard = [(11, 0), (1, 0), (12, 0), (3, 3), (9, 3), (0, 3), (5, 3), (7, 3), (6, 3)]
        elif type(self.difficulty) is list:
            self.chessBoard = self.difficulty
        else: # 3x3 clean board
            self.chessBoard = [(11, 3), (1, 3), (12, 3), (3, 3), (9, 3), (0, 3), (5, 3), (7, 3), (6, 3)]

    def get(self, loc):
        for x, y in self.chessBoard:
            if x == loc:
                return (x, y)

    def update(self, loc, val):
        for i, tup in enumerate(self.chessBoard):
            if tup[0] == loc:
                self.chessBoard[i] = (loc, val)

    def split(self, ym):
        self.spr = [self.get(3), self.get(9), self.get(0)]
        if self.difficulty == "Hard" :
            if ym == 6:
                self.top = [self.get(6), self.get(7), self.get(5)]
                self.bot = [self.get(11), self.get(1), self.get(12)]
            elif ym == 12:
                self.bot = [self.get(6), self.get(7), self.get(5)]
                self.top = [self.get(11), self.get(1), self.get(12)]
        elif self.difficulty == "Normal" :
            if ym == 6:
                self.top = [self.get(7), self.get(5), self.get(6)]
                self.bot = [self.get(11), self.get(1), self.get(12)]
            elif ym == 12:
                self.bot = [self.get(7), self.get(5), self.get(6)]
                self.top = [self.get(11), self.get(1), self.get(12)]

    def adjustSpr(self, pq):
        distToThree = 0
        distToNine = 0
        for loc in pq :
            distToThree += self.hamiltonDist(loc,3)
            distToNine += self.hamiltonDist(loc,9)
        # same avg distance to tile nine and three
        if distToNine == distToThree :
            # adjust spr according to value
            if self.get(3)[1] >= self.get(9)[1] :
                self.spr = [self.get(3), self.get(9), self.get(0)]
            else :
                self.spr = [self.get(9), self.get(3), self.get(0)]
        #
        elif distToNine > distToThree :
            self.spr = [self.get(3), self.get(9), self.get(0)]
        else :
            self.spr = [self.get(9), self.get(3), self.get(0)]

    def hamiltonDist(self, p1, p2):
        distMap = {12:(0,0), 1:(0,1), 3:(0,2),
                   11:(1,0), 0:(1,1), 5:(1,2),
                   9:(2,0), 7:(2,1), 6:(2,2)}
        x1, y1 = distMap[p1]
        x2, y2 = distMap[p2]
        return abs(x1-x2) + abs(y1-y2)

    def zeros(self, ls=None):
        if ls == None :
            return sum(y == 0 for x, y in self.chessBoard)
        return sum(y == 0 for x, y in ls)

    def sum(self, type="all"):
        if type == "all":
            return sum(y for x, y in self.chessBoard) + self.zeros(self.chessBoard) - 9
        elif type == "top":
            return sum(y for x, y in self.top) + self.zeros(self.top) - 3
        elif type == "bot":
            return sum(y for x, y in self.bot) + self.zeros(self.bot) - 3
        elif type == "spr":
            return sum(y for x, y in self.spr) + self.zeros(self.spr) - 3
