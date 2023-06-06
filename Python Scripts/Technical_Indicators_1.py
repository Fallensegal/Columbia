# -*- coding: utf-8 -*-
"""
Created on Fri May 26 22:49:40 2023

@author: Mahir Navid
"""

import yfinance as yf
import pandas as pd
import openai
from datetime import datetime, timedelta

openai.api_key = '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'

def calculate_rsi(data, window):
    delta = data.diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    average_gain = up.rolling(window).mean()
    average_loss = abs(down.rolling(window).mean())

    rs = average_gain / average_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi

def calculate_ma(data, window):
    return data.rolling(window).mean()

def calculate_macd(data, short_window, long_window):
    short_ma = calculate_ma(data, short_window)
    long_ma = calculate_ma(data, long_window)
    return short_ma - long_ma

def calculate_bollinger_bands(data, window):
    ma = calculate_ma(data, window)
    std_dev = data.rolling(window).std()
    upper_band = ma + (std_dev * 2)
    lower_band = ma - (std_dev * 2)
    return upper_band, ma, lower_band

def calculate_vwap(data):
    vwap = data['Close'].mul(data['Volume']).cumsum().div(data['Volume'].cumsum())
    return vwap

def fetch_and_predict(ticker, days_array):

    start_date = datetime.now() - pd.DateOffset(years=2)
    end_date = datetime.now()

    data = yf.download(ticker, start=start_date, end=end_date)

    data['RSI'] = calculate_rsi(data['Close'], window=14)
    data['MA'] = calculate_ma(data['Close'], window=14)
    data['MACD'] = calculate_macd(data['Close'], short_window=12, long_window=26)
    data['upper_band'], data['middle_band'], data['lower_band'] = calculate_bollinger_bands(data['Close'], window=20)
    data['VWAP'] = calculate_vwap(data)

    data_weekly = data.resample('W').last()
    data_weekly = data_weekly.reset_index()

    data_weekly_dict = data_weekly.to_dict('records')
    recent_weeks_data = data_weekly_dict[-30:]

    formatted_data = ["Date: {}, Close: {}, RSI: {}, MA: {}, MACD: {}, Bollinger Bands: {}, VWAP: {}".format(
        week['Date'], week['Close'], week['RSI'], week['MA'], week['MACD'], (week['upper_band'], week['middle_band'], week['lower_band']), week['VWAP']
    ) for week in recent_weeks_data]

    data_str = "\n".join(formatted_data)

    future_dates = [datetime.now() + timedelta(days=day) for day in days_array]

    for future_date in future_dates:
        prompt = f"Based on the historical technical analysis data for the {ticker} stock, what is the predicted closing price of {ticker} on {future_date.strftime('%m/%d/%Y')}?\n\n{data_str}\n\nPrice Prediction: (#), Date: (m/d/y)"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=50
        )

        print(f"Predicted Price on {future_date.strftime('%m/%d/%Y')}: {response.choices[0].text.strip().split(': ')[1]}")

# Example usage:
fetch_and_predict('VZ', [1,2,3,4])
