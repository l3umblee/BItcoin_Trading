import sys, os
sys.path.append(os.pardir)
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd
import time
import schedule

from datetime import datetime
from tc_lib.common import *
from tc_lib.BTCclass import *

model = None
ticker = "KRW-KNC"
if search_model() == False:
    os.system('train_model.py')

print("loading model...")
model = load_model('my_model.h5', compile=False)

trador = TradeAI(model)
tradingManager = TradingManager(ticker)

INTERVAL = 3

current_time = datetime.now()
if current_time.minute % 3 != 0:
    time_minute = (current_time.minute - current_time.minute % INTERVAL + INTERVAL)%60
    if time_minute == 60:
        tmp_time = current_time.replace(hour=(current_time.hour + 1), minute=0, second=0)
    else:
        tmp_time = current_time.replace(minute=time_minute, second=0)

    del_time = tmp_time - current_time
    sec = del_time.seconds
    print("Time Delay :", sec)
    time.sleep(sec)
else:
    print(current_time)

start_time = time.time()

schedule.every(30).seconds.do(trador.predict_data)

cnt = 0

tradingManager.show_balance()
while True:
    cnt += 1
    schedule.run_pending()
    time.sleep(1)

    if cnt == 180:
        tradingManager.show_balance()
        isOk = trador.judge_coin()

        if tradingManager.isAsk == False and isOk: #매수하지 않은 상황, 오를 것이라 판단
            tradingManager.buy_coin()
            print("<<buy coin>>")
        elif tradingManager.isAsk:
            tradingManager.sell_coin()
            print("<<sell coin>>")
            
        cnt = 0
        tradingManager.show_balance()
        print(tradingManager.isAsk)
        print(datetime.now())
        print("-"*30)

    stop_time = time.time() - start_time
    if stop_time >= 120*60:
        break

print("End Program")