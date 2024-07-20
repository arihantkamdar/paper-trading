import streamlit as st
from streamlit_authenticator import Authenticate
import logging
import yaml
from yaml.loader import SafeLoader
import yfinance as yf
import pandas as pd
import json
from Helpers.stock import Stock
from Helpers.get_data import get_data
from Helpers.plot_candlestick import plot_candlestick
import psycopg2
from dotenv import load_dotenv
import os
from Helpers.crud_operation import get_value_float, update_value

load_dotenv() 
api_key = os.getenv("API_KEY") 


conn = psycopg2.connect(database = os.getenv("DB_NAME"), 
                        user = os.getenv("USER"), 
                        host= os.getenv("HOST"),
                        password = os.getenv("PASSWORD"),
                        port = os.getenv("PORT"))

global_market = 'US'

logging.basicConfig(filename="Log.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
 
# Creating an object
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Setting the threshold of logger to
logger.info('Modules imported sucessfully')

with open('data.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('main', fields = {'Form name': 'custom_form_name'})

def get_market_data():

    with open('Database/US_stocks.json') as json_file:
        stock_mapping = json.load(json_file)
        logger.info("Json Loaded successfully")
    return stock_mapping


def get_current_holdings(username):
    sql_buy = f"""
    Select ticker, SUM(quantity), SUM(total_amount), trade_type from trade_history
    where username = '{username}' and trade_type = 'BUY'
    group by ticker, trade_type"""
    sql_sell = f"""
    Select ticker, SUM(quantity) as qty, SUM(total_amount), trade_type from trade_history
    where username = '{username}' and trade_type = 'SELL'
    group by ticker, trade_type"""
    cur = conn.cursor()
    cur.execute(sql_buy)
    buy_rows = cur.fetchall()
    buy_rows_dict = convert_2_dict(buy_rows)
    cur.execute(sql_sell)
    sell_rows = cur.fetchall()
    sell_rows_dict = convert_2_dict(sell_rows)
    # all_tickers = list(set([i["ticker"] for i in buy_rows] + [[i["ticker"] for i in sell_rows]]))
    total_tickers = list(set(list(buy_rows_dict.keys()) + list(sell_rows_dict.keys())))
    # total_holdings = {}

    results =[]
    for ticker in total_tickers:
        temp_dict = {}
        temp_dict["qty"] = float(buy_rows_dict.get(ticker,{}).get('quantity',0)) + float(sell_rows_dict.get(ticker,{}).get('quantity',0))
        temp_dict['amount_invested'] = float(buy_rows_dict.get(ticker,{}).get('amount',0)) + float(sell_rows_dict.get(ticker,{}).get('amount',0))
        stock = yf.Ticker(ticker)
        temp_dict['cmp'] = float(stock.info.get('ask',0))
        temp_dict['Running PnL'] = round(float(temp_dict['cmp']*temp_dict['qty']) - float(temp_dict['amount_invested']),2)
        temp_dict['ticker'] = ticker
        results.append(temp_dict)
        # total_holdings[ticker] = temp_dict
    holdings = pd.DataFrame.from_records(results)
    holdings = holdings[holdings['qty']!=0]
    return holdings


def convert_2_dict(rows):
    # result = []
    result_2 = {}
    for row in rows:
        row_dict = {}
        row_dict['quantity'] = round(float(row[1]),2)
        row_dict['amount'] = round(float(row[2]),2)
        row_dict['ticker'] = row[0]
        result_2[row[0]] = row_dict
    return result_2



if authentication_status:
    balance = get_value_float(conn=conn, col = 'balance', table= "users", addition_where = f"where username = '{username}'")
    stock_name = None
    logger.info(f'Logging Successful for {name}')
    st.write(f'Welcome *{name}*')
    st.write(f'Available Balance : {balance}' )
    st.title('Paper Trading Platform')
    add_bal_col,balance_col,sub_bal_col= st.columns(3)
    balance_to_add = None
    balance_to_add  = balance_col.number_input("Enter Amount to add or withdraw", value=None, placeholder="")    
    if add_bal_col.button("Add Funds"):
        if balance_to_add:
            balance = balance + balance_to_add
            update_value(conn=conn, col='balance', table='users', value= balance,where_clause= f"where username = '{username}'")
            st.write("Balance Updated.  New Balance : ",balance) 
    if sub_bal_col.button("Withdraw Funds"):
        if balance_to_add:
            balance = balance - balance_to_add
            update_value(conn=conn, col='balance', table='users', value= balance,where_clause= f"where username = '{username}'")
            st.write("Balance Updated.  New Balance : ",balance) 

    
    stock_mapping = get_market_data()
    stock_names = list(stock_mapping.keys())    
    stock_selected = st.selectbox("Select Stock", stock_names)
    ticker = stock_mapping[stock_selected]
    stock = yf.Ticker(ticker)
    st.write("Ask Price for the Stock : ",stock.info.get('ask',"Not Available"))
    buy,quantity, sell = st.columns(3)
    qty = None
    qty = quantity.number_input("Insert a number", value=None, placeholder="Enter Quantity")    
    if buy.button("BUY", key='green', help="Click Here to Buy the Stock"):
        if qty is None:
            st.write("Please Enter the Quantity")
        else:
            stock = Stock(conn=conn, name=stock_selected,ticker=ticker, username=username)
            stock.buy(quantity=qty)
    if sell.button("SELL", key='red', help="Click here to sell the stock"):
        if qty is None:
            st.write("Please Enter the Quantity")
        else:
            stock = Stock(conn=conn,name=stock_selected,ticker=ticker, username=username)
            stock.sell(quantity=qty)
    if st.button("Get Current Holdings"):
        holdings = get_current_holdings(username)
        st.dataframe(holdings.style.hide(axis="index"))
    time_frame =  st.selectbox("Select Time Frame", ['1min', '5min', '15min', '30min', '60min', "1day", "1week", "1month"])
    if st.button("Plot Candle Stick"):
        data = get_data(api_key,ticker, time_frame)
        plot_candlestick(data=data)
elif authentication_status == False:
    logger.info(f'Logging Unsuccessful')
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')



    

    


# def get_all_stocks(conn, username):


# # def 
