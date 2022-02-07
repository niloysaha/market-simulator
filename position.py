
class Position:
    def __init__(self, qty, entryPrice):
        self.entryPrice = entryPrice
        self.exitPrice = self.entryPrice + 20
        self.stopPrice = self.entryPrice - 100
        self.qty    = qty
        self.positionIsOpen   = True


    