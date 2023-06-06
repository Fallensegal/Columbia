# -*- coding: utf-8 -*-
"""
Created on Wed May 17 19:46:04 2023

@author: Mahir Navid
"""
import openai
import yfinance as yf
import pandas_ta as ta
import datetime

# Set up your OpenAI API key
openai.api_key = "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"

# Gather historical price data
symbol = 'SPY'
start_date = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
end_date = datetime.datetime.now().strftime('%Y-%m-%d')

ticker = yf.Ticker(symbol)
historical_data = ticker.history(start=start_date, end=end_date)

# Get the latest stock price using Yahoo Finance API
current_quote = ticker.history(period='1d').iloc[-1]

# Calculate technical indicators
historical_data.ta.sma(close='Close', length=10, append=True)
historical_data.ta.rsi(close='Close', length=14, append=True)
historical_data.ta.bbands(close='Close', length=20, append=True)

# Format the data
historical_data_summary = f"Historical price data for the past year:\n{historical_data}\n"
latest_price = f"Current price of {symbol}: {current_quote['Close']} USD\n"

# Create the question
question = f"Based on the historical data, real-time price data, and technical indicators for {symbol}, what do you think the price will be in 3 weeks?"

# Combine the data and question
data = historical_data_summary + latest_price + '\n' + question

# Call the OpenAI API to get the AI's response
response = openai.Completion.create(engine="text-davinci-002", prompt=data, max_tokens=100, n=1, stop=None, temperature=0.7)

# Print the AI's response
print(response.choices[0].text.strip())
