import pyupbit
import datetime
from pandas import *

start_date = datetime.datetime(2023, 8, 5, 0, 0, 0, 0)
finish_date = datetime.datetime(2023, 7, 5, 0, 0, 0, 0)
tmp_date = start_date

#3분봉을 6개씩 받아옴 / 다음의 데이터는 18분 뒤의 데이터를 받아와야 함.
INTERVAL_MINUTE = 18

df = DataFrame()

while (tmp_date != finish_date):
    params = {"ticker":"KRW-IQ", "interval":"minute3", "count":6, "to":tmp_date}
    tmp_df = pyupbit.get_ohlcv(ticker=params['ticker'], interval=params['interval'], count=params['count'], to=params['to'])
    df = concat([tmp_df, df]) 
    tmp_date = tmp_date - datetime.timedelta(minutes=INTERVAL_MINUTE)

# params = {"ticker":"KRW-BTC", "interval":"minute10", "count":200, "to":tmp_date}
# df = pyupbit.get_ohlcv(ticker=params['ticker'], interval=params['interval'], count=params['count'], to=params['to'])

df.to_csv("dataset/bitcoindata.csv", header=None)