import sys, os
sys.path.append(os.pardir)
import pyupbit
import datetime
import csv
import time
import pandas as pd
from pandas import *

start_date = datetime.datetime(2023, 7, 12, 0, 0, 0, 0)
finish_date = datetime.datetime(2023, 8, 12, 0, 0, 0, 0)
tmp_date = start_date

INTERVAL_MINUTE = 18

file_path = "dataset/bitcoindata.csv"
csv_file = open(file_path, mode='a', newline='')
csv_writer = csv.writer(csv_file)

while tmp_date != finish_date:
    params = {"ticker":"KRW-IQ", "interval":"minute3", "count":6, "to":tmp_date}
    tmp_df = pyupbit.get_ohlcv(ticker=params['ticker'], interval=params['interval'], count=params['count'], to=params['to'])
    time.sleep(0.1)
    tmp_df.to_csv(csv_file, header=None)

    tmp_date = tmp_date + datetime.timedelta(minutes=INTERVAL_MINUTE)

csv_file.close()