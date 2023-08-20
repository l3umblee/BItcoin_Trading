import sys, os
sys.path.append(os.pardir)
import pyupbit
import matplotlib.pyplot as plt
from tensorflow.python.keras.models import load_model
from tc_lib.common import *

#TradingAI : 매수/매도를 결정하는 CNN model 클래스
class TradeAI:
    def __init__(self, model, ticker):
        self.ticker = ticker
        self.model = model
        self.maj_data = list()

    #predict_data : 다음 봉이 오를지 판단
    def predict_data(self): 
        dimension = 48

        #x_input = get_cur_data(self.ticker, dimension)
        x_input = get_cur_data_vol(self.ticker, dimension)
        x_input = x_input.reshape(1, dimension, dimension, 3)

        y_input = self.model.predict(x_input)

        self.maj_data.append(y_input[0])

    #judge_coin : 코인의 매도, 매수를 결정
    def judge_coin(self):
        result = sum(self.maj_data)
        half = len(self.maj_data)/2
        print("half : ", half)
        self.maj_data.clear()

        print("result:", result)
        #todo : 다수결보다 1개 더 기준을 높임
        if result > half :
            return True
        else:
            return False

#TradingManager : 매도/매수/주문취소를 실행하는 클래스
class TradingManager:
    def __init__(self, ticker):
        self.access_key = ""
        self.secret_key = ""
        self.upbit = pyupbit.Upbit(self.access_key, self.secret_key)
        self.ticker=  ticker

        self.unit = 0.0
        self.uuid = ""
        self.sell_price = 0.0

        self.isAsk = False

    #get_mybalance : 원하는 종목의 잔고를 확인
    def get_mybalance(self, ticker="KRW"):
        balance = self.upbit.get_balance(ticker=ticker)

        return balance

    #buy_coin : 코인을 매수
    def buy_coin(self):
        KRW = self.get_mybalance("KRW")
        KRW = KRW * 0.9

        order_book = pyupbit.get_orderbook(self.ticker)
        bids_ask = order_book['orderbook_units']
        bid_ask = bids_ask[1] #한 단계 위의 매도 호가
        ask_price = bid_ask['ask_price'] #매도 호가
        
        self.sell_price = ask_price

        self.unit = KRW / self.sell_price

        ret = self.upbit.buy_limit_order(self.ticker, self.sell_price, self.unit)
        ret = self.upbit.get_order(self.ticker)

        if not ret: #체결 완료
            self.uuid = ""
        else: # 미체결
            self.uuid = ret[0]['uuid']

    #sell_coin : 코인을 매도 -> 시가에 매도
    def sell_coin(self):
        cur_coins = self.get_mybalance(self.ticker)
        if cur_coins <= 0:
            print("no coin to cell...")
            return

        order_book = pyupbit.get_orderbook(self.ticker)
        bids_ask = order_book['orderbook_units']
        bid_ask = bids_ask[1] #한 단계 아래의 매수 호가
        ask_price = bid_ask['bid_price'] #매수 호가

        self.sell_price = ask_price

        ret = self.upbit.sell_limit_order(self.ticker, self.sell_price,self.unit)
        print(ret)
        if not ret:
            self.uuid = "" 
        else:
            self.uuid = ret['uuid']

    #order_cancle : 주문 취소
    def order_cancle(self):
        ret = self.upbit.get_order(self.ticker) #미체결 주문
        self.uuid = ret[0]['uuid']

        self.upbit.cancel_order(self.uuid)

    #show_balance : 잔고 조회
    def show_balance(self):
        balances = self.upbit.get_balances()
        print(balances)
        if len(balances) != 1: #원화말고 다른 것도 있음
            for value in balances:
                if value['currency'] != 'KRW':
                    self.unit = value['balance']
                    self.sell_price = value['avg_buy_price']
                    self.isAsk = True
        else:
            self.isAsk = False