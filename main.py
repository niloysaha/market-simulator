import requests
import time
from candle import Candle
from position import Position


timeframe = "1m"
maxPositions = 3
positionList = []
profit  = 0
moneyLost = 0
wins    = 0
losses  = 0
counter = 0
lastClose = Candle('15m').close
bar = []
print('Last 15m close:' + str(lastClose))



def getClose():
    return Candle('1m').close


def openPositions():
    openPos = 0

    for pos in positionList:
        if (pos.positionIsOpen):
            openPos = openPos + 1

    return openPos


def displayData():
    print("---------------------------------------------")
    print('Total Profit: '      + str(profit))
    print('Total Money Lost: '  + str(moneyLost))
    print('Positions total: '   + str(len(positionList)))
    print('Open Positions: '    + str(len(positionList) - (wins + losses)))
    print('Wins: '              + str(wins))
    print('Losses: '            + str(losses))


while(getClose() < 45000):

    counter = counter + 1

    # adds candle information to an array to be accessed later.
    bar.insert(0, Candle(timeframe))

    close = bar[0]


    # display current close price
    print('=====================================================')
    print('Current Close: ' + str(close))



    # Check if open positions is less than max positions. (Enables buying)
    if(openPositions() < maxPositions):

        # Buy immediately if there are 0 open positions (For testing purposes)
        if(openPositions() == 0):
            positionList.insert(0, Position(1, close))
            print('Added a position - ' + str(len(positionList)) + ' target: [' + str(positionList[0].exitPrice) + '] stop: [' + str(positionList[0].stopPrice) + ']')


        # Buy if current close price drops below the previous buy's entry price (For testing purposes)
        if(close < positionList[-1].entryPrice):
            positionList.insert(0, Position(1, close))
            print('Added a position - ' + str(len(positionList)) + ' target: [' + str(positionList[0].exitPrice) + '] stop: [' + str(positionList[0].stopPrice) + ']')



    # Iterate through
    for pos in positionList:

        if(pos.positionIsOpen):

            # Target hit
            if (close > pos.exitPrice):
                profit = profit + (close - pos.exitPrice)
                wins = wins + 1
                pos.qty     = 0
                lastClose   = close
                pos.positionIsOpen = False



            # Stoploss
            if (close < pos.stopPrice):
                moneyLost = moneyLost - (close - pos.exitPrice)
                losses = losses + 1
                pos.qty     = 0
                lastClose   = close
                pos.positionIsOpen = False


    displayData()

    time.sleep(3)

