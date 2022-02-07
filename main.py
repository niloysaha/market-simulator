import requests
import time
from candle import Candle
from position import Position

maxPositions = 3
positionList = []
profit  = 0
moneyLost = 0
wins    = 0
losses  = 0
counter = 0
lastClose = Candle('15m').close
print('Last 15m close:' + str(lastClose))


# In Pinescript, previous values are accessed via an array and I want to emulate that as much as possible here because all of my own algorithms
# for trading signals were created parsing arrays like this.
open = []
close = []
high = []
low = []


def getClose():
    return Candle('1m').close

#Refactored totalQty
def openPositions():
    openPos = 0

    for pos in positionList:
        if (pos.positionIsOpen):
            openPos = openPos + 1

    return openPos


def displayData():
    print("---------------------------------------------")
    print('Total Profit: '      + str(profit))
    print('Total Money Lost: ' + str(moneyLost))
    print('Positions total: '   + str(len(positionList)))
    print('Open Positions: '    + str(len(positionList) - (wins + losses)))
    print('Wins: '              + str(wins))
    print('Losses: '            + str(losses))


while(getClose() < 45000):

    counter = counter + 1

    # display current close price
    print('=====================================================')
    print('Current Close: ' + str(getClose()))

    # adds close information to an array to be accessed later.
    close.insert(0, getClose())


    # check total qty of shares from all positions
    openPositions()

    # if total qty is less than max positions, trade (only valid while 1 qty per position is used)
    if(openPositions() < maxPositions):

        # Buy: held qty = 0
        if(openPositions() == 0):
            positionList.append(Position(1, getClose()))
            print('Added a position - ' + str(len(positionList)) + ' target: [' + str(positionList[-1].exitPrice) + '] stop: [' + str(positionList[-1].stopPrice) + ']')


        # Buy: additional 1
        if((getClose()) < ((positionList[-1].entryPrice))):
            positionList.append(Position(1, getClose()))
            print('Added a position - ' + str(len(positionList)) + ' target: [' + str(positionList[-1].exitPrice) + '] stop: [' + str(positionList[-1].stopPrice) + ']')



    # Sell if price closes above an exitPrice
    for pos in positionList:

        c = getClose()

        # Target hit
        if ((c > pos.exitPrice) & (pos.positionIsOpen == True)):
            profit = profit + (c - pos.exitPrice)
            wins = wins + 1
            pos.qty     = 0
            lastClose   = c
            pos.positionIsOpen = False



        # Stoploss
        if ((c < pos.stopPrice) & (pos.positionIsOpen == True)):
            moneyLost = moneyLost - (c - pos.exitPrice)
            losses = losses + 1
            pos.qty     = 0
            lastClose   = c
            pos.positionIsOpen = False
        

    displayData()

    time.sleep(3)

