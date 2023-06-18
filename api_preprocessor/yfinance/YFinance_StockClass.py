# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 13:54:19 2023

@author: hv872f
"""
import yfinance as yf
"""
Note: pandas API is being used indirectly through yfinance so no need to "import 
pandas" The resample, diff, rolling, ewm, mean, and std, are all pandas 
methods that are being called on the DataFrame object that 
yf.Ticker(self.ticker).history(period=period) returns
"""

"""
Note:
Trying to calculate any of the indicators before getting the 
price data with get_price() would result in error because price 
DataFrame would be None.

I might add exception handling or ensure 
the get_price() method is always called before any calculation methods.
"""


class YFinance_Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.price = None
        self.RSI = None
        self.MACD = None
        self.BB_upper = None
        self.BB_lower = None
        self.VWAP = None

    def get_price(self, period="1y"):
        # get historical market data
        self.price = yf.Ticker(self.ticker).history(period=period)

    def get_close_prices(self):
        return self.price['Close'] if self.price is not None else None

    def calculate_daily_close(self):
        self.price['daily_close'] = self.price['Close'].resample('D').last()

    def calculate_weekly_close(self):
        self.price['weekly_close'] = self.price['Close'].resample('W').last()

    def calculate_monthly_close(self):
        self.price['monthly_close'] = self.price['Close'].resample('M').last()

    def calculate_RSI(self, period=14):
        delta = self.price['Close'].diff()
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        gain = up.rolling(window=period).mean()
        loss = abs(down.rolling(window=period).mean())
        RS = gain / loss
        self.RSI = 100 - (100 / (1 + RS))

    def calculate_MACD(self, short_period=12, long_period=26, signal_period=9):
        short_EMA = self.price['Close'].ewm(span=short_period, adjust=False).mean()
        long_EMA = self.price['Close'].ewm(span=long_period, adjust=False).mean()
        MACD_line = short_EMA - long_EMA
        signal_line = MACD_line.ewm(span=signal_period, adjust=False).mean()
        self.MACD = MACD_line - signal_line

    def calculate_BB(self, period=20):
        SMA = self.price['Close'].rolling(window=period).mean()
        std_dev = self.price['Close'].rolling(window=period).std()
        self.BB_upper = SMA + (2 * std_dev)
        self.BB_lower = SMA - (2 * std_dev)

    def calculate_VWAP(self):
        cum_volume = self.price['Volume'].cumsum()
        cum_vwap = (self.price['Close'] * self.price['Volume']).cumsum()
        self.VWAP = cum_vwap / cum_volume
    
    def get_latest_values(self):
        return {
            'latest_close': self.get_close_prices()[-1] if self.price is not None else None,
            'latest_RSI': self.RSI[-1] if self.RSI is not None else None,
            'latest_MACD': self.MACD[-1] if self.MACD is not None else None,
            'latest_BB_upper': self.BB_upper[-1] if self.BB_upper is not None else None,
            'latest_BB_lower': self.BB_lower[-1] if self.BB_lower is not None else None,
            'latest_VWAP': self.VWAP[-1] if self.VWAP is not None else None,
            # add lines for additional indicators here
        }




# SAMPLE CODE TO USE ABOVE CLASS:
"""
stock = YFinance_Stock("SPY")
stock.get_price()
stock.calculate_RSI()
stock.calculate_MACD()
"""