import numpy as np
import pandas as pd


class HullMA:
    def __init__(self, data: pd.DataFrame, period: int, limit: float) -> None:
        self.last_interval = data.index[-1]
        self.close = data.Close
        self.period = period
        self.limit = limit

        self.get_hma()

    def get_last_interval(self) -> str:
        return self.last_interval

    def get_name(self) -> str:
        return "Hull MA"

    @staticmethod
    def claculate_wma(close: pd.Series, period: int) -> pd.Series:
        return close.rolling(period).apply(
            lambda x: ((np.arange(period) + 1) * x).sum() / (np.arange(period) + 1).sum(), raw=True
        )

    @staticmethod
    def calculate_hma(close: pd.Series, period: int) -> pd.Series:
        return HullMA.claculate_wma(
            HullMA.claculate_wma(close, period // 2).multiply(2).sub(
                HullMA.claculate_wma(close, period)), int(np.sqrt(period)
            )
        )
    
    def get_hma(self) -> None:
        self.hma = HullMA.calculate_hma(self.close, self.period)

    def get_reading(self) -> float:
        return self.hma[-1]

    def get_status(self) -> str:
        return ""
    
    def get_buy_sell(self) -> str:
        close = self.close[-1]
        hma = self.get_reading()
        if close > hma:
            return "Buy"
        if close < hma:
            return "Sell"
        return "Gray"
    
    def get_position(self) -> str:
        if  self.get_reading() >= self.limit:
            return "TRENDING"
        return "SIDEWAYS"

    def get_movements(self) -> str:
        return ""

    def to_list(self) -> list[any]:
        return [
            self.get_last_interval(), self.get_name(), self.get_reading(), self.get_status(),
            self.get_buy_sell(), self.get_position(), self.get_movements()
        ]