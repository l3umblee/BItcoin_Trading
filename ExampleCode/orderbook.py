import pyupbit

orderbook = pyupbit.get_orderbook("KRW-BTC")
print(type(orderbook))
bids_asks = orderbook['orderbook_units']

#ask_price : 매도 호가, bid_price : 매수 호가, ask_size : 매도 호가 수량, bid_size : 매수 호가 수량
for bid_ask in bids_asks:
    print(bid_ask)