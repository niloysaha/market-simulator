# Market-simulator
A market simulator using real price information from the bitfinex rest end point so I can build and test and automate my trading strategies without relying on paid charting software like tradingview.

## Why not use the official libraries?
Bitfinex does have a python library already, and I'll eventually use it but this is a project I've wanted to do for a long time do I'm going to see what I can produce on my own as much as possible before using their library so I can see what problems I run into first.

## Future plans
NodeJS - Instead of running off my PC in a terminal window I'll have this running on NodeJS somewhere

Bring over Icarus and other indicators from tradingview to work natively with my application
![image](https://user-images.githubusercontent.com/71242881/152858151-fbf7da9d-fa9e-4e91-83a5-d0fee8d71855.png)


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
