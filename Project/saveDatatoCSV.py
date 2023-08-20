import sys, os
sys.path.append(os.pardir)
import pyupbit
import datetime
import csv
import time
import pandas as pd
from pandas import *

start_date = datetime.datetime(2023, 5, 17, 0, 0, 0, 0)
finish_date = datetime.datetime(2023, 8, 17, 0, 0, 0, 0)
tmp_date = start_date

INTERVAL_HOUR = 1

ticker = "KRW-HIFI"
file_path = "dataset/bitcoindata.csv"
file_name = "bitcoindata.csv"

files = os.listdir('dataset')
if file_name in files:
    os.remove(file_path)

csv_file = open(file_path, mode='a', newline='')
csv_writer = csv.writer(csv_file)

while tmp_date != finish_date:
    params = {"ticker":ticker, "interval":"minute10", "count":6, "to":tmp_date}
    tmp_df = pyupbit.get_ohlcv(ticker=params['ticker'], interval=params['interval'], count=params['count'], to=params['to'])
    time.sleep(0.1)
    tmp_df.to_csv(csv_file, header=None)

    tmp_date = tmp_date + datetime.timedelta(hours=INTERVAL_HOUR)

csv_file.close()