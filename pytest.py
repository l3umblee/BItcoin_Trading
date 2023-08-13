import sys, os
sys.path.append(os.pardir)
import matplotlib.pyplot as plt
import time
import schedule
from tc_lib.common import *
from tc_lib.BTCclass import *
import tensorflow as tf
print(tf.__version__)