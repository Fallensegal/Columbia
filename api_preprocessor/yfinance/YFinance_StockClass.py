import yfinance as yf

class YFinance_Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.RSI = None
        self.MACD = None
        self.BB = None
        self.VWAP = None
        self.Price = None 

    def get_price(self, period="1y"):
        # get historical market data
        self.price = yf.Ticker(self.ticker).history(period=period)

    def get_close_prices(self):
        return self.data['Close'] if self.data is not None else None

    def calculate_daily_close(self):
        self.data['daily_close'] = self.data['Close'].resample('D').last()

    def calculate_weekly_close(self):
        self.data['weekly_close'] = self.data['Close'].resample('W').last()

    def calculate_monthly_close(self):
        self.data['monthly_close'] = self.data['Close'].resample('M').last()





stock = Stock("SPY")

