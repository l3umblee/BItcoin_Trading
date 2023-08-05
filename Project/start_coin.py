import sys, os
sys.path.append(os.pardir)
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd
import time
import schedule
from tc_lib.common import *
from tensorflow import keras
from tensorflow.python.keras.models import load_model

def predict_data(model):
    model = model
    dimension = 48

    x_input = get_cur_data(dimension)
    x_input = x_input.reshape(1, dimension, dimension, 3)

    y_input = model.predict(x_input)

    return y_input

start_time = time.time()

access_key = ""
secret_key = ""

#uuid = None
unit = 0.0

isAsk = False

#load model
if search_model() == False:
    os.system('train_model.py')

model = load_model('my_model.h5', compile=False)

print("Start time : ", datetime.now())
print(get_mybalance(access_key, secret_key))
print("-"*30)
while True:
    ans = predict_data(model)

    if isAsk: #이미 매수한 상황
        if (ans[0] == 0): #하락 예상
            #uuid, unit = sell_coin(access_key, secret_key)
            #unit = sell_coin(access_key, secret_key)
            sell_coin(access_key, secret_key, unit)
            print("<<sell coin>>")
            print("Current time : ", datetime.now())
            isAsk = False
        else: #매수한 코인이 더 오를 것으로 예상
            print("coin will be up...")

    else: #아직 매수하지 않은 상황
        if (ans[0] == 1):
            #uuid, unit = buy_coin(access_key, secret_key)
            unit = buy_coin(access_key, secret_key)

            print("<<buy coin>>")
            print("Current time : ", datetime.now())
            isAsk = True
    
    print(get_mybalance(access_key, secret_key))
    print("-"*30)

    time.sleep(60*3) #3분 단위로 검사

    stop_time = time.time() - start_time
    if stop_time >= 30*60: #30분 동안 투자
        sell_coin(access_key, secret_key, unit)
        break

print("End time : ", datetime.now())
print("End program")