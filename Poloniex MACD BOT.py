import pandas as pd
import datetime
import time as time
import poloniex as polo
import numpy as np
import calendar

#account info
#insert api key and secret from poloniex account below. e.g. api_key = '1234567890'
api_key = ''
secret = ''
acct = polo.Poloniex(api_key,secret)

#acquire unix timestamp, define number of days to traceback here as timedelta
timeframe = datetime.date.today() - datetime.timedelta(26)
timeframeunix = calendar.timegm(timeframe.timetuple())

#define exponential moving average
def ema(df, window, targetcol='close', colname = 'ema', **kwargs):
    df[colname]=df[targetcol].ewm(span=window,min_periods=0,adjust=True,ignore_na=False).mean()
    return df[colname]

#function
#indicator is value of macd at which decision to trade is made
#timeframeunix refers to how many days of past data is being examined
#buy_amount is number of coins to buy in a 'buy' action
#sell_amount same as buy_amount
def trade(currency = None, timeframe = timeframeunix, buy_amount=100, sell_amount=100):
    raw_crypto = acct.returnChartData(currency, period = 1800, start = timeframe)
    crypto = pd.DataFrame(raw_crypto)
    #adjust datetime format
    crypto['date'] = pd.to_datetime(crypto['date'], unit = 's')
    crypto.set_index('date', inplace = True)


    #set long, short ema and macd
    crypto['fast_ema'] = ema(df = crypto, window = 12, colname= 'fast_ema')
    crypto['slow_ema'] = ema(df = crypto, window = 26, colname= 'slow_ema')
    crypto['macd'] = crypto['fast_ema']-crypto['slow_ema']

    #set buy, sell signals
    def get_indicator(row):
        macd = float(row['macd'])
        indicator_window = crypto['macd'].tail(192)
        indicator = abs(indicator_window).max() * 0.7
        if macd > indicator:
            return -1.0
            print('sold')
        elif macd < -indicator:
            return 1.0
            print('bought')
        else:
            return 0.0
            print('no action taken')
    crypto['positions'] = crypto.apply(get_indicator, axis = 1)
        
    current_signal = crypto['positions'].iloc[-1] 
    print(current_signal)
    if current_signal == 1.0:
        try:
            acct.buy(currencyPair = currency, rate=float(crypto['open'].iloc[-1]), amount=buy_amount, orderType= 'immediateOrCancel')
            print('bought ' + str(currency) + ' at ' + str(datetime.datetime.now()))
        except:
            print('Error! Probably not enough BTC')
 
    elif current_signal == -1.0:
        try:
            acct.sell(currencyPair= currency, rate = float(crypto['close'].iloc[-1]) , amount = sell_amount , orderType='immediateOrCancel')
            print('sold ' + str(currency) + ' at ' + str(datetime.datetime.now()))
        except:
            print('Error! Probably not enough crypto')
            
    elif current_signal == 0.0:
        print('no action taken for ' + str(currency) + ' at ' + str(datetime.datetime.now()))           
       
while True:
    #add currency pair, buy and sell amount below! e.g.
    '''
    trade(currency='BTC_XMR', buy_amount=0.02, sell_amount=0.02)
    trade(currency='BTC_ETH', buy_amount=0.03, sell_amount=0.03)
    '''
    time.sleep(1800)
