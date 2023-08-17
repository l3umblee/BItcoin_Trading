import sys, os
sys.path.append(os.pardir)
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd
import time
import schedule
import pyautogui
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

INTERVAL = 10

time_delay(INTERVAL)

start_time = time.time()

schedule.every(30).seconds.do(trador.predict_data)
schedule.every(5).minutes.do(prevent_off)
schedule.every(10).minutes.do(trading, trador, tradingManager)

tradingManager.show_balance()
while True:
    schedule.run_pending()
    time.sleep(1)

    stop_time = time.time() - start_time
    if stop_time >= 180*60:
        break

print("End Program")