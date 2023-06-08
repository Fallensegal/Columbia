# -*- coding: utf-8 -*-
"""
Created on Fri May 26 16:06:18 2023

@author: Mahir Navid
"""

import yfinance as yf
import pandas as pd
import openai
from datetime import datetime, timedelta


openai.api_key = ''

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

# Fetch the data.
start_date = datetime.now() - pd.DateOffset(years=2)
end_date = datetime.now()

spy_data = yf.download('SPY', start=start_date, end=end_date)

# Calculate the indicators.
spy_data['RSI'] = calculate_rsi(spy_data['Close'], window=14)
spy_data['MA'] = calculate_ma(spy_data['Close'], window=14)
spy_data['MACD'] = calculate_macd(spy_data['Close'], short_window=12, long_window=26)
spy_data['upper_band'], spy_data['middle_band'], spy_data['lower_band'] = calculate_bollinger_bands(spy_data['Close'], window=20)
spy_data['VWAP'] = calculate_vwap(spy_data)

# Resample the daily data to weekly data
spy_data_weekly = spy_data.resample('W').last()

# Reset the index so 'Date' becomes a column
spy_data_weekly = spy_data_weekly.reset_index()

# Convert the DataFrame to a list of dictionaries
spy_data_weekly_dict = spy_data_weekly.to_dict('records')

# Take the last 60 weeks of data
recent_weeks_data = spy_data_weekly_dict[-30:]

# Format each week's data to a string that uses roughly 50 tokens
formatted_data = ["Date: {}, Close: {}, RSI: {}, MA: {}, MACD: {}, Bollinger Bands: {}, VWAP: {}".format(
    week['Date'], week['Close'], week['RSI'], week['MA'], week['MACD'], (week['upper_band'], week['middle_band'], week['lower_band']), week['VWAP']
) for week in recent_weeks_data]

# Join all the formatted data into one string
data_str = "\n".join(formatted_data)

# Array of days
days_array = [1, 2]

# Calculate the future dates
future_dates = [datetime.now() + timedelta(days=day) for day in days_array]

# Now you have a list of future dates:
for date in future_dates:
    print(date.strftime('%m/%d/%Y'))


for future_date in future_dates:
    # Prepare the prompt with the desired format
    prompt = f"Based on the historical technical analysis data for the SPY stock, what is the predicted closing price of SPY on {future_date.strftime('%m/%d/%Y')}?\n\n{data_str}\n\nPrice Prediction: (#), Date: (m/d/y)"

    # Call the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=50
    )

    print(f"Predicted Price on {future_date.strftime('%m/%d/%Y')}: {response.choices[0].text.strip().split(': ')[1]}")

