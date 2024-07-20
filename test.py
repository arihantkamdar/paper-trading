import streamlit as st
import yfinance as yt
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.hasher import Hasher
import pandas as pd
import requests
import yfinance as yf

import yfinance as yf

# Define the ticker symbol for which we want the current market price
ticker_symbol = "AAPL"  # Apple Inc. as an example

# Get the stock data
stock = yf.Ticker(ticker_symbol)
print(stock.info['ask'])
# Get the current market price
current_price = stock.history(period="1d")['Close'].iloc[0]
print(f"The current market price of {ticker_symbol} is ${current_price:.2f}")

# msft = yf.Ticker("MSFT")

# get all stock info
# print(msft.info)

# print("Successfully imported modules")
# # EMO57QFCAEQPR2IB
# hashed_passwords = Hasher(['abc', 'def']).generate()
# print(hashed_passwords)


# stocks_available = pd.read_html(
#     'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]

# print(stocks_available)

# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo&datatype=csv'
# r = requests.get(url)
# data = r.json()

# print(data)

