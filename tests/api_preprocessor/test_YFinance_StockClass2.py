import pytest
import yfinance as yf
import pandas as pd  # Add this line
from generic_API_prepro import GenericPreprocessor  

def test_generic_preprocessor():
    # Test if class instantiates without errors
    preprocessor = GenericPreprocessor('SPY', '1yr')
    
    # Test if data download and preprocess works
    data = preprocessor.get_data()
    
    # Test if the data is a pandas Series
    assert isinstance(data, pd.Series)
    
    # Test if the data is not empty
    assert not data.empty

    
