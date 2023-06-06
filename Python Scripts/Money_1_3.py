# -*- coding: utf-8 -*-
"""
Created on Thu May 18 18:26:56 2023

@author: Mahir Navid
"""

import openai
import yfinance as yf
from datetime import datetime, timedelta
from dateutil.rrule import rrule, FR, WEEKLY
from dateutil.relativedelta import relativedelta

# Set up your OpenAI API key
openai.api_key = ''

# Gather historical price data
symbol = 'SPY'
start_date = (datetime.now() - timedelta(days=3650)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')

ticker = yf.Ticker(symbol)
historical_data = ticker.history(start=start_date, end=end_date)

# Get the latest stock price using Yahoo Finance API
current_quote = ticker.history(period='1d').iloc[-1]

# Format the data
historical_data_summary = f"Historical price data for the past year:\n{historical_data}\n"
latest_price = f"Current price of {symbol}: {current_quote['Close']} USD\n"

# Create dates for the predictions
today = datetime.today()
two_weeks_later = today + relativedelta(weeks=2)

fridays = list(rrule(freq=WEEKLY, dtstart=today, until=two_weeks_later, byweekday=(FR)))

# Now `fridays` contains all Fridays for the next 2 weeks.
fridays = fridays[:2]

# Create the question
dates_str = ", ".join([f"{i.strftime('%m/%d/%Y')}" for i in fridays])
question = f"Given the historical and real-time price data for {symbol}, what do you predict the closing price will be on the following dates: {dates_str}?"

# Combine the data and question
data = historical_data_summary + latest_price + '\n' + question

# Call the OpenAI API to get the AI's response
response = openai.Completion.create(engine="text-davinci-002", prompt=data, max_tokens=100, n=1, stop=None, temperature=0.7)

# Parse the response
predictions = response.choices[0].text.strip().split('\n')

# Combine dates with predictions
predictions_with_dates = [f"{fridays[i].strftime('%m/%d/%Y')}: {predictions[i]}" for i in range(len(fridays))]

# Print predictions with dates
for prediction in predictions_with_dates:
    print(prediction)

print("Raw AI response: ", response.choices[0].text.strip())
