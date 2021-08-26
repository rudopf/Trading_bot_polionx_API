Poloniex-trading-bot
A trading bot that utilises MACD to track and make trades of crytocurrency. Used on Python 3.6 It works off a Poloniex API wrapper by s4w3d0ff for which the link can be found here https://github.com/s4w3d0ff/python-poloniex. You will need to install the above API wrapper for this bot to work. Additionally, a python package named Pandas needs to be installed as well. https://pandas.pydata.org/pandas-docs/stable/install.html

How the bot works: Given a coin pair traded on Poloniex, the largest value of MACD from the past 4 days is found. Every 30 mins, the current MACD is evaluated. If it is at least 80% of the largest MACD, the coin is traded. If current MACD is positive, the market is evaluated as overbought and is sold. If it is negative, market is evaulated as oversold and it is bought.

Note: There is no promise of returns on this bot. Use at your own risk. That said, if you have any suggestions to improve on the bot, please leave a comment.
