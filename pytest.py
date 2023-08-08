import sys, os
sys.path.append(os.pardir)
import matplotlib.pyplot as plt
import time
import schedule
from tc_lib.common import *

access_key = ""
secret_key = ""

upbit = pyupbit.Upbit(access_key, secret_key)
ret = upbit.get_order("KRW-IQ")
print(ret)
if ret == []:
    print("jere")
else:
    uuid = ret[0]['uuid']
    upbit.cancel_order(uuid)
    price = ret[0]['price']
print(price)