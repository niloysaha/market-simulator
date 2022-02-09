# Author: Reginald McPherson
# Date modified: 9 Feb, 2022

# TO-DO: 
# - turn entire process into a self contained object so I can run multiple market simulations at a time with slightly input ranges (I couldn't do this with pine script, I had to test strategies one by one)
# - take a JSON file of candle history that I pull from tradingview and use for testing.
# - record to a JSON file OCHL values for various timeframes starting with (1hr, 4hr, daily, weekly, monthly)
# - better display of data
# - a way of displaying data from multiple instances (once I get multiple instances running)

from numpy import average
import pandas as pd
import numpy as np
import requests
import time
from candle import Candle
from position import Position


# TO-DO:


# Variables
#---------------------------
capital         = 200.00
posSize         = 200
timeframe       = "5m"
maxPositions    = 10

profit          = 0
moneyLost       = 0
wins            = 0
losses          = 0




# Lists
#---------------------------
positionList    = []
open = []
close = []
high = []
low = []



# Functions
#---------------------------
def getClose(timeframe):
    return Candle(timeframe).close



def openPositions():
    openPos = 0

    for pos in positionList:
        if (pos.positionIsOpen):
            openPos = openPos + 1

    return openPos


def displayData(close):
    print("---------------------------------------------")
    print('Close: [' + str(Candle(timeframe).close) + ']',
          'Wins: ['     + str(wins)       + ']',
          'Profit: ['   + str("{:.2f}".format(profit))     + ']',
          'Losses: ['   + str("{:.2f}".format(losses))     + ']',
          'Loss: ['     + str("{:.2f}".format(moneyLost))  + ']',
          'Open Pos: [' + str(len(positionList) - (wins + losses)) + ']',
          'Total Pos: ['+ str(len(positionList)) + ']')



def getHistory(length):
    openHistory = []
    closeHistory = []
    highHistory = []
    lowHistory = []
    volumeHistory = []

    # Pulls the last 100 candles
    hist = requests.get('https://api-pub.bitfinex.com/v2/candles/trade:'+timeframe+':tXRPUSD/hist').json()

    for i in range(length):
        openHistory.append(hist[i][1])
        closeHistory.append(hist[i][2])
        highHistory.append(hist[i][3])
        lowHistory.append(hist[i][4])
        volumeHistory.append(hist[i][5])

    return openHistory, closeHistory, highHistory, lowHistory, volumeHistory

# Add data to history
open, close, high, low, volume = getHistory(100)





#==========================================================================
# Simple Moving Average - length is the number of bars back to calculate
#==========================================================================
def sma(length):
    total = 0

    for i in range(length):
        total = total + close[i]

    return total/length


def ExpMovingAverage(values, window):
    """ Numpy implementation of EMA
    """
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a =  np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a




#===========================================================================================================================================
# MAIN LOOP
# Conditional for while loop will eventually change to something more goal oriented
# For now it's set for testing by looping while closing price stays below some arbitrary number.
#===========================================================================================================================================
while(getClose(timeframe) < 60000):

    #=================================================================
    # Moving Averages
    #=================================================================
    # print(ExpMovingAverage(close, 14))
    print('SMA-10: '  + str("{:.4f}".format(sma(10))))
    print('SMA-20: '  + str("{:.4f}".format(sma(20))))
    print('SMA-50: '  + str("{:.4f}".format(sma(50))))
    print('SMA-100: ' + str("{:.4f}".format(sma(100))))



#==========================================================================
# Buy/Add to position
#==========================================================================

    # Check if open positions is less than max positions. (Enables buying)
    if(openPositions() < maxPositions):

        # Buy immediately if there are 0 open positions (For testing purposes)
        if((openPositions() == 0) & (close[0] < sma(50))):
            positionList.insert(0, Position(posSize, close[0], 0.005, 0.03))
            print('Added a position - ' + str(len(positionList)) + ' target: [' + str("{:.4f}".format(positionList[0].exitPrice)) + '] stop: [' + str("{:.4f}".format(positionList[0].stopPrice)) + ']')

        # Buy if close is lower than previous position entryPrice
        elif((close[0] < sma(100))):
            positionList.insert(0, Position(posSize, close[0], 0.005, 0.03))
            print('Added a position - ' + str(len(positionList)) + ' target: [' + str("{:.4f}".format(positionList[0].exitPrice)) + '] stop: [' + str("{:.4f}".format(positionList[0].stopPrice)) + ']')


#==========================================================================
# Sell/Stop out of position
#==========================================================================

    # Iterate through positions and find open positions
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

    # Basic data and state information
    displayData("{:.4f}".format(close[0]))

    time.sleep(300)

