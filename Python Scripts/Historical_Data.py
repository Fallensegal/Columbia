# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 21:40:42 2023

@author: Mahir Navid
"""

import yfinance as yf
import pandas as pd
import openai
from datetime import datetime, timedelta


def fetch_and_predict(ticker):
    start_date = datetime.now() - pd.DateOffset(days=1205)  # Approximately 3.3 Years
    end_date = datetime.now()
    

    data = yf.download(ticker, start=start_date, end=end_date)

    # Store closing prices in a variable
    historical_closing_prices = data['Close']
    
    # Print today's closing price
    todays_close = data.iloc[-1]['Close']
    print(f"Today's closing price for {ticker}: {todays_close}")

    # Reset index so that 'Date' becomes a column in the DataFrame
    data.reset_index(inplace=True)

    # Filter for Fridays
    data = data[data['Date'].dt.weekday == 4]

    # Convert the DataFrame into a dictionary
    data_dict = data.to_dict('records')

    # Format the data for the prompt
    formatted_data = ["Date: {}, Close: {}".format(
        day['Date'], day['Close']
    ) for day in data_dict]

    data_str = "\n".join(formatted_data)

    # Calculate the next two Fridays
    today = datetime.now()
    days_until_friday = (4 - today.weekday() + 7) % 7
    next_friday = today + timedelta(days=days_until_friday)
    friday_after_next = next_friday + timedelta(days=7)

    future_fridays = [next_friday, friday_after_next]

    for future_date in future_fridays:
        prompt = f"Based on the historical closing price data for the {ticker} stock every Friday for the past 4 years, if you were to guess a numerical value for the closing price of {ticker} on {future_date.strftime('%m/%d/%Y')}, what would it be? Please make sure to provide a numerical value, even if it's just a guess.\n\n{data_str}\n\nPrice Prediction:"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=50
            )
        
        print(f"AI Response: {response.choices[0].text.strip()}")
        
        response_text = response.choices[0].text.strip()
        predicted_price = response_text.split(': ')[1] if ': ' in response_text else 'Unknown'
        print(f"Predicted Price on {future_date.strftime('%m/%d/%Y')}: {predicted_price}")
        

fetch_and_predict('VZ')
