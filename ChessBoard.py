class ChessBoard:
    def __init__(self, difficulty):
        self.bm = 2
        self.chessBoard = dict()
        self.difficulty = difficulty
        if self.difficulty == "Hard":
            self.chessBoard = {11: 2, 1: 1, 12: 2, 3: 3, 9: 2, 0: 2, 5: 0, 7: 0, 6: 0}
            self.ym = 12
        elif self.difficulty == "Normal":
            self.chessBoard = {11: 0, 1: 0, 12: 0, 3: 3, 9: 3, 0: 2, 5: 3, 7: 3, 6: 3}
            self.ym = 6
        self.split()

    def get(self, loc):
        return self.chessBoard[loc]

    def filterByKey(self, keys: list):
        return {x: self.chessBoard[x] for x in keys}

    def update(self, loc, val):
        self.chessBoard[loc] = val

    def split(self):
        sprKey = [3, 9, 0]
        if self.difficulty == "Hard":
            topKey = [6, 7, 5] if self.ym == 6 else [11, 1, 12]
            botKey = [11, 1, 12] if self.ym == 6 else [6, 7, 5]
        elif self.difficulty == "Normal":
            topKey = [7, 5, 6] if self.ym == 6 else [11, 1, 12]
            botKey = [11, 1, 12] if self.ym == 6 else [7, 5, 6]
        self.top = self.filterByKey(topKey)
        self.bot = self.filterByKey(botKey)
        self.spr = self.filterByKey(sprKey)

    def adjustSpr(self, pq):
        distToThree = 0
        distToNine = 0
        for loc in pq:
            distToThree += self.hamiltonDist(loc, 3)
            distToNine += self.hamiltonDist(loc, 9)
        # same avg distance to tile nine and three
        if distToNine == distToThree:
            # adjust spr according to value
            sprKey = [3, 9, 0] if self.get(3) >= self.get(9) else [9, 3, 0]
        # else update by distance
        else:
            sprKey = [3, 9, 0] if distToNine > distToThree else [9, 3, 0]
        self.spr = self.filterByKey(sprKey)

    def hamiltonDist(self, p1, p2):
        distMap = {12: (0, 0), 1: (0, 1), 3: (0, 2),
                   11: (1, 0), 0: (1, 1), 5: (1, 2),
                   9: (2, 0), 7: (2, 1), 6: (2, 2)}
        x1, y1 = distMap[p1]
        x2, y2 = distMap[p2]
        return abs(x1 - x2) + abs(y1 - y2)

    def zeros(self, dic=None):
        if dic == None:
            return sum(v == 0 for k, v in self.chessBoard.items())
        return sum(v == 0 for k, v in dic.items())

    def sum(self, type="all"):
        if type == "all":
            return sum(v for loc, v in self.chessBoard.items()) + self.zeros() - 9
        elif type == "top":
            return sum(v for loc, v in self.top.items()) + self.zeros(self.top) - 3
        elif type == "bot":
            return sum(v for loc, v in self.bot.items()) + self.zeros(self.bot) - 3
        elif type == "spr":
            return sum(v for loc, v in self.spr.items()) + self.zeros(self.spr) - 3