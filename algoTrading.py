import numpy as np
import pandas as pd
import requests
import math
import xlsxwriter
from scipy import stats

stocks = pd.read_csv('sp_500_stocks.csv')
from secrets import IEX_CLOUD_API_TOKEN

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

stock_symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = [','.join(stock_symbol_groups[i]) for i in range(len(stock_symbol_groups))]


my_columns = ['Ticker', 'Price','One-Year Price Return', 'Number Of Shares to Buy']
hqm_columns = [
                'Ticker',
                'Price',
                'Number of Shares to Buy',
                'One-Year Price Return',
                'One-Year Return Percentile',
                'Six-Month Price Return',
                'Six-Month Return Percentile',
                'Three-Month Price Return',
                'Three-Month Return Percentile',
                'One-Month Price Return',
                'One-Month Return Percentile',
                'HQM Score'
                ]

hqm_dataframe = pd.DataFrame(columns = hqm_columns)
finalDataframe = pd.DataFrame(columns=my_columns)
for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=stats,quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        hqm_dataframe = hqm_dataframe.append(
            pd.Series([symbol,
                       data[symbol]['quote']['latestPrice'],
                       'N/A',
                       data[symbol]['stats']['year1ChangePercent'],
                       'N/A',
                       data[symbol]['stats']['month6ChangePercent'],
                       'N/A',
                       data[symbol]['stats']['month3ChangePercent'],
                       'N/A',
                       data[symbol]['stats']['month1ChangePercent'],
                       'N/A',
                       'N/A'
                       ],
                      index=hqm_columns),
            ignore_index=True)
#specific to pycharm to display wider dataframe
desired_width = 320
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)




time_periods = [
                'One-Year',
                'Six-Month',
                'Three-Month',
                'One-Month'
                ]

#calculate percentile according to your evaluations and fill in df

# for row in hqm_dataframe.index:
#     for time_period in time_periods:
#         hqm_dataframe.loc[row, f'{time_period} Return Percentile'] = \
#             stats.percentileofscore(hqm_dataframe[f'{time_period} Price Return'],
#                                     hqm_dataframe.loc[row, f'{time_period} Price Return'])/100
