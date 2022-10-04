class ChessBoard:

    def __init__(self, difficulty):
        self.chessBoard = list()
        if difficulty == "Hard":
            self.chessBoard = [(11, 2), (1, 1), (12, 2), (3, 3), (9, 2), (0, 2), (5, 0), (7, 0), (6, 0)]
        elif difficulty == "Normal":
            self.chessBoard = [(11, 0), (1, 0), (12, 0), (3, 3), (9, 3), (0, 3), (5, 3), (7, 3), (6, 3)]
        elif type(difficulty) is list:
            self.chessBoard = difficulty
        else:
            self.chessBoard = [(11, 3), (1, 3), (12, 3), (3, 3), (9, 3), (0, 3), (5, 3), (7, 3), (6, 3)]


    def get(self, loc):
        for x, y in self.chessBoard:
            if x == loc:
                return (x, y)


    def update(self, loc, val):
        for i, tup in enumerate(self.chessBoard):
            if tup[0] == loc:
                self.chessBoard[i] = (loc, val)


    def divide(self, ym):
        self.spr = [self.get(3), self.get(9), self.get(0)]
        if ym == 6:
            self.top = [self.get(6), self.get(7), self.get(5)]
            self.bot = [self.get(12), self.get(11), self.get(1)]
        elif ym == 12:
            self.bot = [self.get(6), self.get(7), self.get(5)]
            self.top = [self.get(12), self.get(11), self.get(1)]


    def zeros(self):
        return sum(y == 0 for x, y in self.chessBoard)

    def sum(self, type="all"):
        if type == "all":
            return sum(y for x, y in self.chessBoard) + self.zeros() - 9
        elif type == "top":
            return sum(y for x, y in self.top) + sum(y == 0 for x, y in self.top) - 3
        elif type == "bot":
            return sum(y for x, y in self.bot) + sum(y == 0 for x, y in self.bot) - 3
        elif type == "spr":
            return sum(y for x, y in self.spr) + sum(y == 0 for x, y in self.spr) - 3
