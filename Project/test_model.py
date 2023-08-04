import sys, os
sys.path.append(os.pardir)
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd
import time
import schedule
from tc_lib.common import *
from tensorflow import keras
from tensorflow.python.keras.models import load_model

def predict_data():
    if search_model() == False:
        os.system('train_model.py')

    model = load_model('my_model.h5', compile=False)
    dimension = 48

    x_input = get_cur_data(dimension)
    x_input = x_input.reshape(1, dimension, dimension, 3)

    y_input = model.predict(x_input)

    return y_input

print(predict_data())