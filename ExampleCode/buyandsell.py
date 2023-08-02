import pyupbit

access_key = "access key"
secret_key = "secret key"

upbit = pyupbit.Upbit(access_key, secret_key)

#매수 : 마켓명 / 주문가격 / 주문수량
ret = upbit.buy_limit_order("KRW-XRP", 100, 20)

#매도 : 마켓명 / 주문가격 / 주문수량
ret = upbit.sell_limit_order("KRW-XRP", 1000, 20)

#주문 취소 : uuid는 매수 시 ret 객체에 들어있는 값
ret = upbit.cancel_order('uuid')