# Market-simulator
A market simulator using real price information from the bitfinex rest end point so I can build and test and automate my trading strategies without relying on paid charting software like tradingview.

## Why not use the official libraries?
Bitfinex does have a python library already, and I'll eventually use it but this is a project I've wanted to do for a long time do I'm going to see what I can produce on my own as much as possible before using their library so I can see what problems I run into first.

## Future plans
NodeJS - Instead of running off my PC in a terminal window I'll have this running on NodeJS somewhere

# TO-DO: 
- turn entire process into a self contained object so I can run multiple market simulations at a time with slightly input ranges (I couldn't do this with pine script, I had to test strategies one by one)
- take a JSON file of candle history that I pull from tradingview and use for testing.
- record to a JSON file OCHL values for various timeframes starting with (1hr, 4hr, daily, weekly, monthly)
- better display of data
- a way of displaying data from multiple instances (once I get multiple instances running)

## Contributing
I wasn't planning on opening this project up for contributions because it's a bit of a learning project for me and I'm having a lot of fun, but I suppose I'll open it up to the public.

## How to use
Right now just run the `main.py` to start and a simple text output will show you how things are going.

## Basic settings 
**Position size**
File:     `main.py`
Variable: `posSize`
Value:    `1`

**Position target**
File:     `position.py`
Variable: `exitPrice`
Value:    `entryPrice + 20`

**Position stopLoss**
File:     `position.py`
Variable: `stopPrice`
Value:    `entryPrice - 100`
