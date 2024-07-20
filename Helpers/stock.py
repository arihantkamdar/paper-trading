from altair import value
import yfinance as yf
import streamlit as st
from Helpers.crud_operation import get_value_float, update_value, insert_row
import logging
logger = logging.getLogger()
import time
from datetime import datetime

logger.setLevel(logging.INFO)

def convert_string(string):
    return "'" + str(string) + "'"

class Stock:
    def __init__(self, conn, name, ticker, username):
        self.conn = conn
        self.name = name
        self.ticker = ticker
        self.username = username
        self.balance = get_value_float(conn=self.conn, col = 'balance', table='users',addition_where = f"where username = '{username}'" )
    def buy(self, quantity):
        stock = yf.Ticker(self.ticker)
        cmp = stock.info.get('ask',None)
        if cmp is not None:
            if self.balance < cmp*quantity:
                st.write("Insufficient Funds")
            else:
                logger.info("Trade in progress")
                self.balance = self.balance - cmp*quantity
                trade_keys = [ 'username', 'trade_date', 'ticker', 'price', 'quantity', 'total_amount', 'trade_type']
                trade_values = [ convert_string(self.username) , convert_string(datetime.today().strftime('%Y-%m-%d')),
                                  convert_string(self.ticker) , cmp, quantity, cmp*quantity, convert_string('BUY') ]
                insert_row(conn = self.conn, table= 'trade_history', cols= trade_keys, values = trade_values)
                update_value(conn=self.conn, col='balance', table='users', value= self.balance,where_clause= f"where username = '{self.username}'")
                st.write("Executed Buy Trade")    
                logger.info("Trade Completed")
        else:
            st.write("Cannot Execute as cmp is not available")
    def sell(self, quantity):
        quantity *= -1
        stock = yf.Ticker(self.ticker)
        cmp = stock.info.get('ask',None)
        if cmp is not None:
            logger.info("Trade in progress")
            self.balance = self.balance - cmp*quantity
            trade_keys = [ 'username', 'trade_date', 'ticker', 'price', 'quantity', 'total_amount', 'trade_type']
            trade_values = [ convert_string(self.username) , convert_string(datetime.today().strftime('%Y-%m-%d')),
                            convert_string(self.ticker) , cmp, quantity, cmp*quantity, convert_string('SELL') ]
            insert_row(conn = self.conn, table= 'trade_history', cols= trade_keys, values = trade_values)
            update_value(conn=self.conn, col='balance', table='users', value= self.balance, where_clause= f"where username = '{self.username}'")
            st.write("Executed Sell Trade")
            logger.info("Trade Completed")
        else:
            st.write("Cannot Execute as cmp is not available")
