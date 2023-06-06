# -*- coding: utf-8 -*-
"""
Created on Thu May 18 15:04:37 2023

@author: hv872f
"""

import openai
import yfinance as yf
import datetime
from dateutil.rrule import rrule, WEEKLY, MO, FR
from dateutil.relativedelta import relativedelta

# Set up your OpenAI API key
openai.api_key = ''

# Gather historical price and volume data
symbol = 'SPY'
start_date = (datetime.datetime.now() - datetime.timedelta(days=3650)).strftime('%Y-%m-%d')
end_date = datetime.datetime.now().strftime('%Y-%m-%d')

ticker = yf.Ticker(symbol)
historical_data = ticker.history(start=start_date, end=end_date)

# Get the latest stock price and volume using Yahoo Finance API
current_quote = ticker.history(period='1d').iloc[-1]

# Format the data
historical_data_summary = f"Historical price and volume data for the past year:\n{historical_data}\n"
latest_price = f"Current price of {symbol}: {current_quote['Close']} USD\n"
latest_volume = f"Current volume of {symbol}: {current_quote['Volume']}\n"

# Create dates for the predictions
today = datetime.datetime.now()
three_weeks_later = today + relativedelta(weeks=3)

mondays_and_fridays = list(rrule(freq=WEEKLY, dtstart=today, until=three_weeks_later, byweekday=(MO,FR)))
mondays_and_fridays = mondays_and_fridays[:6]

# Create the question
dates_str = ", ".join([f"{i.strftime('%m/%d/%Y')}" for i in mondays_and_fridays])
question = f"Given the historical and real-time price and volume data for {symbol}, what do you predict the closing price will be on the following dates: {dates_str}?"

# Combine the data and question
data = historical_data_summary + latest_price + latest_volume + '\n' + question

# Call the OpenAI API to get the AI's response
response = openai.Completion.create(engine="text-davinci-002", prompt=data, max_tokens=100, n=1, stop=None, temperature=0.7)

# Parse the response
predictions = response.choices[0].text.strip().split('\n')

# Combine dates with predictions
predictions_with_dates = [f"{mondays_and_fridays[i].strftime('%m/%d/%Y')}: {predictions[i]}" for i in range(len(mondays_and_fridays))]

# Print predictions with dates
for prediction in predictions_with_dates:
    print(prediction)
