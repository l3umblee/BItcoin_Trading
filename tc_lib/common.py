import sys, os
sys.path.append(os.pardir)
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pyupbit

from tqdm import tqdm
from mplfinance.original_flavor import candlestick2_ochl
from datetime import datetime

#get_coindata : fname으로 받은 곳의 데이터를 가져와 그래프로 나타내는 함수, 정확히는 im2col의 역할을 함.
'''
c는 seq_len보다 1 작은 그래프 / c_는 seq_len 만큼의 그래프
c_의 마지막의 데이터(-1)는 c에 없고, c_의 마지막에서 2번째 데이터(-2)는 c의 마지막 데이터
c_의 -1번째 인덱스 값이 -2번째 인덱스 값보다 크다면, c의 그래프는 오를 그래프였던 것 -> 라벨 1
'''
def get_coindata(fname, seq_len, dimension):
    print("Get coin data...")
    df = pd.read_csv(fname, names=['time','open', 'high', 'low', 'close','volume', 'value'])
    df.fillna(0)

    plt.style.use('dark_background')
    df.reset_index(inplace=True)
    
    figs = np.zeros((len(df) - 1, dimension, dimension, 3))        
    labels = []
    for i in tqdm(range(0, len(df)-1)):
        c = df.iloc[i:i + int(seq_len) - 1, :]
        c_ = df.iloc[i:i + int(seq_len), :]
        if len(c) == int(seq_len) - 1:
            my_dpi = 96
            fig_final = plt.figure(figsize=(dimension / my_dpi,
                                            dimension / my_dpi), dpi=my_dpi)
    
            ax1 = fig_final.add_subplot(1, 1, 1)
            candlestick2_ochl(ax1, c['open'], c['close'], c['high'],
                              c['low'], width=1,
                              colorup='#77d879', colordown='#db3f3f')
            
            ax1.grid(False)
            ax1.set_xticklabels([])
            ax1.set_yticklabels([])
            ax1.xaxis.set_visible(False)
            ax1.yaxis.set_visible(False)
            ax1.axis('off')
        
        #정답레이블 다는 곳 - starting은 endvalue 보다 10분 이전의 종가
        starting = c_["close"].iloc[-2]
        endvalue = c_["close"].iloc[-1]
        if endvalue > starting :
            label = 1 #label = 1은 결국 오른 것
        else :
            label = 0 #그렇지 않은 것
        labels.append(label)

        fig_final.canvas.draw()
        fig_np = np.array(fig_final.canvas.renderer._renderer) #canvas에 그린 것을 np array로 변환(im2col과 같은 동작)
        figs[i] = fig_np[:,:,:3]

        plt.close(fig_final)
        
    print("Completed!")
    return figs, labels

#shuffle_dataset : input_data를 섞어서 반환
def shuffle_dataset(input_data, labels, num, dimension):
    x_train = np.zeros(shape=(num, dimension, dimension, 3))
    y_train = np.zeros(shape=(num, ))    
    
    for i in range(num):
        idx = np.random.randint(len(labels))
        x_train[i] = input_data[idx]
        y_train[i] = labels[idx]
    
    return x_train, y_train

#search_model : 기존에 생성한 모델이 있는지 확인
def search_model():
    files = os.listdir()
    for file in files:
        if file == 'my_model.h5':
            print("model already exist...")
            return True
    
    return False

#get_cur_data : 현재의 코인 데이터를 image로 가져와 predict에 넣는 용도
def get_cur_data(dimension=48):
    #print("Get current data...")
    cur_time = datetime.now()
    
    params = {"ticker":"KRW-IQ", "interval":"minute3", "count":5, "to":cur_time}
    candles = pyupbit.get_ohlcv(ticker=params['ticker'], interval=params['interval'], count=params['count'], to=cur_time)

    plt.style.use("dark_background")

    figs = np.zeros((1, dimension, dimension, 3))
    my_dpi = 96
    fig_final = plt.figure(figsize=(dimension / my_dpi,
                                    dimension / my_dpi), dpi=my_dpi)
    
    ax1 = fig_final.add_subplot(1, 1, 1)
    candlestick2_ochl(ax1, candles['open'], candles['close'], candles['high'],
                        candles['low'], width=1,
                        colorup='#77d879', colordown='#db3f3f')
            
    ax1.grid(False)
    ax1.set_xticklabels([])
    ax1.set_yticklabels([])
    ax1.xaxis.set_visible(False)
    ax1.yaxis.set_visible(False)
    ax1.axis('off')

    fig_final.canvas.draw()
    fig_np = np.array(fig_final.canvas.renderer._renderer)

    figs = fig_np[:,:,:3]
    plt.close(fig_final)

    return figs

#time_delay

#get_candle_cur : 시가, 종가, 저가, 고가, 현재가를 받아올 수 있음 / 현재가를 제외한 나머지는 candle에 담겨있음
def get_candle_cur():
    cur_time = datetime.now()
    params = {"ticker":"KRW-IQ", "interval":"minute3", "count":1, "to":cur_time}
    candle = pyupbit.get_ohlcv(ticker=params['ticker'], interval=params['interval'], count=params['count'], to=cur_time)
    cur_price = pyupbit.get_current_price("KRW-IQ")
    return candle, cur_price

#get_coinbalance : 보유한 코인의 가격
def get_coinbalance(access_key, secret_key):
    upbit = pyupbit.Upbit(access_key, secret_key)
    my_balances = upbit.get_balances()
    print(len(my_balances))
    price = my_balances[1]["avg_buy_price"]

    return price