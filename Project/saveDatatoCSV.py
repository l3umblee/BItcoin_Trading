import pyupbit
import datetime
from pandas import *

start_date = datetime.datetime(2023, 8, 1, 0, 0, 0, 0)
finish_date = datetime.datetime(2023, 7, 31, 0, 0, 0, 0)
tmp_date = start_date

INTERVAL_MINUTE = 10

df = DataFrame()

#params = {"ticker":"KRW-BTC", "interval":"minute10", "count":6, "to":"202307281800"}

while (tmp_date != finish_date):
    params = {"ticker":"KRW-BTC", "interval":"minute10", "count":20, "to":tmp_date}
    tmp_df = pyupbit.get_ohlcv(ticker=params['ticker'], interval=params['interval'], count=params['count'], to=params['to'])
    df = concat([df, tmp_df]) 
    tmp_date = tmp_date - datetime.timedelta(minutes=INTERVAL_MINUTE)

# params = {"ticker":"KRW-BTC", "interval":"minute10", "count":200, "to":tmp_date}
# df = pyupbit.get_ohlcv(ticker=params['ticker'], interval=params['interval'], count=params['count'], to=params['to'])

df.to_csv("dataset/bitcoindata.csv", index=True)
#index 삭제해줘야 함.