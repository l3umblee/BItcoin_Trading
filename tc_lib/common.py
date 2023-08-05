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
    print("Get current data...")
    cur_time = datetime.now()
    
    params = {"ticker":"KRW-BTC", "interval":"minute3", "count":5, "to":cur_time}
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

    print(figs.shape)
    return figs

#get_KRW : 현재 잔고에 있는 원화를 조회 
def get_mybalance(access_key, secret_key, ticker='KRW'):
    upbit = pyupbit.Upbit(access_key, secret_key)
    print("현재",ticker, "조회: ",upbit.get_balance(ticker=ticker))
    
    return upbit.get_balance(ticker=ticker)

#buy_coin : 매수하는 함수 / 주문 취소 시 필요한 uuid와 수량 unit 반환
def buy_coin(access_key, secret_key):
    upbit = pyupbit.Upbit(access_key, secret_key)
    
    KRW = get_mybalance(access_key, secret_key, "KRW") #현재 KRW 원화 가져오기
    KRW = KRW*0.9995 #수수료 제외
    order_book = pyupbit.get_orderbook("KRW-BTC")
    bids_ask = order_book['orderbook_units']
    bid_ask = bids_ask[0]
    sell_price = bid_ask['bid_price']

    #매수 수량 = 현재 원화 잔고 / 매도 호가 (분할 매수에 관한 건은 나중에)
    unit = KRW/sell_price

    ret = upbit.buy_market_order("KRW-BTC", KRW, unit)
    print("KRW : ", KRW, ", unit : ", unit)
    print(upbit.get_order("KRW-BTC"))
    #uuid = ret['uuid']

    #return uuid, unit
    return unit

def sell_coin(access_key, secret_key, unit):
    upbit = pyupbit.Upbit(access_key, secret_key)
    cur_coins = get_mybalance(access_key, secret_key, "KRW-BTC") #현재 비트코인 잔고 확인
    if cur_coins <= 0:
        print("no coin to cell...")
        return
    
    ret = upbit.sell_market_order("KRW-BTC", cur_coins, unit)
    
    #uuid = ret['uuid']

    #return uuid, unit
    #return unit

def search_lowvalue():
    pass