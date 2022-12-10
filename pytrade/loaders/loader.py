import functools

import pandas as pd


class Loader:
    DELIMITER = "/"

    def get_ticker_data(self, ticker: str, period: str, interval: str, exclude_current_interval: bool = True) -> pd.DataFrame:
        tickers = ticker.split(Loader.DELIMITER)
        data = [self.get_historical_data(ticker, period, interval, exclude_current_interval) for ticker in tickers]
        return functools.reduce(lambda t1, t2: t1/t2, data)