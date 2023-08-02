import pyupbit
from datetime import datetime
import pandas_datareader.data as web
import mplfinance as mpf
import matplotlib.pyplot as plt

INTERVAL_MINUTE = 10

cur_time = datetime.now()
input_time = cur_time.replace(minute=cur_time.minute - cur_time.minute % INTERVAL_MINUTE, second=0, microsecond=0)

params = {"ticker":"KRW-BTC", "interval":"minute10", "count":5, "to":input_time}
candles = pyupbit.get_ohlcv(ticker=params['ticker'], interval=params['interval'], count=params['count'], to=input_time)
#candles에는 dataframe 객체로 들어 있음
print(candles)

mpf.plot(candles, type="candle", mav=(), volume=False, style="yahoo")
plt.show()