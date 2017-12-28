# Data pre-processing for machine learning
import numpy as np
import pandas as pd
import pickle


def process_data_for_labels(ticker):
    hm_days = 7
    df = pd.read_csv('sp500_joined_close.csv', index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)

    for i in range(1, hm_days+1):
        df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]

    df.fillna(0, inplace=True)
    return ticker, df


print(process_data_for_labels('AAPL'))

