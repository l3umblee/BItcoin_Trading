import pyupbit
import requests
from datetime import datetime
'''
10분 간격의 봉 데이터 3개를 받아올 수 있음
'''
INTERVAL_MINUTE = 10

cur_time = datetime.now()
input_time = cur_time.replace(minute=cur_time.minute - cur_time.minute % INTERVAL_MINUTE, second=0, microsecond=0)

params = {"ticker":"KRW-BTC", "interval":"minute10", "count":5, "to":input_time}
candles = pyupbit.get_ohlcv(ticker=params['ticker'], interval=params['interval'], count=params['count'], to=input_time)
print(candles.columns)
print(candles)