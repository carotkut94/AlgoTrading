import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas_datareader.data as web
import pandas as pd

style.use('ggplot')

start = dt.datetime(2000, 1, 1)
end = dt.datetime(2017, 11, 30)

# df = web.DataReader('TSLA', 'yahoo', start, end)
# print(df.head())
# df.to_csv('tsla.csv')

# and make date as the index
df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)
# print(df.head())
# df['Open'].plot()
# plt.show()
# 100 Moving Average, it is the average of today's price and past 99 days
df['100ma'] = df['Adj Close'].rolling(window=100).mean()
df.dropna(inplace=True)
# print(df.head())

# only for sampling using ohlc (open high low close)
df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

# print(df_ohlc)

df_ohlc.reset_index(inplace=True)

df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
print(df_ohlc.head())
# sampling ends here

ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)

# ax1.plot(df.index, df['Adj Close'])
# ax1.plot(df.index, df['100ma'])
# ax2.plot(df.index, df['Volume'])
# Pretty dope graph with multiple axes
# plt.show()

# Re-sampling of data using candle stick
ax1.xaxis_date()
candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

plt.show()



