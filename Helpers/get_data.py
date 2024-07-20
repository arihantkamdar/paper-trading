import requests
import json
import pandas as pd
import os

def get_data(api_key,ticker, time_frame,):
    if time_frame in ['1min', '5min', '15min', '30min', '60min']:
        url =f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval={time_frame}&apikey={api_key}"
        r = requests.get(url)
        data = r.json()
    if time_frame in ['1day']:
        url =f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"
        r = requests.get(url)
        data = r.json()
    if time_frame in ['1week']:
        url =f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={ticker}&apikey={api_key}"
        r = requests.get(url)
        data = r.json()
    if time_frame in ['1month']:
        url =f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={ticker}&apikey={api_key}"
        r = requests.get(url)
        data = r.json()
    keys = data.keys()
    for key in keys:
        if key.startswith("Time Series"):
            data = data[key]
    time = data.keys()
    values = list(data.values())
    open = [i['1. open'] for i in values]
    high = [i['2. high'] for i in values]
    low = [i['3. low'] for i in values]
    close = [i['4. close'] for i in values]
    data = {'Time' : time,
            "Open" : open,
            "High" : high,
            "Close" : close,
            "Low" : low}
    stock_dataframe = pd.DataFrame(data)
    stock_dataframe = stock_dataframe.dropna(subset=['Time', 'Open', 'High', 'Low', 'Close'])
    return stock_dataframe
    



