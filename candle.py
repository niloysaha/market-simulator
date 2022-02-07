import requests

class Candle:

    def __init__(self, timeframe):
        self.timeframe = timeframe
        candle = requests.get('https://api-pub.bitfinex.com/v2/candles/trade:'+self.timeframe+':tBTCUSD/last').json()
        self.open = candle[1]
        self.close = candle[2]
        self.high = candle[3]
        self.low = candle[4]
