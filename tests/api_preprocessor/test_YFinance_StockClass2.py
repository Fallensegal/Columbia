
import pytest
import yfinance as yf
from test_YFinance_StockClass2 import YFinance_Stock

class TestYFinanceStock:

    @pytest.fixture(scope="module")
    def stock(self):
        return YFinance_Stock('SPY')

    def test_get_price(self, stock):
        stock.get_price()
        assert isinstance(stock.price, yf.base.TickerBase)  

    def test_get_close_prices(self, stock):
        stock.get_price()
        result = stock.get_close_prices()
        assert isinstance(result, list)  

    def test_calculate_daily_close(self, stock):
        stock.get_price()
        stock.calculate_daily_close()
        assert 'daily_close' in stock.price.columns

    def test_calculate_weekly_close(self, stock):
        stock.get_price()
        stock.calculate_weekly_close()
        assert 'weekly_close' in stock.price.columns

    def test_calculate_monthly_close(self, stock):
        stock.get_price()
        stock.calculate_monthly_close()
        assert 'monthly_close' in stock.price.columns

    def test_calculate_RSI(self, stock):
        stock.get_price()
        stock.calculate_RSI()
        assert stock.RSI is not None

    def test_calculate_MACD(self, stock):
        stock.get_price()
        stock.calculate_MACD()
        assert stock.MACD is not None

    def test_calculate_BB(self, stock):
        stock.get_price()
        stock.calculate_BB()
        assert stock.BB_upper is not None
        assert stock.BB_lower is not None

    def test_calculate_VWAP(self, stock):
        stock.get_price()
        stock.calculate_VWAP()
        assert stock.VWAP is not None

    def test_get_latest_values(self, stock):
        stock.get_price()
        stock.calculate_daily_close()
        stock.calculate_weekly_close()
        stock.calculate_monthly_close()
        stock.calculate_RSI()
        stock.calculate_MACD()
        stock.calculate_BB()
        stock.calculate_VWAP()
        result = stock.get_latest_values()
        assert isinstance(result, dict)
        assert 'latest_close' in result
        assert 'latest_RSI' in result
        assert 'latest_MACD' in result
        assert 'latest_BB_upper' in result
        assert 'latest_BB_lower' in result
        assert 'latest_VWAP' in result

