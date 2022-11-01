from abc import ABC

import pandas as pd
import yfinance as yf


class Loader(ABC):
    @staticmethod
    def get_historical_data(ticker: str, period: str, interval: str, exclude_current_interval: bool = True) -> pd.DataFrame:
        pass


class YahooFinanceLoader(Loader):
    @staticmethod
    def get_historical_data(ticker: str, period: str, interval: str, exclude_current_interval: bool = True) -> pd.DataFrame:
        data = yf.Ticker(ticker).history(period, interval)
        data.index = pd.to_datetime(data.index).date
        if exclude_current_interval:
            data.drop(data.tail(1).index, inplace=True)
        return data