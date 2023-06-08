# -*- coding: utf-8 -*-
"""
Created on Thu May 18 09:55:08 2023

@author: hv872f
"""

import openai
import yfinance as yf
import datetime

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

# Create the question
question = f"Given the historical and real-time price data for {symbol}, provide predictions for the price at the following future points, each on a new line in the format 'Predicted price on [Date]: [Predicted price] USD':\n- 2 business days from today\n- 1 week from today\n- 2 weeks from today\n- 3 weeks from today"

# Combine the data and question
data = historical_data_summary + latest_price + '\n' + question

# Call the OpenAI API to get the AI's response
response = openai.Completion.create(engine="text-davinci-002", prompt=data, max_tokens=100, n=1, stop=None, temperature=0.7)

# Parse the response
predictions = response.choices[0].text.strip().split('\n')

# Create dates for the predictions
today = datetime.date.today()
two_business_days = today + datetime.timedelta(days=2)
one_week = today + datetime.timedelta(weeks=1)
two_weeks = today + datetime.timedelta(weeks=2)
three_weeks = today + datetime.timedelta(weeks=3)

dates = [two_business_days, one_week, two_weeks, three_weeks]

# Combine dates with predictions
predictions_with_dates = [f"{dates[i].strftime('%m/%d/%Y')}: {predictions[i]}" for i in range(4)]

# Print predictions with dates
for prediction in predictions_with_dates:
    print(prediction)