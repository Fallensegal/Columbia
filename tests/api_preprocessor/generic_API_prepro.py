
import yfinance as yf

class GenericPreprocessor:
    def __init__(self, ticker, period):
        self.ticker = ticker
        self.period = period
        self.data = None

    def download_data(self):
        # Download data from Yahoo Finance
        self.data = yf.download(self.ticker, period=self.period)

    def preprocess_data(self):
        # Preprocess the data to only include closing prices
        self.data = self.data['Close']

    def get_data(self):
        if self.data is None:
            self.download_data()
            self.preprocess_data()
        return self.data
    
