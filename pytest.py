import sys, os
sys.path.append(os.pardir)
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from tc_lib.common import *
from tc_lib.BTCclass import *

seq_len = 6
dimension = 48
my_dpi = 96
ticker = "KRW-KNC"
params = {"ticker":ticker, "interval":"minute10", "count":6, "to":datetime.now()}
gs = gridspec.GridSpec(nrows=2, ncols=1, height_ratios=[3, 1])
x = list(range(6))

df = pyupbit.get_ohlcv(ticker=params['ticker'], interval=params['interval'], count=params['count'], to=params['to'])
print
color_func = lambda x : '#77d879' if x >= 0 else '#db3f3f'
df['close'].diff().fillna(0)
print(df)
color_df = df['close'].diff().fillna(0).apply(color_func)
print(color_df)
color_list = list(color_df)

fig = plt.figure(figsize=(dimension/my_dpi, dimension/my_dpi), dpi=my_dpi)
ax0 = fig.add_subplot(gs[0])
candlestick2_ochl(ax0, df['open'], df['close'], df['high'],
                              df['low'], width=1,
                              colorup='#77d879', colordown='#db3f3f')
ax0.grid(False)
ax0.set_xticklabels([])
ax0.set_yticklabels([])
ax0.xaxis.set_visible(False)
ax0.yaxis.set_visible(False)
ax0.axis('off')

ax1 = fig.add_subplot(gs[1])
ax1.bar(x, df['volume'], color=color_list, width=1, align='center')
ax1.grid(False)
ax1.set_xticklabels([])
ax1.set_yticklabels([])
ax1.xaxis.set_visible(False)
ax1.yaxis.set_visible(False)
ax1.axis('off')

fig.canvas.draw()
plt.show()