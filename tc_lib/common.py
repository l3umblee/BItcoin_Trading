import sys, os
sys.path.append(os.pardir)
import numpy as np
from mplfinance.original_flavor import candlestick2_ochl
import matplotlib.pyplot as plt
import pandas as pd

def get_coindata(fname, seq_len, dimension):
    df = pd.read_csv(fname, names=['time','open', 'high', 'low', 'close','volume', 'value'])
    df.fillna(0)

    plt.style.use('dark_background')
    df.reset_index(inplace=True)

    my_dpi = 96
    figs = np.zeros((len(df) - 1, dimension, dimension, 3))
    fig_final = plt.figure(figsize=(dimension / my_dpi,
                                      dimension / my_dpi), dpi=my_dpi)
    labels = []
    for i in range(0, len(df)-1):
        c = df.iloc[i:i + int(seq_len), :]
        c_ = df.iloc[i:i + int(seq_len) + 1, :]
        if len(c) == int(seq_len):
            ax1 = fig_final.add_subplot(1, 1, 1)
            candlestick2_ochl(ax1, c['open'], c['close'], c['high'],
                              c['low'], width=1,
                              colorup='#77d879', colordown='#db3f3f')
            
            ax1.grid(False)
            ax1.set_xticklabels([])
            ax1.set_yticklabels([])
            ax1.xaxis.set_visible(False)
            ax1.yaxis.set_visible(False)
            ax1.axis('off')
        
        #정답레이블 다는 곳 - starting은 endvalue 보다 하루 이전의 종가
        starting = c_["close"].iloc[-2]
        endvalue = c_["close"].iloc[-1]
        if endvalue > starting :
            label = 1 #label1은 결국 오른 것
        else :
            label = 0 #그렇지 않은 것
        labels.append(label)

        fig_final.canvas.draw()
        fig_np = np.array(fig_final.canvas.renderer._renderer) #canvas에 그린 것을 np array로 변환(im2col과 같은 동작)
        
        print(i)
        figs[i] = fig_np[:,:,:3]

        plt.close(fig_final)

    return figs, labels