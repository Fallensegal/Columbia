# -*- coding: utf-8 -*-
"""
Created on Thu May 18 18:44:22 2023

@author: Mahir Navid
"""

import openai
import yfinance as yf
import datetime
from dateutil.rrule import rrule, FR, WEEKLY

# Set up your OpenAI API key
openai.api_key = ''

# Gather historical price data
symbol = 'SPY'
start_date = (datetime.datetime.now() - datetime.timedelta(days=3650)).strftime('%Y-%m-%d')
end_date = datetime.datetime.now().strftime('%Y-%m-%d')

ticker = yf.Ticker(symbol)
historical_data = ticker.history(start=start_date, end=end_date)

# Get the latest stock price using Yahoo Finance API
current_quote = ticker.history(period='1d').iloc[-1]

# Format the data
historical_data_summary = f"Historical price data for the past year:\n{historical_data}\n"
latest_price = f"Current price of {symbol}: {current_quote['Close']} USD\n"

# Calculate the date of the next Friday
today = datetime.date.today()
days_ahead = 4 - today.weekday()
if days_ahead <= 0:  # Target day already happened this week
    days_ahead += 7
next_friday = today + datetime.timedelta(days=days_ahead)
next_friday_str = next_friday.strftime('%m/%d/%Y')

# Create the question
question = f"Based on the historical and real-time price data for {symbol}, can you provide a hypothetical closing price prediction for next Friday ({next_friday_str}), along with a detailed explanation of why you arrived at this prediction?"

# Combine the data and question
data = historical_data_summary + latest_price + '\n' + question

# Call the OpenAI API to get the AI's response
response = openai.Completion.create(engine="text-davinci-002", prompt=data, max_tokens=300, n=1, stop=None, temperature=0.3)

# Print the AI's response
print(response.choices[0].text.strip())
