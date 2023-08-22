import sys, os
sys.path.append(os.pardir)
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import requests
from tc_lib.common import *
from tc_lib.BTCclass import *

cur_time = datetime.now()
params = {"ticker":"KRW-BTC", "interval":"minute1", "count":5, "to":cur_time}
candles = pyupbit.get_ohlcv(ticker=params['ticker'], interval=params['interval'], count=params['count'], to=cur_time)
print(candles)
print(candles.iloc[-1, 4])            
print(max(candles['volume']))