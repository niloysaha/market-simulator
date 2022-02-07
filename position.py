
class Position:
    def __init__(self, qty, entryPrice):
        self.entryPrice = entryPrice
        self.exitPrice = self.entryPrice + 1
        self.stopPrice = self.entryPrice - 3
        self.qty    = qty


    