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
cur_balance = get_mybalance(access_key, secret_key, "KRW")
D = get_coinbalance(access_key, secret_key, "IQ")
print(D[0]["IQ"])
print(cur_balance)