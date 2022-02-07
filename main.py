# Author: Reginald McPherson
# Date modified: 7 Feb, 2022

# TO-DO: 
# - turn entire process into a self contained object so I can run multiple market simulations at a time with slightly input ranges (I couldn't do this with pine script, I had to test strategies one by one)
# - take a JSON file of candle history that I pull from tradingview and use for testing.
# - record to a JSON file OCHL values for various timeframes starting with (1hr, 4hr, daily, weekly, monthly)
# - better display of data
# - a way of displaying data from multiple instances (once I get multiple instances running)

import requests
import time
from candle import Candle
from position import Position

posSize         = 1
timeframe       = "1m"
maxPositions    = 3

profit          = 0
moneyLost       = 0
wins            = 0
losses          = 0
counter         = 0


bar = []
positionList    = []



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

    # adds candle information to an array to be accessed later.
    open = []
    close = []
    high = []
    low = []
    
    close.insert(0, Candle(timeframe).close)
    open.insert(0, Candle(timeframe).open)
    high.insert(0, Candle(timeframe).high)
    low.insert(0, Candle(timeframe).low)


    # display current close price
    print('=====================================================')
    print('Current Close: ' + str(close[0]))



    # Check if open positions is less than max positions. (Enables buying)
    if(openPositions() < maxPositions):

        # Buy immediately if there are 0 open positions (For testing purposes)
        if(openPositions() == 0):
            positionList.insert(0, Position(posSize, close[0], 0.001, 0.003))
            print('Added a position - ' + str(len(positionList)) + ' target: [' + str(positionList[0].exitPrice) + '] stop: [' + str(positionList[0].stopPrice) + ']')
        # Buy if close is lower than previous position entryPrice
        elif((close[0]) < ((positionList[0].entryPrice))):
            positionList.insert(0, Position(posSize, close[0], 0.001, 0.003))
            print('Added a position - ' + str(len(positionList)) + ' target: [' + str(positionList[0].exitPrice) + '] stop: [' + str(positionList[0].stopPrice) + ']')



    # Iterate through
    for pos in positionList:

        if(pos.positionIsOpen):

            # Target hit
            if (close[0] > pos.exitPrice):
                profit = profit + (close[0] - pos.exitPrice)
                wins = wins + 1
                pos.qty     = 0
                pos.positionIsOpen = False



            # Stoploss
            if (close[0] < pos.stopPrice):
                moneyLost = moneyLost - (close[0] - pos.exitPrice)
                losses = losses + 1
                pos.qty     = 0
                pos.positionIsOpen = False


    displayData()

    time.sleep(10)

