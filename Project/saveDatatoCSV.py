import pyupbit
import datetime
from pandas import *

start_date = datetime.datetime(2023, 8, 4, 0, 0, 0, 0)
finish_date = datetime.datetime(2023, 7, 30, 0, 0, 0, 0)
tmp_date = start_date

INTERVAL_MINUTE = 10

df = DataFrame()

while (tmp_date != finish_date):
    params = {"ticker":"KRW-BTC", "interval":"minute3", "count":6, "to":tmp_date}
    tmp_df = pyupbit.get_ohlcv(ticker=params['ticker'], interval=params['interval'], count=params['count'], to=params['to'])
    df = concat([df, tmp_df]) 
    tmp_date = tmp_date - datetime.timedelta(minutes=INTERVAL_MINUTE)

# params = {"ticker":"KRW-BTC", "interval":"minute10", "count":200, "to":tmp_date}
# df = pyupbit.get_ohlcv(ticker=params['ticker'], interval=params['interval'], count=params['count'], to=params['to'])

df.to_csv("dataset/bitcoindata.csv", header=None)