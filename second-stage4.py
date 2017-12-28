# S&P 500 companies
import bs4 as bs
import pickle
import requests
import datetime as dt
import os
import numpy as np
import pandas_datareader as web
import pandas as pd
from matplotlib import  style
import matplotlib.pyplot as plt
from pandas.io.sas.sas_constants import column_name_text_subheader_length

style.use('ggplot')

def save_sp500_tickers():
    response = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(response.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    with open('sp500tickers.pickle', 'wb') as f:
        pickle.dump(tickers, f)

    print(tickers)
    return tickers


# Helper method to get all ticker's data from yahoo
def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open('sp500tickers.pickle', 'rb') as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2000, 1, 1)
    end = dt.datetime(2017, 11, 30)

    for ticker in tickers:
        print(ticker)
        try:
            if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
                df = web.DataReader(ticker, 'yahoo', start, end)
                df.to_csv('stock_dfs/{}.csv'.format(ticker))
            else:
                print('Already have the file for {}'.format(ticker))
        except ConnectionError:
            pass


def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()
    for count, ticker in enumerate(tickers):
        try:
            df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
            df.set_index('Date', inplace=True)
            df.rename(columns= {'Adj Close': ticker}, inplace=True)
            df.drop(['Open','High','Close','Low','Volume'], 1, inplace=True)
            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df, how='outer')

            if count % 10 == 0:
                print(count)
        except FileNotFoundError:
            pass

    print(main_df.head())
    main_df.to_csv('sp500_joined_close.csv')


def visualize_data():
    df = pd.read_csv('sp500_joined_close.csv')
    # df['AAPL'].plot()
    # plt.show()
    # Create a correlation table and generate correlation values
    df_corr = df.corr()
    print(df_corr.head())

    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0])+0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1])+0.5, minor=False)

    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns
    row_labels = df_corr.index

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1, 1)
    plt.tight_layout()
    plt.show()


visualize_data()

