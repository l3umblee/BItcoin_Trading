import sys, os
sys.path.append(os.pardir)
import matplotlib.pyplot as plt
import time
import schedule
from tc_lib.common import *
from tc_lib.BTCclass import *
import tensorflow as tf

def test(a, b):
    x = a
    y = b
    print(x+y)

schedule.every(5).seconds.do(test, 2, 3)
while True:  
    schedule.run_pending()