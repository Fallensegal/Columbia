# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 09:09:03 2023

@author: hv872f
"""


import yfinance as yf

class YFinance_Stock:
    def __init__(self, ticker, data_range=365):
        # Check is ticker passed in is a string literal
        if not isinstance(ticker, str):
            raise TypeError("Ticker must be a string")
            
        # Check if ticker is valid
        self.ticker = yf.Ticker(ticker)
        
        # Fetch a small amount of data to check if ticker is valid
        try:
            self.ticker.history(period="1d")
        except ValueError:
            # Attribute error raised when ticker does not exist in Yfinance
            raise AttributeError(f"{ticker} is not a valid ticker symbol")
        
        self.data_range = data_range
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
        self.RSI = (100 - (100 / (1 + RS)))[-self.data_range:]

    def calculate_MACD(self, short_period=12, long_period=26, signal_period=9):
        short_EMA = self.price['Close'].ewm(span=short_period, adjust=False).mean()
        long_EMA = self.price['Close'].ewm(span=long_period, adjust=False).mean()
        MACD_line = short_EMA - long_EMA
        signal_line = MACD_line.ewm(span=signal_period, adjust=False).mean()
        self.MACD = (MACD_line - signal_line)[-self.data_range:]

    def calculate_BB(self, period=20):
        SMA = self.price['Close'].rolling(window=period).mean()
        std_dev = self.price['Close'].rolling(window=period).std()
        self.BB_upper = (SMA + (2 * std_dev))[-self.data_range:]
        self.BB_lower = (SMA - (2 * std_dev))[-self.data_range:]

    def calculate_VWAP(self):
        cum_volume = self.price['Volume'].cumsum()
        cum_vwap = (self.price['Close'] * self.price['Volume']).cumsum()
        self.VWAP = (cum_vwap / cum_volume)[-self.data_range:]
    
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