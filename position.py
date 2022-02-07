# Author: Reginald McPherson
# Date modified: 7 Feb, 2022

# TO-DO: 


class Position:
    
    def __init__(self, qty, entryPrice, target, stop):
        self.positionIsOpen   = True
        self.entryPrice = entryPrice
        self.exitPrice = self.entryPrice * (1 + target)
        self.stopPrice = self.entryPrice * (1 - stop)
        self.qty    = qty
        self.value  = self.entryPrice * qty