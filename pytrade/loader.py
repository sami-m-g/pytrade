import functools

import pandas as pd
import yfinance as yf


class Loader:
    DELIMITER = "/"

    def get_ticker_data(self, ticker: str, period: str, interval: str, exclude_current_interval: bool = True) -> pd.DataFrame:
        tickers = ticker.split(Loader.DELIMITER)
        data = [self.get_historical_data(ticker, period, interval, exclude_current_interval) for ticker in tickers]
        return functools.reduce(lambda t1, t2: t1/t2, data)


class YahooFinanceLoader(Loader):
    def get_historical_data(self, ticker: str, period: str, interval: str, exclude_current_interval: bool = True) -> pd.DataFrame:
        data = yf.Ticker(ticker).history(period, interval)
        data.index = pd.to_datetime(data.index).date
        if exclude_current_interval:
            data.drop(data.tail(1).index, inplace=True)
        return data