import sys, os
sys.path.append(os.pardir)
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd
from tc_lib.common import *
from tensorflow import keras

inputs = "dataset/bitcoindata.csv"
#saveDatatoCSV에서 data를 받아올 때 사용한 params 중 count와 같은 값이어야 함.
seq_len = 6
dimension = 48

figures, labels = get_coindata(inputs, seq_len, dimension)

figures = figures/255.0
print(np.shape(labels), np.shape(figures))

#논문 구현 [Using Deep Learning Neural Networks and Candlestick Chart Representation to Predict Stock Market]
model = keras.Sequential()
model.add(keras.layers.Conv2D(32, kernel_size=3, activation='relu', padding='same'))
model.add(keras.layers.MaxPooling2D(2))
model.add(keras.layers.Conv2D(48, kernel_size=3, activation='relu', padding='same'))
model.add(keras.layers.MaxPooling2D(2))
model.add(keras.layers.Dropout(0.5))

model.add(keras.layers.Conv2D(64, kernel_size=3, activation='relu', padding='same'))
model.add(keras.layers.MaxPooling2D(2))
model.add(keras.layers.Conv2D(96, kernel_size=3, activation='relu', padding='same'))
model.add(keras.layers.MaxPooling2D(2))
model.add(keras.layers.Dropout(0.5))

model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(256, activation='relu'))
model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Dense(1, activation='sigmoid')) #이진분류

train_len = int(len(figures)*0.7)
batch_size = 16

num_iters=  train_len // batch_size
num_epochs = 100

x_train, y_train = shuffle_dataset(figures[:train_len],labels[:train_len], train_len, dimension)
x_test, y_test = shuffle_dataset(figures[train_len:], labels[train_len:], len(labels) - train_len, dimension)

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(x_train, y_train, batch_size=batch_size, epochs=num_epochs)

model.save('my_model.h5', overwrite=True)

predicted = model.predict(x_test)

print(predicted)