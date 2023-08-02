import sys, os
sys.path.append(os.pardir)
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd
from tc_lib.common import *

inputs = "dataset/bitcoindata.csv"
#saveDatatoCSV에서 data를 받아올 때 사용한 params 중 count와 같은 값이어야 함.
seq_len = 20
dimension = 48

figures, labels = get_coindata(inputs, seq_len, dimension)

figures = figures/255.0
print(np.shape(labels), np.shape(figures))